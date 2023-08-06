from __future__ import annotations

from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Protocol,
    Sized,
    Tuple,
    Type,
    TypeVar,
    no_type_check,
)

import clu.metrics
import clu.periodic_actions
from absl import logging
from flax import struct
from flax.core import frozen_dict
from flax.training import early_stopping, train_state
from jaxtyping import Array, Float, Int, Key, jaxtyped
from keras.utils.generic_utils import Progbar

from absl_extra.jax_utils import prefetch_to_device

T = TypeVar("T", contravariant=True)
TS = TypeVar("TS", bound=train_state.TrainState, contravariant=True)
M = TypeVar("M", bound=clu.metrics.Collection, contravariant=True)
DatasetFactory = Callable[[], Iterable[Tuple[T, Int[Array, "batch classes"]]]]  # noqa


@struct.dataclass
class NanSafeAverage(clu.metrics.Average):
    def compute(self) -> float:
        if self.count == 0:
            return 0
        return super().compute()


class ApplyFn(Protocol[T]):
    def __call__(
        self,
        params: Dict[str, frozen_dict.FrozenDict],
        x_batch: T,
        train: bool = False,
        rngs: Dict[str, Key] | None = None,
        **kwargs,
    ) -> Float[Array, "batch classes"]:  # noqa
        ...


class TrainingHook(Protocol[TS, M]):
    def __call__(
        self,
        step: int,
        *,
        training_state: TS,
        training_metrics: M,
        **kwargs,
    ) -> None:
        ...


class ValidationHook(Protocol[M]):
    def __call__(
        self,
        step: int,
        *,
        validation_metrics: M,
        **kwargs,
    ) -> None:
        ...


class UncheckedReportProgress(clu.periodic_actions.ReportProgress):
    def __call__(self, step: int, **kwargs) -> bool:
        return super().__call__(int(step))

    @no_type_check
    def _init_and_check(self, step: int, t: float):
        """Initializes and checks it was called at every step."""
        if self._previous_step is None:
            self._previous_step = step
            self._previous_time = t
            self._last_step = step
        else:
            self._last_step = step


class UncheckedPeriodicCallback(clu.periodic_actions.PeriodicCallback):
    def __call__(self, step: int, *args, **kwargs) -> bool:
        return super().__call__(int(step), *args, **kwargs)

    @no_type_check
    def _init_and_check(self, step: int, t: float):
        """Initializes and checks it was called at every step."""
        if self._previous_step is None:
            self._previous_step = step
            self._previous_time = t
            self._last_step = step
        else:
            self._last_step = step


def save_as_msgpack(
    params: frozen_dict.FrozenDict, save_path: str = "model.msgpack"
) -> None:
    """
    Parameters
    ----------
    params : frozen_dict.FrozenDict
        The frozen dictionary object that contains the parameters to be saved.
    save_path : str, optional
        The file path where the msgpack file will be saved. Default is "model.msgpack".

    Returns
    -------
    None
        This method does not return any value.
    """
    logging.info(f"Writing {save_path}")
    msgpack_bytes: bytes = frozen_dict.serialization.to_bytes(params)
    with open(save_path, "wb+") as file:
        file.write(msgpack_bytes)


def load_from_msgpack(
    params: frozen_dict.FrozenDict, save_path: str = "model.msgpack"
) -> frozen_dict.FrozenDict:
    """
    Load model parameters from a msgpack file.

    Parameters
    ----------
    params : frozen_dict.FrozenDict
        The original parameters of the model.
    save_path : str, optional
        The path to the msgpack file containing the serialized parameters.
        Default is "model.msgpack".

    Returns
    -------
    params : frozen_dict.FrozenDict
        The loaded parameters.

    """
    logging.info(f"Reading {save_path}")

    with open(save_path, "rb") as file:
        bytes_data = file.read()

    params = frozen_dict.serialization.from_bytes(params, bytes_data)

    return params


class InvalidEpochsNumberError(RuntimeError):
    def __init__(self, value: int):
        super().__init__(f"Epochs must be greater than 0, but found {value}")


class MissingSizeError(RuntimeError):
    def __init__(self, size_key: str = "size"):
        super().__init__(f"Must provide {size_key}, for not sized iterable.")


@jaxtyped
def train_on_single_device(
    *,
    training_state: TS,
    training_dataset_factory: DatasetFactory,
    validation_dataset_factory: DatasetFactory,
    metrics_container_type: Type[M],
    # fmt: off
    training_step_func: Callable[[TS, T, Int[Array, "batch classes"]], Tuple[TS, M]], # noqa
    validation_step_func: Callable[[TS, T, Int[Array, "batch classes"]], M], # noqa
    # fmt: on
    training_hooks: List[TrainingHook[TS, M]] | None = None,
    validation_hooks: List[ValidationHook[M]] | None = None,
    epochs: int = 1,
    prefetch_buffer_size: int = 2,
    verbose: bool = False,
    num_training_steps: int | None = None,
) -> Tuple[Tuple[Dict[str, float], Dict[str, float]], frozen_dict.FrozenDict]:
    """
    Parameters
    ----------
    training_state : TS
        The initial state of the training process.
    training_dataset_factory : DatasetFactory
        A factory function that returns the training dataset.
    validation_dataset_factory : DatasetFactory
        A factory function that returns the validation dataset.
    metrics_container_type : Type[M]
        The type of container to store the metrics.
    training_step_func : Callable[[TS, T, Int[Array, "batch classes"]], Tuple[TS, M]]
        A function that performs a single training step. It takes the training state, input data, and target data as inputs,
        and returns the updated training state and metrics.
    validation_step_func : Callable[[TS, T, Int[Array, "batch classes"]], M]
        A function that performs a single validation step. It takes the training state, input data, and target data as inputs,
        and returns the metrics.
    training_hooks : List[TrainingHook[TS, M]] | None, optional
        A list of training hooks to be executed after each training step. Defaults to None.
    validation_hooks : List[ValidationHook[M]] | None, optional
        A list of validation hooks to be executed after each validation step. Defaults to None.
    epochs : int, optional
        The number of training epochs. Defaults to 1.
    prefetch_buffer_size : int, optional
        The size of the prefetch buffer for loading data. Defaults to 2.
    verbose : bool, optional
        Whether to display verbose output during training. Defaults to False.
    num_training_steps : int | None, optional
        The total number of training steps. If None, it is calculated based on the size of the training dataset.
        Defaults to None.

    Returns
    -------
    Tuple[Tuple[Dict[str, float], Dict[str, float]], frozen_dict.FrozenDict]
        A tuple containing the training and validation metrics, and the final training state parameters.
    """
    if epochs <= 0:
        raise InvalidEpochsNumberError(epochs)

    if training_hooks is None:
        training_hooks = []
    if validation_hooks is None:
        validation_hooks = []

    if verbose:
        if num_training_steps is None:
            training_dataset = training_dataset_factory()
            if isinstance(training_dataset, Sized):
                num_training_steps = len(training_dataset)
            else:
                raise MissingSizeError("num_training_steps")

    for epoch in range(epochs):
        if verbose:
            logging.info(f"Epoch {epoch+1}/{epochs}...")

        training_dataset = training_dataset_factory()
        if prefetch_buffer_size != 0:
            training_dataset = prefetch_to_device(
                training_dataset, prefetch_buffer_size
            )

        if verbose:
            logging.debug(f"Training epoch {epoch+1}/{epochs}...")

        training_metrics = metrics_container_type.empty()

        if verbose:
            pbar = Progbar(num_training_steps)

        for x_batch, y_batch in training_dataset:
            training_state, metrics_i = training_step_func(
                training_state, x_batch, y_batch
            )
            training_metrics = training_metrics.merge(metrics_i)

            if verbose:
                pbar.update(
                    int(training_state.step),
                    [
                        (f"train_{k}", float(v))
                        for k, v in training_metrics.compute().items()
                    ],
                )

            for hook in training_hooks:
                hook(
                    training_state.step,
                    training_state=training_state,
                    training_metrics=training_metrics,
                )

        validation_dataset = validation_dataset_factory()
        if prefetch_buffer_size != 0:
            validation_dataset = prefetch_to_device(
                validation_dataset, prefetch_buffer_size
            )
        validation_metrics = metrics_container_type.empty()

        for x_batch, y_batch in validation_dataset:
            metrics_i = validation_step_func(training_state, x_batch, y_batch)
            validation_metrics = validation_metrics.merge(metrics_i)

        if verbose:
            pbar.update(
                int(training_state.step),
                [
                    (f"val_{k}", float(v))
                    for k, v in validation_metrics.compute().items()
                ],
            )

        for val_hook in validation_hooks:
            val_hook(training_state.step, validation_metrics=validation_metrics)

            if isinstance(val_hook, early_stopping.EarlyStopping):
                if val_hook.should_stop:
                    break

    return (
        training_metrics.compute(),  # noqa
        validation_metrics.compute(),  # noqa
    ), training_state.params
