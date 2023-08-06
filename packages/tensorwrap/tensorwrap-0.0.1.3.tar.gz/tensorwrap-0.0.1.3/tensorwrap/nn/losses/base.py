"""This module aims to provide a workable subclass for all the loss functions."""

import tensorwrap as tf
from tensorwrap.module import Module

class Loss(Module):

    def __init__(self) -> None:
        super().__init__()
        pass

    def call(self, *args, **kwargs):
        pass
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)