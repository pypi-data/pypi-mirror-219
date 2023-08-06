from typing import Dict, List, Optional, Tuple, Union

import pydantic
from typing_extensions import TypeAlias

from classiq.interface.generator.arith.register_user_input import RegisterUserInput
from classiq.interface.generator.control_state import ControlState

from classiq.quantum_register import RegisterRole

ParameterName = str
IOQubitMapping: TypeAlias = Dict[str, Tuple[int, ...]]


class QubitMapping(pydantic.BaseModel):
    logical_inputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    logical_outputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_inputs: IOQubitMapping = pydantic.Field(default_factory=dict)
    physical_outputs: IOQubitMapping = pydantic.Field(default_factory=dict)


class GeneratedRegister(pydantic.BaseModel):
    name: str
    role: RegisterRole
    register_type: Optional[RegisterUserInput]
    qubit_indexes_relative: List[int]
    qubit_indexes_absolute: List[int]

    def __len__(self) -> int:
        return self.qubit_indexes_relative.__len__()

    @property
    def width(self) -> int:
        return len(self)


class GeneratedFunction(pydantic.BaseModel):
    name: str
    control_states: List[ControlState]
    registers: List[GeneratedRegister] = list()
    depth: Optional[int]
    width: Optional[int]
    released_auxiliary_qubits: List[int] = list()
    dangling_inputs: Dict[str, GeneratedRegister] = dict()
    dangling_outputs: Dict[str, GeneratedRegister] = dict()

    def __getitem__(self, key: Union[int, str]) -> GeneratedRegister:
        if type(key) is int:
            return self.registers[key]
        if type(key) is str:
            for register in self.registers:
                if key == register.name:
                    return register
        raise KeyError(key)

    def get(self, key: Union[int, str]) -> Optional[GeneratedRegister]:
        try:
            return self.__getitem__(key)
        except KeyError:
            return None


class GeneratedCircuitData(pydantic.BaseModel):
    width: int
    circuit_parameters: List[ParameterName] = pydantic.Field(default_factory=list)
    qubit_mapping: QubitMapping = pydantic.Field(default_factory=QubitMapping)
    generated_functions: List[GeneratedFunction] = pydantic.Field(default_factory=list)
    _function_mapping: Dict[Union[int, str], GeneratedFunction] = pydantic.PrivateAttr(
        default_factory=dict
    )

    def _fill_function_mapping(self) -> None:
        if self._function_mapping:
            return
        for idx, fm in enumerate(self.generated_functions):
            self._function_mapping[idx] = fm
            self._function_mapping[fm.name] = fm

    def __getitem__(self, key: Union[int, str]) -> GeneratedFunction:
        self._fill_function_mapping()
        if key not in self._function_mapping:
            raise KeyError(f"No function named {key}")
        return self._function_mapping[key]

    def __len__(self) -> int:
        return self.generated_functions.__len__()

    def __iter__(self):
        yield from self.generated_functions

    def pprint(self) -> None:
        print("Circuit Synthesis Metrics")
        print(f"The circuit has {len(self.generated_functions)} functions:")
        for index, fm in enumerate(self.generated_functions):
            print(f"{index}) {fm.name}")
            print(
                f"  depth: {fm.depth} ; "
                f"width: {fm.width} ; "
                f"registers: {len(fm.registers)}"
            )
            for reg_index, register in enumerate(fm.registers):
                print(
                    f"  {reg_index}) {register.role.value} - {register.name} ; "
                    f"qubits: {register.qubit_indexes_absolute}"
                )

    @classmethod
    def from_empty_logic_flow(cls) -> "GeneratedCircuitData":
        return cls(width=0)
