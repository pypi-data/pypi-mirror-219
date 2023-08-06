from typing import Any
import jax.numpy as jnp
from jax import jit
from ...module import Module

class Lambda(Module):
    """A superclass for layers without trainable variables."""
    def __init__(self) -> None:
        pass

    def __call__(self, *args, **kwargs) -> Any:
        pass

class Flatten(Lambda):
    def __init__(self, input_shape = None) -> None:
        if input_shape is None:
            self.input_shape = -1
        else:
            self.input_shape = jnp.prod(jnp.array(input_shape))

    @jit
    def __call__(self, inputs) -> Any:
        return jnp.reshape(inputs, [inputs.shape[0], self.input_shape])