from typing import List

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import Pauli, Real
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.identity import Identity
from classiq.interface.generator.standard_gates.standard_angled_gates import (
    RXGate,
    RYGate,
    RZGate,
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

from classiq import ClassicalList, Integer, RegisterUserInput

LPR_LIBRARY: List[NativeFunctionDefinition] = [
    NativeFunctionDefinition(
        name="single_pauli",
        param_decls={"reg_size": Integer(), "slope": Real(), "offset": Real()},
        port_declarations={
            "x": PortDeclaration(
                name="x",
                size=Expression(expr="reg_size"),
                direction=PortDeclarationDirection.Inout,
            ),
            "q": PortDeclaration(
                name="q",
                size=Expression(expr="1"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        operand_declarations={
            "q1_qfunc": QuantumOperandDeclaration(
                name="q1_qfunc",
                param_decls={"theta": Real()},
                port_declarations={
                    "target": PortDeclaration(
                        name="target",
                        direction=PortDeclarationDirection.Inout,
                        size=Expression(expr="1"),
                    )
                },
            )
        },
        body=[
            QuantumFunctionCall(
                function="join",
                params={
                    "in1_size": Expression(expr="reg_size"),
                    "in2_size": Expression(expr="1"),
                },
                inputs={"in1": "x_in", "in2": "q_in"},
                outputs={"out": "repeat_in"},
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="reg_size"),
                    "port_size": Expression(expr="reg_size + 1"),
                },
                inputs={"qbv": "repeat_in"},
                outputs={"qbv": "repeat_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="control",
                                params={
                                    "ctrl_size": Expression(expr="1"),
                                    "target_size": Expression(expr="1"),
                                },
                                inputs={
                                    "ctrl": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                    "target": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="reg_size"),
                                        end=Expression(expr="reg_size"),
                                    ),
                                },
                                outputs={
                                    "ctrl": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                    "target": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="reg_size"),
                                        end=Expression(expr="reg_size"),
                                    ),
                                },
                                operands={
                                    "operand": QuantumLambdaFunction(
                                        body=[
                                            QuantumFunctionCall(
                                                function="q1_qfunc",
                                                params={
                                                    "theta": Expression(
                                                        expr="2**index*slope"
                                                    )
                                                },
                                                inputs={"target": "target_in"},
                                                outputs={"target": "target_out"},
                                            ),
                                        ]
                                    ),
                                },
                            ),
                        ]
                    ),
                },
            ),
            QuantumFunctionCall(
                function="split",
                params={
                    "out1_size": Expression(expr="reg_size"),
                    "out2_size": Expression(expr="1"),
                },
                inputs={"in": "repeat_out"},
                outputs={"out1": "x_out", "out2": "q_2"},
            ),
            QuantumFunctionCall(
                function="q1_qfunc",
                params={"theta": Expression(expr="offset")},
                inputs={"target": "q_2"},
                outputs={"target": "q_out"},
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="linear_pauli_rotations",
        param_decls={
            "reg_size": Integer(),
            "num_state_qubits": Integer(),
            "bases": ClassicalList(element_type=Pauli()),
            "slopes": ClassicalList(element_type=Real()),
            "offsets": ClassicalList(element_type=Real()),
        },
        port_declarations={
            "x": PortDeclaration(
                name="x",
                size=Expression(expr="reg_size"),
                direction=PortDeclarationDirection.Inout,
            ),
            "q": PortDeclaration(
                name="q",
                size=Expression(expr="num_state_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="join",
                params={
                    "in1_size": Expression(expr="reg_size"),
                    "in2_size": Expression(expr="num_state_qubits"),
                },
                inputs={"in1": "x_in", "in2": "q_in"},
                outputs={"out": "repeat_in"},
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_state_qubits"),
                    "port_size": Expression(expr="reg_size + num_state_qubits"),
                },
                inputs={"qbv": "repeat_in"},
                outputs={"qbv": "repeat_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="single_pauli",
                                params={
                                    "reg_size": Expression(expr="reg_size"),
                                    "slope": Expression(expr="slopes[index]"),
                                    "offset": Expression(expr="offsets[index]"),
                                },
                                inputs={
                                    "x": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="reg_size-1"),
                                    ),
                                    "q": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="reg_size+index"),
                                        end=Expression(expr="reg_size+index"),
                                    ),
                                },
                                outputs={
                                    "x": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="reg_size-1"),
                                    ),
                                    "q": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="reg_size+index"),
                                        end=Expression(expr="reg_size+index"),
                                    ),
                                },
                                operands={
                                    "q1_qfunc": QuantumLambdaFunction(
                                        body=[
                                            QuantumFunctionCall(
                                                function="switch",
                                                params={
                                                    "port_size": Expression(expr="1"),
                                                    "selector": Expression(
                                                        expr="bases[index]"
                                                    ),
                                                },
                                                inputs={"qbv": "target_in"},
                                                outputs={"qbv": "target_out"},
                                                operands={
                                                    "cases": [
                                                        QuantumLambdaFunction(
                                                            body=[
                                                                QuantumFunctionCall(
                                                                    function="Identity",
                                                                    function_params=Identity(
                                                                        arguments=[
                                                                            RegisterUserInput(
                                                                                size=1,
                                                                                name="TARGET",
                                                                            )
                                                                        ]
                                                                    ),
                                                                    inputs={
                                                                        "TARGET": "qbv_in"
                                                                    },
                                                                    outputs={
                                                                        "TARGET": "qbv_out"
                                                                    },
                                                                )
                                                            ]
                                                        ),
                                                        QuantumLambdaFunction(
                                                            body=[
                                                                QuantumFunctionCall(
                                                                    function="RXGate",
                                                                    function_params=RXGate(
                                                                        theta="theta"
                                                                    ),
                                                                    inputs={
                                                                        "TARGET": "qbv_in"
                                                                    },
                                                                    outputs={
                                                                        "TARGET": "qbv_out"
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                        QuantumLambdaFunction(
                                                            body=[
                                                                QuantumFunctionCall(
                                                                    function="RYGate",
                                                                    function_params=RYGate(
                                                                        theta="theta"
                                                                    ),
                                                                    inputs={
                                                                        "TARGET": "qbv_in"
                                                                    },
                                                                    outputs={
                                                                        "TARGET": "qbv_out"
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                        QuantumLambdaFunction(
                                                            body=[
                                                                QuantumFunctionCall(
                                                                    function="RZGate",
                                                                    function_params=RZGate(
                                                                        phi="theta"
                                                                    ),
                                                                    inputs={
                                                                        "TARGET": "qbv_in"
                                                                    },
                                                                    outputs={
                                                                        "TARGET": "qbv_out"
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                },
                                            )
                                        ]
                                    )
                                },
                            ),
                        ]
                    ),
                },
            ),
            QuantumFunctionCall(
                function="split",
                params={
                    "out1_size": Expression(expr="reg_size"),
                    "out2_size": Expression(expr="num_state_qubits"),
                },
                inputs={"in": "repeat_out"},
                outputs={"out1": "x_out", "out2": "q_out"},
            ),
        ],
    ),
]
