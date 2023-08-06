import enum
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import pydantic
from typing_extensions import TypeAlias

from classiq.interface.backend.backend_preferences import BackendPreferences
from classiq.interface.backend.quantum_backend_providers import ProviderVendor
from classiq.interface.executor import quantum_program
from classiq.interface.executor.quantum_instruction_set import QuantumInstructionSet
from classiq.interface.executor.register_initialization import RegisterInitialization
from classiq.interface.generator.generated_circuit_data import GeneratedCircuitData
from classiq.interface.generator.model.model import SynthesisModel
from classiq.interface.generator.model.preferences.preferences import (
    CustomHardwareSettings,
    QuantumFormat,
)
from classiq.interface.generator.synthesis_metadata.synthesis_duration import (
    SynthesisStepDurations,
)
from classiq.interface.helpers.versioned_model import VersionedModel

from classiq.exceptions import (
    ClassiqMissingOutputFormatError,
    ClassiqStateInitializationError,
)

_MAXIMUM_STRING_LENGTH = 250

Code: TypeAlias = str
CodeAndSyntax: TypeAlias = Tuple[Code, QuantumInstructionSet]
RegisterName: TypeAlias = str
InitialConditions: TypeAlias = Dict[RegisterName, int]

_INSTRUCTION_SET_TO_FORMAT: Dict[QuantumInstructionSet, QuantumFormat] = {
    QuantumInstructionSet.QASM: QuantumFormat.QASM,
    QuantumInstructionSet.QSHARP: QuantumFormat.QSHARP,
    QuantumInstructionSet.IONQ: QuantumFormat.IONQ,
}
_VENDOR_TO_INSTRUCTION_SET: Dict[str, QuantumInstructionSet] = {
    ProviderVendor.IONQ: QuantumInstructionSet.IONQ,
    ProviderVendor.AZURE_QUANTUM: QuantumInstructionSet.QSHARP,
    ProviderVendor.IBM_QUANTUM: QuantumInstructionSet.QASM,
    ProviderVendor.NVIDIA: QuantumInstructionSet.QASM,
    ProviderVendor.AMAZON_BRAKET: QuantumInstructionSet.QASM,
}
_DEFAULT_INSTRUCTION_SET = QuantumInstructionSet.QASM


class LongStr(str):
    def __repr__(self):
        if len(self) > _MAXIMUM_STRING_LENGTH:
            length = len(self)
            return f'"{self[:4]}...{self[-4:]}" (length={length})'
        return super().__repr__()


class QasmVersion(str, enum.Enum):
    V2 = "2.0"
    V3 = "3.0"


class HardwareData(pydantic.BaseModel):
    _is_default: bool = pydantic.PrivateAttr(default=False)
    custom_hardware_settings: CustomHardwareSettings
    backend_preferences: Optional[BackendPreferences]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._is_default = (
            self.custom_hardware_settings.is_default
            and self.backend_preferences is None
        )

    @property
    def is_default(self) -> bool:
        return self._is_default


class CircuitWithOutputFormats(pydantic.BaseModel):
    outputs: Dict[QuantumFormat, Code]
    qasm_version: QasmVersion

    @pydantic.validator("outputs")
    def reformat_long_string_output_formats(
        cls, outputs: Dict[QuantumFormat, str]
    ) -> Dict[QuantumFormat, LongStr]:
        return {key: LongStr(value) for key, value in outputs.items()}

    @property
    def qasm(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.QASM)

    @property
    def qsharp(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.QSHARP)

    @property
    def qir(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.QIR)

    @property
    def ionq(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.IONQ)

    @property
    def cirq_json(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.CIRQ_JSON)

    @property
    def qasm_cirq_compatible(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.QASM_CIRQ_COMPATIBLE)

    @property
    def cudaq_json(self) -> Optional[Code]:
        return self.outputs.get(QuantumFormat.CUDAQ_JSON)

    @property
    def output_format(self) -> List[QuantumFormat]:
        return list(self.outputs.keys())


class TranspiledCircuitData(CircuitWithOutputFormats):
    depth: int
    count_ops: Dict[str, int]
    logical_to_physical_input_qubit_map: List[int]
    logical_to_physical_output_qubit_map: List[int]


class GeneratedCircuit(VersionedModel, CircuitWithOutputFormats):
    data: GeneratedCircuitData
    transpiled_circuit: Optional[TranspiledCircuitData]
    hardware_data: HardwareData
    creation_time: str = pydantic.Field(default_factory=datetime.utcnow().isoformat)
    synthesis_duration: Optional[SynthesisStepDurations]
    model: SynthesisModel
    interactive_html: Optional[str]
    analyzer_data: Dict
    initial_values: Optional[InitialConditions]

    def save_results(self, filename: Optional[Union[str, Path]] = None) -> None:
        """
        Saves generated circuit results as json.
            Parameters:
                filename (Union[str, Path]): Optional, path + filename of file.
                                             If filename supplied add `.json` suffix.

            Returns:
                  None
        """
        if filename is None:
            filename = f"synthesised_circuit_{self.creation_time}.json"

        with open(filename, "w") as file:
            file.write(self.json(indent=4))

    @staticmethod
    def _get_code_by_priority_from_outputs(
        outputs: Dict[QuantumFormat, Code]
    ) -> Optional[CodeAndSyntax]:
        for instruction_set, quantum_format in _INSTRUCTION_SET_TO_FORMAT.items():
            code = outputs.get(quantum_format)
            if code is not None:
                return code, instruction_set

        return None

    def _hardware_unaware_program_code(self) -> CodeAndSyntax:
        if self.transpiled_circuit:
            transpiled_circuit_code = self._get_code_by_priority_from_outputs(
                self.transpiled_circuit.outputs
            )
            if transpiled_circuit_code is not None:
                return transpiled_circuit_code

        circuit_code = self._get_code_by_priority_from_outputs(self.outputs)
        if circuit_code is not None:
            return circuit_code

        raise ClassiqMissingOutputFormatError(
            missing_formats=list(_INSTRUCTION_SET_TO_FORMAT.values())
        )

    def _default_program_code(self) -> CodeAndSyntax:
        if self.hardware_data.backend_preferences is None:
            return self._hardware_unaware_program_code()

        backend_provider = (
            self.hardware_data.backend_preferences.backend_service_provider
        )
        instruction_set: QuantumInstructionSet = _VENDOR_TO_INSTRUCTION_SET.get(
            backend_provider, _DEFAULT_INSTRUCTION_SET
        )
        return self._get_code(instruction_set), instruction_set

    def _get_code(self, instruction_set: QuantumInstructionSet) -> Code:
        quantum_format: QuantumFormat = _INSTRUCTION_SET_TO_FORMAT[instruction_set]
        code = (
            self.transpiled_circuit.outputs.get(quantum_format)
            if self.transpiled_circuit
            else self.outputs.get(quantum_format)
        )
        if code is None:
            raise ClassiqMissingOutputFormatError(missing_formats=[quantum_format])
        return code

    def to_base_program(self) -> quantum_program.QuantumBaseProgram:
        code, syntax = self._default_program_code()
        return quantum_program.QuantumBaseProgram(code=code, syntax=syntax)

    def to_program(
        self,
        initial_values: Optional[InitialConditions] = None,
        instruction_set: Optional[QuantumInstructionSet] = None,
    ) -> quantum_program.QuantumProgram:
        initial_values = initial_values or self.initial_values

        if instruction_set is not None:
            code, syntax = self._get_code(instruction_set), instruction_set
        else:
            code, syntax = self._default_program_code()

        if initial_values is not None:
            registers_initialization = self.get_registers_initialization(
                initial_values=initial_values
            )
        else:
            registers_initialization = None
        return quantum_program.QuantumProgram(
            code=code,
            syntax=syntax,
            output_qubits_map=self.data.qubit_mapping.physical_outputs,
            registers_initialization=registers_initialization,
        )

    def _get_initialization_qubits(self, name: str) -> Tuple[int, ...]:
        qubits = self.data.qubit_mapping.logical_inputs.get(name)
        if qubits is None:
            raise ClassiqStateInitializationError(
                f"Cannot initialize register {name}, it does not appear in circuit inputs"
            )
        return qubits

    def get_registers_initialization(
        self, initial_values: InitialConditions
    ) -> Dict[RegisterName, RegisterInitialization]:
        return {
            name: RegisterInitialization(
                name=name,
                qubits=list(self._get_initialization_qubits(name)),
                initial_condition=init_value,
            )
            for name, init_value in initial_values.items()
        }

    @pydantic.validator("interactive_html")
    def reformat_long_strings(cls, v):
        if v is None:
            return v
        return LongStr(v)
