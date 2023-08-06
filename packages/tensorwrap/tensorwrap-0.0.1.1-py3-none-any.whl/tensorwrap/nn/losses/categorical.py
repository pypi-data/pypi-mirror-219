from tensorwrap.core.losses import _SparseCategoricalCrossentropy
from tensorwrap.nn.losses import Loss
import jax

class SparseCategoricalCrossentrophy(Loss):
    def __init__(self, from_logits = False) -> None:
        super().__init__()
        self.from_logits = from_logits

    def call(self, labels, logits):
        if self.from_logits:
            jax.nn.softmax(logits)
        
        return _SparseCategoricalCrossentropy(logits, labels)
