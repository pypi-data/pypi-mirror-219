from enum import Enum
from typing import Dict, List, Optional

import numpy
import pydantic
from pydantic import PositiveInt

from classiq.interface.backend.quantum_backend_providers import (
    AnalyzerProviderVendor,
    ProviderVendor,
)
from classiq.interface.chemistry.ground_state_problem import MoleculeProblem
from classiq.interface.executor.optimizer_preferences import OptimizerPreferences
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString


class AnalysisParams(pydantic.BaseModel):
    qasm: PydanticNonEmptyString


class HardwareListParams(pydantic.BaseModel):
    devices: Optional[List[PydanticNonEmptyString]] = pydantic.Field(
        default=None, description="Devices"
    )
    providers: List[AnalyzerProviderVendor]

    @pydantic.validator("providers", always=True)
    def set_default_providers(cls, providers: Optional[List[AnalyzerProviderVendor]]):
        if providers is None:
            providers = list(AnalyzerProviderVendor)
        return providers


class AnalysisOptionalDevicesParams(HardwareListParams):
    qubit_count: int = pydantic.Field(
        default=..., description="number of qubits in the data"
    )


class AnalysisHardwareListParams(AnalysisParams, HardwareListParams):
    pass


class HardwareParams(pydantic.BaseModel):
    device: PydanticNonEmptyString = pydantic.Field(default=None, description="Devices")
    provider: AnalyzerProviderVendor


class AnalysisHardwareParams(AnalysisParams, HardwareParams):
    pass


class CircuitAnalysisHardwareParams(AnalysisParams):
    provider: ProviderVendor
    device: PydanticNonEmptyString


class ComparisonProperties(str, Enum):
    DEPTH = "depth"
    MULTI_QUBIT_GATE_COUNT = "multi_qubit_gate_count"
    TOTAL_GATE_COUNT = "total_gate_count"


class AnalysisComparisonParams(pydantic.BaseModel):
    property: ComparisonProperties = pydantic.Field(
        default=...,
        description="The comparison property used to select the best devices",
    )


class AnalysisRBParams(pydantic.BaseModel):
    hardware: str
    counts: List[Dict[str, int]]
    num_clifford: List[int]


class ChemistryGenerationParams(pydantic.BaseModel):
    molecule: MoleculeProblem = pydantic.Field(
        default=...,
        description="The molecule to generate the VQE ansatz for",
    )
    optimizer_preferences: OptimizerPreferences = pydantic.Field(
        default=..., description="Execution options for the classical Optimizer"
    )
    num_shots: PositiveInt = pydantic.Field(
        description="Number of repetitions of the quantum ansatz.",
    )

    def initial_point(self) -> Optional[numpy.ndarray]:
        if self.optimizer_preferences.initial_point is not None:
            return numpy.ndarray(self.optimizer_preferences.initial_point)  # type: ignore
        else:
            return None
