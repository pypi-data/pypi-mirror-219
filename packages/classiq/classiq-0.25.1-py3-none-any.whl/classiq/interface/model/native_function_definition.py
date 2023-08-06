from typing import Any, Dict, List, Optional

import pydantic

from classiq.interface.generator.function_params import IOName, PortDirection
from classiq.interface.generator.functions import (
    LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG,
    PortDeclaration,
)
from classiq.interface.generator.functions.native_function_definition import (
    _validate_ports_wiring_for_direction,
)
from classiq.interface.generator.parameters import ParameterFloatType, ParameterMap
from classiq.interface.generator.quantum_function_call import WireDict, WireName
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.model.validations import flow_graph


class NativeFunctionDefinition(QuantumFunctionDeclaration):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    parameters: List[ParameterMap] = pydantic.Field(
        default_factory=list,
        description="The parameters (name and mapped parameter or value) of the function",
    )

    input_ports_wiring: Dict[IOName, WireName] = pydantic.Field(
        description="The mapping between the functions input ports, to inner wires",
        default_factory=dict,
    )

    output_ports_wiring: Dict[IOName, WireName] = pydantic.Field(
        description="The mapping between the functions output ports, to inner wires",
        default_factory=dict,
    )

    body: List[QuantumFunctionCall] = pydantic.Field(
        default_factory=list, description="List of function calls to perform."
    )

    @pydantic.validator("body")
    def _validate_logic_body(
        cls, body: List[QuantumFunctionCall], values: Dict[str, Any]
    ) -> List[QuantumFunctionCall]:
        function_call_names = {call.name for call in body}
        if len(function_call_names) != len(body):
            raise ValueError(LOGIC_FLOW_DUPLICATE_NAME_ERROR_MSG)

        inputs = values.get("input_ports_wiring", dict())
        outputs = values.get("output_ports_wiring", dict())

        flow_graph.validate_legal_wiring(
            body,
            flow_input_names=list(inputs.values()),
            flow_output_names=list(outputs.values()),
        )
        flow_graph.validate_acyclic_logic_flow(
            body,
            flow_input_names=list(inputs.values()),
            flow_output_names=list(outputs.values()),
        )
        return body

    @property
    def inputs_to_wires(self) -> WireDict:
        return self.input_ports_wiring

    @property
    def outputs_to_wires(self) -> WireDict:
        return self.output_ports_wiring

    @property
    def parameters_mapping(self) -> Dict[str, ParameterFloatType]:
        return {
            parameter.original: parameter.new_parameter for parameter in self.parameters
        }

    @classmethod
    def _validate_direction_ports(
        cls,
        port_declarations: Dict[IOName, PortDeclaration],
        directions_external_port_wiring: WireDict,
        direction: PortDirection,
    ) -> None:
        for io_name in directions_external_port_wiring:
            if (
                io_name not in port_declarations
                or not port_declarations[io_name].direction == direction
            ):
                raise ValueError(
                    f"The wired {direction} port {io_name!r} is not declared."
                )

    @pydantic.root_validator
    def validate_ports(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        port_declarations: Optional[Dict[IOName, PortDeclaration]] = values.get(
            "port_declarations"
        )
        if port_declarations is None:
            return values
        cls._validate_direction_ports(
            port_declarations,
            values.get("input_ports_wiring", dict()),
            PortDirection.Input,
        )
        cls._validate_direction_ports(
            port_declarations,
            values.get("output_ports_wiring", dict()),
            PortDirection.Output,
        )
        return values

    @pydantic.validator("input_ports_wiring", always=True)
    def _populate_input_ports_wiring(
        cls, input_ports_wiring: Dict[IOName, WireName], values: Dict[str, Any]
    ) -> Dict[IOName, WireName]:
        return _validate_ports_wiring_for_direction(
            input_ports_wiring, values, PortDirection.Input
        )

    @pydantic.validator("output_ports_wiring", always=True)
    def _populate_output_ports_wiring(
        cls, output_ports_wiring: Dict[IOName, WireName], values: Dict[str, Any]
    ) -> Dict[IOName, WireName]:
        return _validate_ports_wiring_for_direction(
            output_ports_wiring, values, PortDirection.Output
        )
