import jax.numpy as jnp
from jax import jit
from tensorwrap.nn.losses import Loss

class Accuracy(Loss):
    def __init__(self) -> None:
        super().__init__()
        pass
    
    @staticmethod
    @jit
    def __call__(y_true, y_pred, from_logits=True):
        """Computes the accuracy metric.

        Args:
            y_true (jax.numpy.ndarray): The true labels with shape (batch_size,).
            y_pred (jax.numpy.ndarray): The predicted logits or class probabilities with shape (batch_size, num_classes).
            from_logits (bool, optional): Whether the predicted values are logits or class probabilities.
                Defaults to True.

        Returns:
            float: The accuracy value.

        """
        if from_logits:
            y_pred = jnp.argmax(y_pred, axis=-1)

        correct = jnp.sum(y_true == y_pred)
        total = y_true.shape[0]
        return correct / total
