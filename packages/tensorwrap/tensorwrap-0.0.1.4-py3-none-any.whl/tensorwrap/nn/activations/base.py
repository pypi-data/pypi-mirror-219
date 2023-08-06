""" This is the activation's module for TensorWrap"""

import tensorwrap as tf
from tensorwrap.module import Module

__all__ = ["Activation", "ReLU"]

class Activation(Module):
    __layer_tracker = 0
    def __init__(self, name = "activation"):
        self.name = name + str(Activation.__layer_tracker)
        Activation.__layer_tracker += 1
    

    def call(self, inputs):
        raise NotImplementedError("Please implement the call function to define control flow.")


    def __call__(self, inputs):
        return self.call(inputs)

class ReLU(Activation):
    
    __name_tracker = 0

    def __init__(self, 
                 max_value=None,
                 negative_slope = 0,
                 threshold = 0,
                 name = "ReLU"):
        super().__init__(name = name)
        self.max_value = max_value
        self.slope = negative_slope
        self.threshold = threshold
        ReLU.__name_tracker += 1
        if self.max_value is not None and self.max_value < 0:
            raise ValueError("Max_value cannot be negative.")
    

    def call(self, inputs):
        part1 = tf.maximum(0, inputs - self.threshold)
        if self.max_value is not None:
            return tf.minimum(part1, self.max_value)
        else:
            return part1
        
# Inspection Fixes:
Activation.__module__ = "tensorwrap.nn.activations"
ReLU.__module__ = "tensorwrap.nn.activations"