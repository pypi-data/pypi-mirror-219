from typing import Any, Dict, List, Optional, Union

import numpy as np

from classiq.interface.applications.qsvm import DataList, QSVMData, QSVMPreferences
from classiq.interface.backend.backend_preferences import IBMBackendPreferences
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.qsvm import (
    FeatureMapType,
    QSVMFeatureMapBlochSphere,
    QSVMFeatureMapPauli,
)

from classiq import GeneratedCircuit
from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import Asyncify
from classiq.applications import numpy_utils
from classiq.exceptions import ClassiqQSVMError, ClassiqValueError

Data = Union[DataList, np.ndarray]
Labels = Union[List[Any], np.ndarray]
FeatureMap = Union[FeatureMapType, str, List[str]]

_DEFAULT_EXECUTION_PREFERENCES = ExecutionPreferences(
    num_shots=1024,
    backend_preferences=IBMBackendPreferences(backend_name="aer_simulator"),
    random_seed=1234,
)


class QSVM(metaclass=Asyncify):
    def __init__(
        self,
        feature_map: Optional[FeatureMap] = None,
        generated_circuit: Optional[GeneratedCircuit] = None,
        train_data: Optional[Data] = None,
        train_labels: Optional[Labels] = None,
        test_data: Optional[Data] = None,
        test_labels: Optional[Labels] = None,
        predict_data: Optional[Data] = None,
        preferences: Optional[QSVMPreferences] = None,
        **preferences_kwargs,
    ):
        if generated_circuit is None and feature_map is not None:
            self._set_feature_map(feature_map)
            self.generated_circuit = None
        elif feature_map is None and generated_circuit is not None:
            self.generated_circuit = generated_circuit
            self._feature_map = None
        else:
            raise ClassiqValueError(
                "Exactly one of feature_map or generated_circuit can be provided"
            )

        self._train_data = train_data
        self._train_labels = train_labels
        self._test_data = test_data
        self._test_labels = test_labels
        self._predict_data = predict_data
        self._result: dict = {}

        self._set_preferences(preferences, preferences_kwargs)

        labels = numpy_utils.choose_first(self._train_labels, self._test_labels)
        if labels is not None:
            self._generate_label_map(labels)

    def _set_feature_map(self, feature_map: FeatureMap) -> None:
        if isinstance(feature_map, FeatureMapType.__args__):  # type: ignore[attr-defined]
            self._feature_map = feature_map
        elif isinstance(feature_map, str):
            if feature_map == "bloch_sphere":
                self._feature_map = QSVMFeatureMapBlochSphere()  # type: ignore[assignment]
            elif feature_map == "pauli":
                self._feature_map = QSVMFeatureMapPauli()  # type: ignore[assignment]
            else:
                raise ClassiqValueError(
                    'Invalid feature map entered. Please enter either "bloch_sphere" or a list of pauli operators'
                )
        elif isinstance(feature_map, list):
            self._feature_map = QSVMFeatureMapPauli(paulis=feature_map)  # type: ignore[assignment]
        else:
            raise ClassiqValueError(
                'Invalid feature map entered. Please enter either "bloch_sphere" or a list of pauli operators'
            )

    def _set_preferences(
        self, preferences: Optional[QSVMPreferences], preferences_kwargs: dict
    ):
        if preferences is not None:
            self.preferences = preferences
        else:
            if "execution_preferences" not in preferences_kwargs:
                preferences_kwargs[
                    "execution_preferences"
                ] = _DEFAULT_EXECUTION_PREFERENCES

            self.preferences = QSVMPreferences(**preferences_kwargs)

    def _generate_label_map(self, labels: Labels) -> None:
        self._label_to_int_map: Dict[Any, int] = {
            label: index for index, label in enumerate(sorted(set(labels)))
        }
        self._int_to_label_map: Dict[int, Any] = {
            index: label for index, label in enumerate(sorted(set(labels)))
        }

    def _label_to_int(self, labels: Labels) -> List[int]:
        if not hasattr(self, "_label_to_int_map"):
            self._generate_label_map(labels)

        return [self._label_to_int_map[i] for i in labels]

    def _int_to_label(self, ints: List[int]) -> List[Any]:
        if not hasattr(self, "_int_to_label_map"):
            raise ClassiqValueError(
                "Unable to translate int to label without conversion map"
            )

        return [self._int_to_label_map[i] for i in ints]

    async def run_async(
        self,
        train_data: Optional[Data] = None,
        train_labels: Optional[Labels] = None,
        test_data: Optional[Data] = None,
        test_labels: Optional[Labels] = None,
        predict_data: Optional[Data] = None,
        preferences: Optional[QSVMPreferences] = None,
        **preferences_kwargs,
    ) -> dict:
        if preferences or preferences_kwargs:
            self._set_preferences(preferences, preferences_kwargs)

        self._train_data = numpy_utils.choose_first(train_data, self._train_data)
        self._train_labels = numpy_utils.choose_first(train_labels, self._train_labels)
        if numpy_utils.bool_data(self._train_data, self._train_labels):
            await self.train_async()

        self._test_data = numpy_utils.choose_first(test_data, self._test_data)
        self._test_labels = numpy_utils.choose_first(test_labels, self._test_labels)
        if numpy_utils.bool_data(self._test_data, self._test_labels):
            await self.test_async()

        self._predict_data = numpy_utils.choose_first(predict_data, self._predict_data)
        if numpy_utils.bool_data(self._predict_data):
            await self.predict_async()

        return self._result

    def _get_data(self, *data_objects) -> Any:
        data = numpy_utils.choose_first(*data_objects)
        if not numpy_utils.bool_data(data):
            raise ClassiqValueError("Empty data was supplied")
        return data

    def _get_labels(self, *labels_objects) -> Any:
        labels = numpy_utils.choose_first(*labels_objects)
        if not numpy_utils.bool_data(labels):
            raise ClassiqValueError("Empty labels was supplied")
        return labels

    async def train_async(
        self, data: Optional[Data] = None, labels: Optional[Labels] = None
    ) -> None:
        self._internal_state = await ApiWrapper().call_qsvm_train(
            self._prepare_qsvm_data(
                self._get_data(data, self._train_data),
                self._get_labels(labels, self._train_labels),
            )
        )

    async def test_async(
        self, data: Optional[Data] = None, labels: Optional[Labels] = None
    ) -> float:
        self._validate_trained("test")

        result = await ApiWrapper().call_qsvm_test(
            self._prepare_qsvm_data(
                self._get_data(data, self._test_data),
                self._get_labels(labels, self._test_labels),
            )
        )
        self.accuracy = result.data
        self._result["accuracy"] = result.data

        return self.accuracy

    async def predict_async(self, data: Optional[Data] = None) -> np.ndarray:
        self._validate_trained("predict")

        result = await ApiWrapper().call_qsvm_predict(
            self._prepare_qsvm_data(self._get_data(data, self._predict_data))
        )
        self._result["predicted_labels"] = np.array(self._int_to_label(result.data))
        return self._result["predicted_labels"]

    def _validate_feature_map(self, data: Data):
        if self._feature_map is not None:
            # if unset, set it
            if self._feature_map.feature_dimension is None:  # type: ignore[unreachable]
                self._feature_map = self._feature_map.copy(
                    update={"feature_dimension": len(data[0])}
                )

            # this will only happen if it was already set, and an invalid data was given
            if len(data[0]) != self._feature_map.feature_dimension:
                raise ClassiqQSVMError(
                    "The shape of the data is incompatible with the feature map"
                )
        else:
            pass  # When Generated Circuit is used, feature dimension is not relevant

    def _prepare_qsvm_data(
        self, data: Data, labels: Optional[Labels] = None
    ) -> QSVMData:
        self._validate_feature_map(data)

        kwargs = {
            "data": data,
            "feature_map": self._feature_map,
            "preferences": self.preferences,
        }

        if hasattr(self, "_internal_state"):
            kwargs["internal_state"] = self._internal_state  # type: ignore[assignment]

        if labels is not None:
            kwargs["labels"] = self._label_to_int(labels)  # type: ignore[assignment]

        return QSVMData(**kwargs)

    @property
    def _is_trained(self) -> bool:
        return hasattr(self, "_internal_state")

    def _validate_trained(self, s="use") -> None:
        if not self._is_trained:
            raise ClassiqQSVMError(f"Cannot {s} QSVM on an un-trained model")


__all__ = [
    "QSVM",
    "QSVMData",
    "QSVMPreferences",
]


def __dir__():
    return __all__
