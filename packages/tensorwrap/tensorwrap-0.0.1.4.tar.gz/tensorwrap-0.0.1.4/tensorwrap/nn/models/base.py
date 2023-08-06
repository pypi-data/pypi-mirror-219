# Stable Modules:
import time
import jax
import optax
from jax import numpy as jnp
from typing import (Any,
                    Tuple,
                    final)
from jaxtyping import Array

# Custom built Modules:
import tensorwrap as tf
from tensorwrap.module import Module
from tensorwrap.nn.layers.base import Layer


__all__ = ["Model", "Sequential"]

class Model(Module):
    """A custom module for subclassing for all model classes.

    All subclasses inherits Model attributes, training methods, and layer detection.

    Args:
        name (string): The name of the model.
    """

    _name_tracker = 0

    def __init__(self, name:str = "Model"):
        self.trainable_variables = {}
        self._init = False
        self.name = f"{name}:{Model._name_tracker}"
        Model._name_tracker += 1

    
    def __check_attributes(self, obj: Any):
        """A recursive trainable_variable gatherer.

        Checks each attribute of the object to gather all trainable variables.

        Args:
            obj (Any): The object whose attributes are to be checked.

        NOTE: Private Method.
        """

        if isinstance(obj, tf.nn.layers.Layer):
            self.trainable_variables[obj.name] = obj.trainable_variables
        elif isinstance(obj, list):
            for item in obj:
                if self.__check_attributes(item):
                    return True
        elif isinstance(obj, dict):
            for value in obj.values():
                if self.__check_attributes(value):
                    return True
        elif hasattr(obj, '__dict__'):
            for attr_name, attr_value in obj.__dict__.items():
                if self.__check_attributes(attr_value):
                    return True
        return False


    def init_params(self, inputs: jax.Array):
        """An instance that initiates all the trainable_variables and sets up all the layer inputs.
        
        Returns a dictionary with names and trainable_variables of each trainable_layer.
        
        Args:
            inputs: Jax arrays that are used to determine the input shape and parameters.

        Example::
            >>> model = SubclassedModel() # a subclassed ``Model`` instance
            >>> array = tensorwrap.Variable([...]) # An array with same input shape as the inputs.
            >>> params = model.init_params(array) # Initializes the parameters and input shapes
            >>> # Asserting the equivalence of the returned value and parameters.
            >>> print(params == model.trainable_variables)
            True
        """
        self._init = True
        self.__check_attributes(self)
        self.__call__(self.trainable_variables, inputs)
        self.__check_attributes(self)
        return self.trainable_variables
    
    
    def compile(self,
                loss,
                optimizer,
                metrics = None):
        """An instance method that compiles the model's prebuilt fit method.
        
        Given the loss function, optimizer, metrics, it creates the Optax opt_state and the gradient based loss function as well.

        Args:
            loss: A function or ``tensorwrap.nn.losses.Loss`` subclass that has the arguments (y_true, y_pred) to compute the loss.
            optimizer: An optax optimizer that have been initialized with learning_rate.
            metrics: A function or ``tensorwrap.nn.losses.Loss`` subclass that has arguments (y_true, y_pred) to compute the metric.

        Example::
            >>> model = SubclassedModel() # a subclassed ``Model`` instance
            >>> array = tensorwrap.Variable([...]) # An array with same input shape as the inputs.
            >>> params = model.init_params(array) # Initializes the parameters and input shapes
            >>> # Compiling:
            >>> import optax
            >>> model.compile(
                loss = tensorwrap.nn.losses.mse, # Any loss function available.
                optimizer = optax.adam(learning_rate = 1e-2), # Any optax optimizer available.
                metrics = tensorwrap.nn.losses.mae # Any loss function or custom function needed.
            )
        """

        if not self._init:
            raise NotImplementedError("The model is not initialized using ``self.init_params``.")

        self.loss_fn = loss
        self.optimizer = optimizer
        self.metrics = metrics if metrics is not None else loss
        self._compiled = True

        # Prepping the optimizer:
        self.__opt_state = self.optimizer.init(self.trainable_variables)
        
        def compute_grad(params, x, y):
            y_pred = self.__call__(params, x)
            losses = self.loss_fn(y, y_pred)
            return losses, y_pred

        self._value_and_grad_fn = jax.value_and_grad(compute_grad, has_aux=True)
    
    
    def train_step(self,
                   params,
                   x_train,
                   y_train) -> Tuple[Any, Tuple[int, int]]:
        """ Notes:
            Avoid using when using new loss functions or optimizers.
                - This assumes that the loss function arguments are (y_true, y_pred)."""
        if not self._compiled:
            raise NotImplementedError("The model has not been compiled using ``model.compile``.")
        
        (losses, y_pred), grads = self._value_and_grad_fn(params, x_train, y_train)
        updates, self.__opt_state = self.optimizer.update(grads, self.__opt_state)
        params = optax.apply_updates(params, updates)
        return params, (losses, y_pred)


    def fit(self,
            x_train,
            y_train,
            epochs = 1,
            batch_size=32):
        """ Built-in in training method that updates gradients with minimalistic setup.
        
        Args:
            x_train: The labels array.
            y_train: The targets array.
            epochs: Number of repetition for gradient updates.

        NOTE: Doesn't support batching and requires initiating of parameters and compilation of loss function
        and optimizers.
        """
        if epochs < 1:
            raise ValueError("Epochs must be a positive value.")

        # Batching the data:
        X_train_batched, y_train_batched = tf.experimental.data.Dataset(x_train).batch(batch_size), tf.experimental.data.Dataset(y_train).batch(batch_size)

        batch_num = len(x_train)//batch_size
        update_time = batch_num//20
        prev_loss = "nan"
        prev_acc = "nan"
        metric = tf.randn((batch_num,))
        for epoch in range(1, epochs + 1):
            for index, (x_batch, y_batch) in enumerate(zip(X_train_batched, y_train_batched)):
                self.trainable_variables, (loss, pred) = self.train_step(self.trainable_variables, x_batch, y_batch)
                metric = metric.at[index].set(self.metrics(y_batch, pred))
                if index % (update_time + 1) == 0:
                    prev_loss = loss
                    prev_acc = metric.mean()
                self.__show_loading_animation(epoch, batch_num, index + 1, prev_loss, prev_acc)
            print('\n')
        
    def __show_loading_animation(self, epoch, total_batches, current_batch, loss, metric):
        prefix = f'Epoch {epoch}: '
        length = 30
        filled_length = int(length * current_batch // total_batches)
        bar = '=' * filled_length + '>' + '-' * (length - filled_length - 1)
        print(f'\r{prefix} [{bar}] {current_batch}/{total_batches} \t Loss: {loss} \t metric: {metric}', end='', flush=True)

    def predict(self, x):
        return self.__call__(self.trainable_variables, x)
    
    def evaluate(self, x, y):
        if not self._compiled:
            raise NotImplementedError("The model has not been compiled. Please compile using ``self.compile``.")
        
        pred = self.predict(x)
        metric = self.metrics(y, pred)
        loss = self.loss_fn(y, pred)
        print(f"Epoch 1 \t\t\t Loss: {loss} \t\t\t metric: {metric}")


    def __call__(self, params = None, inputs = None) -> Any:
        if not self._init:
            raise NotImplementedError("The model is not initialized using ``self.init_params``.")

    def __repr__(self) -> str:
        return f"<tf.{self.name}>"


# Sequential models that create Forward-Feed Networks:
class Sequential(Model):
    def __init__(self, layers: list = []) -> None:
        super().__init__()
        self.layers = layers


    def add(self, layer: Layer) -> None:
        self.layers.append(layer)

    
    def __call__(self, params: dict, x: Array) -> Array:
        super().__call__()
        for layer in self.layers:
            if isinstance(layer, Layer):
                x = layer(params[layer.name], x)
            else:
                x = layer(x)
        return x


# Inspection Fixes:
Model.__module__ = "tensorwrap.nn.models"
Sequential.__module__ = "tensorwrap.nn.models"