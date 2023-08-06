from typing import Any, Dict, List, NewType, Optional, Union

import pydantic

from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.constant import Constant
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions import (
    PortDeclaration,
    QuantumFunctionDeclaration,
    SynthesisNativeFunctionDefinition,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.name_resolution import resolve_function_calls
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.generator.quantum_function_call import (
    SUFFIX_RANDOMIZER,
    SynthesisQuantumFunctionCall,
    WireDict,
)
from classiq.interface.generator.types.combinatorial_problem import (
    CombinatorialOptimizationStructDeclaration,
)
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.helpers.validation_helpers import is_list_unique
from classiq.interface.helpers.versioned_model import VersionedModel

from classiq import ForeignFunctionDefinition as SynthesisForeignFunctionDefinition

MAIN_FUNCTION_NAME = "main"
CLASSICAL_ENTRY_FUNCTION_NAME = "cmain"

DEFAULT_PORT_SIZE = 1


SerializedModel = NewType("SerializedModel", str)

ConcreteStructDeclaration = Union[
    CombinatorialOptimizationStructDeclaration, StructDeclaration
]

# We need to define ConcreteFunctionData so pydantic will know
# what class to use when deserializing from object (pydantic attempts to
# parse as each of the classes in the Union, in order).
ConcreteFunctionDefinition = Union[
    SynthesisForeignFunctionDefinition, SynthesisNativeFunctionDefinition
]

TYPE_LIBRARY_DUPLICATED_TYPE_NAMES = (
    "Cannot have multiple struct types with the same name"
)


def _create_default_functions() -> List[ConcreteFunctionDefinition]:
    return [SynthesisNativeFunctionDefinition(name=MAIN_FUNCTION_NAME)]


class SynthesisModel(VersionedModel):
    """
    All the relevant data for generating quantum circuit in one place.
    """

    # Must be validated before logic_flow
    functions: List[ConcreteFunctionDefinition] = pydantic.Field(
        default_factory=_create_default_functions,
        description="The user-defined custom type library.",
    )

    types: List[ConcreteStructDeclaration] = pydantic.Field(
        default_factory=list,
        description="The user-defined custom function library.",
    )

    constants: List[Constant] = pydantic.Field(
        default_factory=list,
    )

    classical_functions: List[ClassicalFunctionDefinition] = pydantic.Field(
        default_factory=list,
        description="The classical functions of the model",
    )

    constraints: Constraints = pydantic.Field(default_factory=Constraints)

    execution_preferences: ExecutionPreferences = pydantic.Field(
        default_factory=ExecutionPreferences
    )
    preferences: Preferences = pydantic.Field(default_factory=Preferences)

    def __init__(
        self,
        *,
        body: Optional[List[SynthesisQuantumFunctionCall]] = None,
        inputs: Optional[WireDict] = None,
        outputs: Optional[WireDict] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if body:
            self.main_func.body.extend(body)
        if inputs:
            self.set_inputs(inputs)
        if outputs:
            self.set_outputs(outputs)

    @property
    def main_func(self) -> SynthesisNativeFunctionDefinition:
        return self.function_dict[MAIN_FUNCTION_NAME]  # type:ignore[return-value]

    @property
    def body(self) -> List[SynthesisQuantumFunctionCall]:
        return self.main_func.body

    @property
    def inputs(self) -> WireDict:
        return self.main_func.input_ports_wiring

    def set_inputs(self, value) -> None:
        self._update_main_declarations(value, PortDeclarationDirection.Input)
        self.main_func.input_ports_wiring.update(value)

    @property
    def outputs(self) -> WireDict:
        return self.main_func.output_ports_wiring

    def set_outputs(self, value) -> None:
        self._update_main_declarations(value, PortDeclarationDirection.Output)
        self.main_func.output_ports_wiring.update(value)

    @pydantic.validator("preferences", always=True)
    def _seed_suffix_randomizer(cls, preferences: Preferences) -> Preferences:
        SUFFIX_RANDOMIZER.seed(preferences.random_seed)
        return preferences

    def _get_qualified_direction(
        self, port_name: str, direction: PortDeclarationDirection
    ) -> PortDeclarationDirection:
        if port_name in self.main_func.port_declarations:
            return PortDeclarationDirection.Inout
        return direction

    def _update_main_declarations(
        self, value, direction: PortDeclarationDirection
    ) -> None:
        for port_name in value.keys():
            self.main_func.port_declarations[port_name] = PortDeclaration(
                name=port_name,
                size=Expression(expr=f"{DEFAULT_PORT_SIZE}"),
                direction=self._get_qualified_direction(port_name, direction),
            )

    @property
    def function_dict(self) -> Dict[str, QuantumFunctionDeclaration]:
        return nameables_to_dict(self.functions)

    @property
    def classical_function_dict(self) -> Dict[str, ClassicalFunctionDefinition]:
        return nameables_to_dict(self.classical_functions)

    @pydantic.root_validator()
    def validate_static_correctness(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        functions: List[QuantumFunctionDeclaration] = values.get(
            "functions"
        )  # type:ignore[assignment]
        classical_functions: List[ClassicalFunctionDefinition] = values.get(
            "classical_functions"
        )  # type:ignore[assignment]
        resolve_function_calls(
            values,
            nameables_to_dict(classical_functions),
            nameables_to_dict(functions),
        )
        for func_def in functions:
            if isinstance(func_def, SynthesisNativeFunctionDefinition):
                func_def.validate_body()
        return values

    @pydantic.validator("types")
    def types_validator(cls, types: List[ConcreteStructDeclaration]):
        if not is_list_unique([struct_type.name for struct_type in types]):
            raise ValueError(TYPE_LIBRARY_DUPLICATED_TYPE_NAMES)

        return types

    def get_model(self) -> SerializedModel:
        return SerializedModel(self.json(exclude_defaults=True, indent=2))
