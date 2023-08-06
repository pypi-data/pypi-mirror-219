from typing import Dict, List, Tuple

from classiq.interface.generator.arith.arithmetic_expression_abc import (
    UncomputationMethods,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.assignment_statement import (
    AssignmentStatement,
)
from classiq.interface.generator.functions.classical_function_definition import (
    ClassicalFunctionDefinition,
)
from classiq.interface.generator.functions.classical_type import Histogram
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.save_statement import SaveStatement
from classiq.interface.generator.functions.variable_declaration_statement import (
    VariableDeclaration,
)
from classiq.interface.generator.model.model import SerializedModel
from classiq.interface.generator.oracles import ArithmeticOracle
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.generator.wiring.sliced_wire import PortBinding
from classiq.interface.model.model import Model
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
    PortDeclaration,
)
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)

from classiq import RegisterUserInput
from classiq.applications_model_constructors.constructors_utilities import get_model
from classiq.applications_model_constructors.libraries.grover_library import (
    GROVER_LIBRARY,
)

_OUTPUT_VARIABLE_NAME = "result"


def split_registers(
    register_names: List[str],
    register_sizes: List[int],
    input_wire_name: str,
) -> List[QuantumFunctionCall]:
    if len(register_names) == 0:
        return []
    wires = (
        [input_wire_name]
        + [f"split{i}" for i in range(len(register_names) - 2)]
        + [register_names[-1]]
    )
    return [
        QuantumFunctionCall(
            function="split",
            params={
                "out1_size": Expression(expr=f"{int(register_sizes[i])}"),
                "out2_size": Expression(expr=f"{int(sum(register_sizes[i + 1:]))}"),
            },
            inputs={"in": wires[i]},
            outputs={"out1": register, "out2": wires[i + 1]},
        )
        for i, register in enumerate(register_names[:-1])
    ]


def _arithmetic_oracle_io_dict(
    definitions: List[Tuple[str, RegisterUserInput]], wire_name: str
):
    cursor = 0
    ios = dict()
    for reg_name, reg in definitions:
        ios[reg_name] = PortBinding(
            name=wire_name,
            start=Expression(expr=f"{cursor}"),
            end=Expression(expr=f"{cursor + reg.size - 1}"),
        )
        cursor += reg.size
    return ios


def _construct_arithmetic_oracle(
    expression: str,
    definitions: List[Tuple[str, RegisterUserInput]],
    uncomputation_method: UncomputationMethods,
) -> QuantumFunctionCall:
    return QuantumFunctionCall(
        function="ArithmeticOracle",
        function_params=ArithmeticOracle(
            expression=expression,
            definitions={name: reg for name, reg in definitions},
            uncomputation_method=uncomputation_method,
        ),
        inputs=_arithmetic_oracle_io_dict(definitions, "oq_in"),
        outputs=_arithmetic_oracle_io_dict(definitions, "oq_out"),
    )


def grover_main_port_declarations(
    definitions: List[Tuple[str, RegisterUserInput]]
) -> Dict[str, PortDeclaration]:
    return {
        name: PortDeclaration(
            name=name,
            size=Expression(expr=f"{reg.size}"),
            direction=PortDeclarationDirection.Output,
        )
        for name, reg in definitions
    }


def construct_grover_model(
    definitions: List[Tuple[str, RegisterUserInput]],
    expression: str,
    num_shots: int,
    uncomputation_method: UncomputationMethods = UncomputationMethods.optimized,
    num_reps: int = 1,
) -> SerializedModel:
    grover_model = Model(
        functions=[
            *GROVER_LIBRARY,
            NativeFunctionDefinition(
                name="main",
                port_declarations=grover_main_port_declarations(definitions),
                body=[
                    QuantumFunctionCall(
                        function="grover_search",
                        params={
                            "num_qubits": Expression(
                                expr=f"{sum(reg.size for _, reg in definitions)}"
                            ),
                            "reps": Expression(expr=f"{num_reps}"),
                        },
                        outputs={"gsq": "gsq_out"},
                        operands={
                            "oracle_op": QuantumLambdaFunction(
                                body=[
                                    _construct_arithmetic_oracle(
                                        expression,
                                        definitions,
                                        uncomputation_method,
                                    )
                                ]
                            )
                        },
                    ),
                    *split_registers(
                        [f"{name}_out" for name, _ in definitions],
                        [reg.size for _, reg in definitions],
                        "gsq_out",
                    ),
                ],
            ),
        ],
        classical_functions=[
            ClassicalFunctionDefinition(
                name="cmain",
                body=[
                    VariableDeclaration(
                        name=_OUTPUT_VARIABLE_NAME, var_type=Histogram()
                    ),
                    AssignmentStatement(
                        assigned_variable=_OUTPUT_VARIABLE_NAME,
                        invoked_expression=QuantumInvokerCall(
                            function="sample",
                            params={"num_shots": Expression(expr=f"{num_shots}")},
                            target_function="main",
                        ),
                    ),
                    SaveStatement(saved_variable=_OUTPUT_VARIABLE_NAME),
                ],
            ),
        ],
    )
    return get_model(grover_model)
