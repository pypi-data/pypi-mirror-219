import jax
from jax import numpy as jnp

__all__ = ['_mse', '_mae']

@jax.jit
def _mse(y_true, y_pred):
    """Hidden Implementation of mse."""
    return jnp.mean(jnp.square(y_pred - y_true))

@jax.jit
def _mae(y_true, y_pred):
    return jnp.mean(jnp.abs(y_pred - y_true))