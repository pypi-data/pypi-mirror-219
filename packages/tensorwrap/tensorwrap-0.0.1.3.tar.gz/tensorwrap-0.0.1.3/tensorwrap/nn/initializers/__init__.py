from typing import Any
import tensorwrap as tf

class Initializer:
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


class GlorotUniform(Initializer):
    def __init__(self) -> None:
        pass

    def __call__(self, shape):
        return tf.randu(shape)


class GlorotNormal(Initializer):
    def __init__(self) -> None:
        pass

    def __call__(self, shape):
        return tf.randn(shape)


class Zeros(Initializer):
    def __init__(self) -> None:
        pass

    def __call__(self, shape):
        return tf.zeros(shape)