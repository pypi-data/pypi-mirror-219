import tensorwrap as tf
from jax import jit
from tensorwrap.core.losses import (_mse,
                                    _mae)

__all__ = ["mse", "mae"]

def mse(y_true, y_pred):
    """Calculates the mean square error of the predictions with respect to the true values."""
    try:
        return _mse(y_true, y_pred)
    except:
        tf.mean(tf.square(y_pred - y_true))


def mae(y_true, y_pred):
    try:
        return _mae(y_true, y_pred)
    except:
        return tf.mean(tf.abs(y_pred - y_true))


# Inspection Fixes:
mse.__module__ = "tensowrap.nn.losses"
mae.__module__ = "tensorwrap.nn.losses"


# Adding proper names:
mse.__repr__ = "<function mse>"
mae.__repr__ = "<function mae>"