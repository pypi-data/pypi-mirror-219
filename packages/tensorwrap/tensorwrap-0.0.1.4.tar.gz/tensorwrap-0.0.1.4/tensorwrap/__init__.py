""" TensorWrap's initial API. This API contains various frontend functions that are
used to manipulate tensors and various data. However, most of the API currently borrows
from JAX's built-in operations. For neural networks, please use the Keras API or import
the Torch API to use PyTorch variants."""

# Error Silencer:
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Library Paths:
from tensorwrap import nn
from tensorwrap import test
from tensorwrap import config
from tensorwrap import experimental

# Path Shortener:
from tensorwrap.module import Module
from tensorwrap.version import __version__
from tensorwrap.experimental.serialize import save_model, load_model
from tensorwrap.experimental.wrappers import function
from tensorwrap.ops import (last_dim,
                            randu,
                            randn)

# JAX Built-ins:
from jax import (disable_jit,
                 value_and_grad,
                 grad,
                 vmap as vectorized_map)
from jax.numpy import (array as tensor,
                       arange as range,
                       expand_dims,
                       matmul,
                       square,
                       abs,
                       mean,
                       sum,
                       reshape,
                       float16,
                       float32,
                       float64,
                       eye as identity,
                       shape,
                       prod,
                       max,
                       min,
                       maximum,
                       minimum,
                       zeros,
                       argmax,
                       argmin)