# Stable Modules:
import jax
import numpy as np
from jax import (jit,
                 numpy as jnp)
from jax.random import PRNGKey
from jaxtyping import Array
from random import randint
from typing import (Any,
                    Tuple,
                    final)

# Custom built Modules:
import tensorwrap as tf
from ...module import Module
from ...nn.initializers import (GlorotNormal,
                                GlorotUniform, 
                                Initializer,
                                Zeros)

__all__ = ["Layer", "Dense"]

# Custom Trainable Layer


class Layer(Module):
    """A base layer class that is used to create new JIT enabled layers.
       Acts as the subclass for all layers, to ensure that they are converted in PyTrees."""

    _name_tracker: int = 1

    def __init__(self, name: str = "Layer") -> None:
        self.built = False
        self.trainable_variables = {}
        # Name Handling:
        self.name = name + ":" + str(Layer._name_tracker)
        self.id = Layer._name_tracker
        Layer._name_tracker += 1

    def add_weights(self, shape: Tuple[int, ...], key = PRNGKey(randint(1, 1000)), initializer:Initializer = GlorotNormal(), name = 'unnamed weight', trainable=True):
        """Useful method inherited from layers.Layer that adds weights that can be trained.
        ---------
        Arguments:
            - shape: Shape of the inputs and the units
            - initializer: The initial values of the weights
            - name: The name of the weight.
            - trainable (Optional) - Not required or implemented yet. """
        
        weight = initializer(shape)

        # Adding to the trainable variables:
        if trainable:
            self.trainable_variables[name] = weight

        return weight

    def build(self, inputs):
        pass

    def init_params(self, inputs):
        self.build(inputs)
        self.built=True
        return self.trainable_variables

    def compute_output_shape(self):
        raise NotImplementedError("Method `compute_output_shape` has not been implemented.")

    
    @final
    def __call__(self, params: dict, inputs: Array):
        if not self.built:
            self.init_params(inputs)
            params = self.trainable_variables
        out = self.call(params, inputs)
        return out
    
    
    def call(self, params: dict, inputs: Array):
        raise NotImplementedError("Call Method Missing:\nPlease define the control flow in the call method.")


    # Displaying the names:
    def __repr__(self) -> str:
        return f"<tf.{self.name}>"


# Dense Layer:

class Dense(Layer):
    """ A fully connected layer that applies linear transformation to the inputs.
    ---------
    Arguments:
        - units (int): A positive integer representing the output shape.
        - activation (Optional, str or Activation): Activation function to use. Defaults to None.
        - use_bias (Optional, bool): A boolean signifying whether to include a bias term.
        - kernel_initializer (Optional, str or Initializer): An initializer function that returns 
    """


    def __init__(self,
                 units: int,
                 use_bias: bool = True,
                 kernel_initializer: Initializer = GlorotUniform(),
                 bias_initializer: Initializer = Zeros()):
        super().__init__()
        self.units = units
        self.use_bias = use_bias
        self.kernel_initializer = kernel_initializer
        self.bias_initializer = bias_initializer

    def build(self, inputs):
        self.input_shape = tf.shape(inputs)
        self.kernel = self.add_weights(shape = (self.input_shape[-1], self.units),
                                       initializer = self.kernel_initializer,
                                       name = "kernel")
        if self.use_bias:
            self.bias = self.add_weights(shape = (self.units,),
                                         initializer = self.bias_initializer,
                                         name="bias")
        else:
            self.bias = None
            self.trainable_variables['bias'] = self.bias


    @staticmethod
    @jax.jit
    def call(params: dict, inputs: Array) -> Array:
        if params['bias'] is None:
            return inputs @ params['kernel']
        
        x = inputs @ params['kernel'] + params['bias']
        return x
    


# Inspection Fixes:
Layer.__module__ = "tensorwrap.nn.layers"
Dense.__module__ = "tensorwrap.nn.layers"

