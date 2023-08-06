import jax
import tensorwrap as tf
from ...module import Module

class Dataset(Module):
    def __init__(self, data) -> None:
        self.data = tf.tensor(data)
    
    def batch(self, batch_size, drop_remainder = True):
        num_batches = len(self.data)//batch_size
        batched_data = jax.numpy.array([self.data[i * batch_size: (i + 1) * batch_size] for i in range(num_batches)])
        return Dataset(batched_data)
    
    def map(self, function):
        new_data = jax.numpy.array([function(i) for i in self.data])
        return new_data

    def vmap(self, function):
        """The vectorized version of map that works well for most arrays."""
        new_data = jax.vmap(function)(self.data)
        return Dataset(new_data)
    
    def first(self):
        for tensor in self.data:
            return tensor
    
    def __iter__(self):
        return iter(self.data)