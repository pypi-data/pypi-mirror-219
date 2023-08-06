from jax import (numpy as np,
                 jit,
                 Array)

import random
import jax

@jit
def last_dim(array: Array):
    r"""Returns the last dimension of the array, list, or integer. Used internally for Dense Layers and Compilations.
    
    Arguments:
        array (Array): Array for size computation
    """
    try:
        return np.shape(array)[-1]
    except:
        return array


def randu(shape, key = jax.random.PRNGKey(random.randint(1, 5))):
    return jax.random.uniform(key, shape, dtype=np.float32)


def randn(shape, key = jax.random.PRNGKey(random.randint(1, 5))):
    return jax.random.normal(key, shape, dtype=np.float32)