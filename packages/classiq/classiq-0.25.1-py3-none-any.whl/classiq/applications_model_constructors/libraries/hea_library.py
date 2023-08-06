from typing import List

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_call import OperandIdentifier
from classiq.interface.generator.functions.classical_type import Real
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.wiring.sliced_wire import PortBinding
from classiq.interface.model.native_function_definition import (
    NativeFunctionDefinition,
    PortDeclaration,
)
from classiq.interface.model.quantum_function_call import (
    QuantumFunctionCall,
    QuantumLambdaFunction,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumOperandDeclaration,
)

from classiq import ClassicalList, Integer

HEA_LIBRARY: List[NativeFunctionDefinition] = [
    NativeFunctionDefinition(
        name="full_hea",
        param_decls={
            "num_qubits": Integer(),
            "is_parametrized": ClassicalList(element_type=Integer()),
            "angle_params": ClassicalList(element_type=Real()),
            "connectivity_map": ClassicalList(
                element_type=ClassicalList(element_type=Integer())
            ),
            "reps": Integer(),
        },
        port_declarations={
            "x": PortDeclaration(
                name="x",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            )
        },
        operand_declarations={
            "operands_1qubit": QuantumOperandDeclaration(
                name="operands_1qubit",
                param_decls={"angle": Real()},
                port_declarations={
                    "q": PortDeclaration(
                        name="q",
                        size=Expression(expr="1"),
                        direction="inout",
                    )
                },
                is_list=True,
            ),
            "operands_2qubit": QuantumOperandDeclaration(
                name="operands_2qubit",
                param_decls={"angle": Real()},
                port_declarations={
                    "q1": PortDeclaration(
                        name="q1", size=Expression(expr="1"), direction="inout"
                    ),
                    "q2": PortDeclaration(
                        name="q2", size=Expression(expr="1"), direction="inout"
                    ),
                },
                is_list=True,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="reps"),
                    "port_size": Expression(expr="num_qubits"),
                },
                inputs={"qbv": "x_in"},
                outputs={"qbv": "x_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        rename_params={"index": "r"},
                        body=[
                            QuantumFunctionCall(
                                function="repeat",
                                params={
                                    "count": Expression(expr="len(operands_1qubit)"),
                                    "port_size": Expression(expr="num_qubits"),
                                },
                                inputs={"qbv": "qbv_in"},
                                outputs={"qbv": "x_1"},
                                operands={
                                    "iteration": QuantumLambdaFunction(
                                        rename_params={"index": "i1"},
                                        body=[
                                            QuantumFunctionCall(
                                                function="repeat",
                                                params={
                                                    "count": Expression(
                                                        expr="num_qubits"
                                                    ),
                                                    "port_size": Expression(
                                                        expr="num_qubits"
                                                    ),
                                                },
                                                inputs={"qbv": "qbv_in"},
                                                outputs={"qbv": "qbv_out"},
                                                operands={
                                                    "iteration": QuantumLambdaFunction(
                                                        body=[
                                                            QuantumFunctionCall(
                                                                function="if",
                                                                params={
                                                                    "condition": Expression(
                                                                        expr="Eq(is_parametrized[i1],1)"
                                                                    ),
                                                                    "port_size": Expression(
                                                                        expr="num_qubits"
                                                                    ),
                                                                },
                                                                inputs={
                                                                    "qbv": "qbv_in"
                                                                },
                                                                outputs={
                                                                    "qbv": "qbv_out"
                                                                },
                                                                operands={
                                                                    "then": QuantumLambdaFunction(
                                                                        body=[
                                                                            QuantumFunctionCall(
                                                                                function=OperandIdentifier(
                                                                                    name="operands_1qubit",
                                                                                    index=Expression(
                                                                                        expr="i1"
                                                                                    ),
                                                                                ),
                                                                                params={
                                                                                    "angle": Expression(
                                                                                        expr="angle_params[sum(is_parametrized[0:i1])+len(angle_params)//reps*r+index]"
                                                                                    )
                                                                                },
                                                                                inputs={
                                                                                    "q": PortBinding(
                                                                                        name="qbv_in",
                                                                                        start=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                                outputs={
                                                                                    "q": PortBinding(
                                                                                        name="qbv_out",
                                                                                        start=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    "else": QuantumLambdaFunction(
                                                                        body=[
                                                                            QuantumFunctionCall(
                                                                                function=OperandIdentifier(
                                                                                    name="operands_1qubit",
                                                                                    index=Expression(
                                                                                        expr="i1"
                                                                                    ),
                                                                                ),
                                                                                params={
                                                                                    "angle": Expression(
                                                                                        expr="0"
                                                                                    )
                                                                                },
                                                                                inputs={
                                                                                    "q": PortBinding(
                                                                                        name="qbv_in",
                                                                                        start=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                                outputs={
                                                                                    "q": PortBinding(
                                                                                        name="qbv_out",
                                                                                        start=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="index"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ],
                                                                    ),
                                                                },
                                                            ),
                                                        ],
                                                    )
                                                },
                                            ),
                                        ],
                                    )
                                },
                            ),
                            QuantumFunctionCall(
                                function="repeat",
                                params={
                                    "count": Expression(expr="len(operands_2qubit)"),
                                    "port_size": Expression(expr="num_qubits"),
                                },
                                inputs={"qbv": "x_1"},
                                outputs={"qbv": "qbv_out"},
                                operands={
                                    "iteration": QuantumLambdaFunction(
                                        rename_params={"index": "i2"},
                                        body=[
                                            QuantumFunctionCall(
                                                function="repeat",
                                                params={
                                                    "count": Expression(
                                                        expr="len(connectivity_map)"
                                                    ),
                                                    "port_size": Expression(
                                                        expr="num_qubits"
                                                    ),
                                                },
                                                inputs={"qbv": "qbv_in"},
                                                outputs={"qbv": "qbv_out"},
                                                operands={
                                                    "iteration": QuantumLambdaFunction(
                                                        body=[
                                                            QuantumFunctionCall(
                                                                function="if",
                                                                params={
                                                                    "condition": Expression(
                                                                        expr="Eq(is_parametrized[len(operands_1qubit) + i2],1)"
                                                                    ),
                                                                    "port_size": Expression(
                                                                        expr="num_qubits"
                                                                    ),
                                                                },
                                                                inputs={
                                                                    "qbv": "qbv_in"
                                                                },
                                                                outputs={
                                                                    "qbv": "qbv_out"
                                                                },
                                                                operands={
                                                                    "then": QuantumLambdaFunction(
                                                                        body=[
                                                                            QuantumFunctionCall(
                                                                                function=OperandIdentifier(
                                                                                    name="operands_2qubit",
                                                                                    index=Expression(
                                                                                        expr="i2"
                                                                                    ),
                                                                                ),
                                                                                params={
                                                                                    "angle": Expression(
                                                                                        expr="angle_params[num_qubits*sum(is_parametrized[0:len(operands_1qubit)])+\
                                                                                            +len(connectivity_map)*sum(is_parametrized[len(operands_1qubit):len(operands_1qubit)+i2])+len(angle_params)//reps*r+index] "
                                                                                    )
                                                                                },
                                                                                inputs={
                                                                                    "q1": PortBinding(
                                                                                        name="qbv_in",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                    ),
                                                                                    "q2": PortBinding(
                                                                                        name="qbv_in",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                                outputs={
                                                                                    "q1": PortBinding(
                                                                                        name="qbv_out",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                    ),
                                                                                    "q2": PortBinding(
                                                                                        name="qbv_out",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    "else": QuantumLambdaFunction(
                                                                        body=[
                                                                            QuantumFunctionCall(
                                                                                function=OperandIdentifier(
                                                                                    name="operands_2qubit",
                                                                                    index=Expression(
                                                                                        expr="i2"
                                                                                    ),
                                                                                ),
                                                                                params={
                                                                                    "angle": Expression(
                                                                                        expr="0"
                                                                                    )
                                                                                },
                                                                                inputs={
                                                                                    "q1": PortBinding(
                                                                                        name="qbv_in",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                    ),
                                                                                    "q2": PortBinding(
                                                                                        name="qbv_in",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                                outputs={
                                                                                    "q1": PortBinding(
                                                                                        name="qbv_out",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][0]"
                                                                                        ),
                                                                                    ),
                                                                                    "q2": PortBinding(
                                                                                        name="qbv_out",
                                                                                        start=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                        end=Expression(
                                                                                            expr="connectivity_map[index][1]"
                                                                                        ),
                                                                                    ),
                                                                                },
                                                                            ),
                                                                        ],
                                                                    ),
                                                                },
                                                            ),
                                                        ],
                                                    )
                                                },
                                            )
                                        ],
                                    )
                                },
                            ),
                        ],
                    )
                },
            )
        ],
    )
]
