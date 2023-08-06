#!/usr/bin/env python
# ******************************************************************************
# Copyright 2023 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

__all__ = ["calibrate", "calibration_required"]

import numpy as np
import tensorflow as tf

from copy import deepcopy
from keras.layers import (Conv2D, Conv2DTranspose, SeparableConv2D, DepthwiseConv2D, Dense, Dropout,
                          Reshape, Flatten, MaxPool2D, GlobalAvgPool2D)

from .transforms.insert_layer import insert_in_config
from .transforms.transforms_utils import get_layers_by_type
from .utils import apply_weights_to_model
from ..layers import (OutputQuantizer, OutputObserver, PaddedConv2D, DepthwiseConv2DTranspose,
                      Attention)
from ..tensors import FixedPoint, floor_log2


def calibration_required(model):
    """Checks if a model requires calibration.

    If one of the 'OutputQuantizer' layers in the model has its range_max variable set to 1, it
    requires calibration.

    Args:
        model (keras.Model): the model to check

    Returns:
        bool: True if calibration is required, False otherwise.
    """
    calibrables = get_layers_by_type(model, OutputQuantizer)
    for calibrable in calibrables:
        # If the model has never been calibrated, all range_max of the OutputQuantizer objects
        # will be set to 1.
        if tf.reduce_all(calibrable.variables[0] == 1):
            return True
    # all calibrable objects are set
    return False


def _get_calibration_model(model, qmodel):
    """Builds a calibration model with OutputObserver added between blocks.

    Args:
        model (keras.Model): input model
        qmodel (keras.Model): quantized model

    Returns:
        keras.Model, dict: the calibration ready model and dict mapping end of block layer names to
        the name of their OutputObserver.
    """
    # Get model config to edit
    config = deepcopy(model.get_config())

    # Insert OutputObservers where OutputQuantizers are
    end_of_blocks = {}
    for layer in qmodel.layers:
        if getattr(layer, 'out_quantizer', None):
            # Build an observer and store it for future use
            observer = OutputObserver(layer.out_quantizer.axis)
            end_of_blocks[layer.name] = observer.name
            # Insert observer in config
            insert_in_config(model, layer.name, observer, config)

    # Build the calibration model from the config
    custom_objects = {"OutputObserver": OutputObserver}
    calibration_model = model.from_config(config, custom_objects)

    # Load original weights
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(calibration_model, variables_dict, False)
    return calibration_model, end_of_blocks


def _get_next_layer(layer, supported_layers, skippable_layers, reshape_ops):
    """ Finds the layer following a target layer.

    Args:
        layer (keras.Layer): the layer of interest
        supported_layers (list): layer types that will support equalization
        skippable_layers (list): layer types that can be skipped
        reshape_ops (list): list of reshape operation encountered as
            [(input_shape,), (output_shape,)]

    Returns:
        keras.Layer: the layer following the layer of interest if valid, None otherwise
    """
    # Limit support to single outbound
    outbounds = layer.outbound_nodes
    if len(outbounds) != 1:
        return None
    next_layer = outbounds[0].layer

    # If the layer is supported, it is a valid candidate
    if isinstance(next_layer, supported_layers):
        return next_layer
    # If the next layer can be skipped, recursively call the function
    elif isinstance(next_layer, skippable_layers):
        return _get_next_layer(next_layer, supported_layers, skippable_layers, reshape_ops)
    # If the next layer is a Reshape or Flatten store the performed ops and continue (limit reshape
    # ops to a single layer)
    elif isinstance(next_layer, (Reshape, Flatten)) and len(reshape_ops) == 0:
        reshape_ops.append([next_layer.input_shape[1:], next_layer.output_shape[1:]])
        return _get_next_layer(next_layer, supported_layers, skippable_layers, reshape_ops)

    # If next layer is not supported, alignment cannot happen
    return None


def _set_and_equalize(qmodel, layer_name, range_max):
    """ Set 'layer_name' output quantizer range_max to the ideal value.

    The ideal range_max is computed from the maximum value the target layer OutputQuantizer's
    can represent given it's bitwidth, and the float calibrated range_max.

    The ratio between the calibrated value and the ideal value is stored in the OutputQuantizer and
    will be applied when the scale_out operation happens. Equalization happens by dividing weights
    of the next layer by the ratio to preserve global outputs.

    Args:
        qmodel (keras.Model): quantized keras model
        layer_name (str): layer name where to set the range_max
        range_max (tf.Tensor): the float calibrated range_max
    """
    # First set the calibrated range_max in the target OutputQuantizer
    target_layer = qmodel.get_layer(layer_name)
    target_layer.out_quantizer.range_max.assign(range_max)

    # Skip Attention layers because they do not perform a scale out so rescaling rate cannot be
    # applied
    if isinstance(target_layer, Attention):
        return

    # Define layers that will support or can be skipped when equalizing
    supported_layers = (Conv2D, PaddedConv2D, Conv2DTranspose, SeparableConv2D, DepthwiseConv2D,
                        Dense, DepthwiseConv2DTranspose)
    skippable_layers = (Dropout, MaxPool2D, GlobalAvgPool2D)
    # When quantized per-tensor, Reshaping layers can be skipped as the rescaling rate single value
    # will be used during equalization on all weights values
    if target_layer.out_quantizer.axis == 'per-tensor':
        skippable_layers += (Reshape, Flatten)

    # Retrieve next_layer: if there is no candidate layer following layer_name, equalization cannot
    # happen
    reshape_ops = []
    next_layer = _get_next_layer(target_layer, supported_layers, skippable_layers, reshape_ops)
    if next_layer is None:
        return

    # Compute ideal range_max
    bitwidth = target_layer.out_quantizer.bitwidth
    frac_bits = bitwidth - floor_log2(range_max)
    int_max = FixedPoint.int_max(bitwidth)
    ideal_range_max = FixedPoint(int_max, bitwidth, frac_bits).to_float().numpy()

    # Check that values are different
    if np.all(ideal_range_max == range_max):
        return

    # Set ideal_range_max into the target OutputQuantizer
    target_layer.out_quantizer.range_max.assign(ideal_range_max)

    # Compute the rescaling rate
    rescaling_rate = ideal_range_max / range_max.numpy()

    # range_max can be 0 on some channels (eg. a ReLU where an input channel had all negative
    # values), when that happens, rescaling_rate is forced to 1 so that cross-layer equalization
    # does nothing.
    rescaling_rate = np.where(range_max == 0, 1, rescaling_rate)

    # Set rate in the target OutputQuantizer
    target_layer.out_quantizer.rescaling_rate.assign(rescaling_rate)

    # Divide weights of the next layer by the rescaling rate
    next_weights = next_layer.get_weights()
    new_weights = next_weights[0]

    # Apply reshape ops
    if reshape_ops:
        # Supporting a single reshape ops
        reshape_ops = reshape_ops[0]
        # Check that last dimension is unchanged by the reshape ops, if that's not the case, the op
        # needs to be undone on weights, eg. for Flatten: X*Y*C, F -> X, Y, C, F
        if reshape_ops[0][-1] != reshape_ops[1][-1]:
            F = (new_weights.shape[-1], )
            new_weights = np.reshape(new_weights, reshape_ops[0] + F)
        # Invert last two dimensions (input and output channels), eg. for flatten:
        # X, Y, C, F -> X, Y, F, C
        axes = list(range(0, len(new_weights.shape)))
        assert len(axes) > 1
        axes[-2], axes[-1] = axes[-1], axes[-2]
        new_weights = np.transpose(new_weights, axes)
    else:
        # Expand dims to allow broadcasting on the expected dimension
        rescaling_rate = np.expand_dims(rescaling_rate, -1)

    # Apply rescaling rate
    new_weights /= rescaling_rate

    # Undo reshape ops
    if reshape_ops:
        # Revert last dimensions swap, eg. for Flatten: X, Y, F, C -> X, Y, C, F
        new_weights = np.transpose(new_weights, axes)
        # Undo the reshape op on weights when last dimension is changed, eg. for Flatten:
        # X, Y, C, F -> X*Y*C, F
        if reshape_ops[0][-1] != reshape_ops[1][-1]:
            F = (new_weights.shape[-1], )
            new_weights = np.reshape(new_weights, reshape_ops[1] + F)

    next_weights[0] = new_weights
    next_layer.set_weights(next_weights)


def calibrate(model, qmodel, samples=None, num_samples=1024, batch_size=None, epochs=1):
    """Calibrates the model using the provided samples.

    When no samples are provided, random samples are generated.

    Args:
        model (keras.Model): the original model
        qmodel (keras.Model): the quantized model to calibrate
        samples (tf.Dataset, np.array or generator, optional): calibration samples. When no samples
            are provided, random samples are generated. Defaults to None.
        num_samples (int, optional): number of samples to use in the provided samples or number of
            samples to generate. Defaults to 1024.
        batch_size (int, optional): the batch size. Defaults to None.
        epochs (int, optional): the number of epochs. Defaults to 1.

    """
    if not calibration_required(qmodel):
        return

    # Build a calibration model which is a float model with OutputObservers at locations where the
    # quantized model has OutputQuantizers.
    calibration_model, end_of_blocks = _get_calibration_model(model, qmodel)

    if samples is None:
        # Generate random samples
        samples_shape = (num_samples, ) + qmodel.input_shape[1:]

        # Handle image like samples (channels in [1, 3]) as uint8 and other as int8
        if samples_shape[-1] in [1, 3]:
            samples = np.random.randint(0, 255, size=samples_shape).astype(np.uint8)
        else:
            samples = np.random.randint(-128, 127, size=samples_shape).astype(np.int8)

    # Compute step value otherwise 'predict' will run until samples are exhausted (ie. indefinitely
    # if samples is a dataset with repeat enabled)
    if batch_size is None:
        steps = num_samples
    else:
        assert batch_size > 0, "The batch size should be strictly positive."
        steps = np.ceil(num_samples / batch_size)

    # Forward samples into the calibration model which will update the range_max in OutputObservers
    for _ in range(epochs):
        calibration_model.predict(x=samples, steps=steps, batch_size=batch_size)

    # Update quantized model OutputQuantizers range_max using OutputObservers calibrated values
    for eob, observer in end_of_blocks.items():
        _set_and_equalize(qmodel, eob, calibration_model.get_layer(observer).range_max)
