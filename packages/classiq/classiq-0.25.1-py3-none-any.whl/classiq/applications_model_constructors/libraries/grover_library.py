import numpy as np

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.standard_gates.standard_gates import XGate, ZGate
from classiq.interface.generator.standard_gates.u_gate import UGate
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

from classiq import Integer

GROVER_LIBRARY = [
    NativeFunctionDefinition(
        name="grover_diffuser",
        param_decls={"num_qubits": Integer()},
        port_declarations={
            "p": PortDeclaration(
                name="p",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="apply_to_all",
                params={"num_qubits": {"expr": "num_qubits"}},
                inputs={"q": "p_in"},
                outputs={"q": "p_1"},
                operands={
                    "gate_operand": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="XGate",
                                function_params=XGate(),
                                inputs={"TARGET": "target_in"},
                                outputs={"TARGET": "target_out"},
                            )
                        ]
                    )
                },
            ),
            QuantumFunctionCall(
                function="split",
                params={
                    "out1_size": Expression(expr="num_qubits-1"),
                    "out2_size": Expression(expr="1"),
                },
                inputs={"in": "p_1"},
                outputs={"out1": "msbs0", "out2": "lsb0"},
            ),
            QuantumFunctionCall(
                function="control",
                params={
                    "ctrl_size": Expression(expr="num_qubits-1"),
                    "target_size": Expression(expr="1"),
                },
                inputs={"ctrl": "msbs0", "target": "lsb0"},
                outputs={"ctrl": "msbs1", "target": "lsb1"},
                operands={
                    "operand": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="ZGate",
                                function_params=ZGate(),
                                inputs={"TARGET": "target_in"},
                                outputs={"TARGET": "target_out"},
                            ),
                        ]
                    ),
                },
            ),
            QuantumFunctionCall(
                function="join",
                params={
                    "in1_size": Expression(expr="num_qubits-1"),
                    "in2_size": Expression(expr="1"),
                },
                inputs={"in1": "msbs1", "in2": "lsb1"},
                outputs={"out": "p_2"},
            ),
            QuantumFunctionCall(
                function="apply_to_all",
                params={"num_qubits": {"expr": "num_qubits"}},
                inputs={"q": "p_2"},
                outputs={"q": "p_out"},
                operands={
                    "gate_operand": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="XGate",
                                function_params=XGate(),
                                inputs={"TARGET": "target_in"},
                                outputs={"TARGET": "target_out"},
                            )
                        ]
                    )
                },
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="grover_operator",
        param_decls={"num_qubits": Integer()},
        port_declarations={
            "p": PortDeclaration(
                name="p",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        operand_declarations={
            "sp_op": QuantumOperandDeclaration(
                name="sp_op",
                param_decls={"num_qubits": Integer()},
                port_declarations={
                    "spq": PortDeclaration(
                        name="spq",
                        direction="inout",
                        size=Expression(expr="num_qubits"),
                    )
                },
            ),
            "oracle_op": QuantumOperandDeclaration(
                name="oracle_op",
                param_decls={"num_qubits": Integer()},
                port_declarations={
                    "oq": PortDeclaration(
                        name="oq",
                        direction="inout",
                        size=Expression(expr="num_qubits"),
                    )
                },
            ),
        },
        body=[
            QuantumFunctionCall(
                function="oracle_op",
                params={"num_qubits": Expression(expr="num_qubits")},
                inputs={"oq": "p_in"},
                outputs={"oq": "w2"},
            ),
            QuantumFunctionCall(
                function="invert",
                params={
                    "target_size": Expression(expr="num_qubits"),
                },
                inputs={"target": "w2"},
                outputs={"target": "w3"},
                should_control=False,
                operands={
                    "operand": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="sp_op",
                                params={"num_qubits": Expression(expr="num_qubits")},
                                inputs={"spq": "target_in"},
                                outputs={"spq": "target_out"},
                            )
                        ]
                    )
                },
            ),
            QuantumFunctionCall(
                function="grover_diffuser",
                params={"num_qubits": Expression(expr="num_qubits")},
                inputs={"p": "w3"},
                outputs={"p": "w4"},
            ),
            QuantumFunctionCall(
                function="sp_op",
                params={"num_qubits": Expression(expr="num_qubits")},
                inputs={"spq": "w4"},
                outputs={"spq": "w5"},
                should_control=False,
            ),
            # add a (-1) phase to the operator so that AE will work
            QuantumFunctionCall(
                function="UGate",
                function_params=UGate(theta=0, phi=0, lam=0, gam=np.pi),
                inputs={
                    "TARGET": PortBinding(
                        name="w5", start=Expression(expr="0"), end=Expression(expr="0")
                    )
                },
                outputs={
                    "TARGET": PortBinding(
                        name="p_out",
                        start=Expression(expr="0"),
                        end=Expression(expr="0"),
                    )
                },
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="uniform_superposition",
        param_decls={"num_qubits": Integer()},
        port_declarations={
            "q": PortDeclaration(
                name="q",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="apply_to_all",
                operands={
                    "gate_operand": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="H",
                                inputs={"target": "target_in"},
                                outputs={"target": "target_out"},
                            )
                        ]
                    )
                },
                params={"num_qubits": {"expr": "num_qubits"}},
                inputs={"q": "q_in"},
                outputs={"q": "q_out"},
            )
        ],
    ),
    NativeFunctionDefinition(
        name="apply_to_all",
        param_decls={"num_qubits": Integer()},
        port_declarations={
            "q": PortDeclaration(
                name="q",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        operand_declarations={
            "gate_operand": QuantumOperandDeclaration(
                name="gate_operand",
                port_declarations={
                    "target": PortDeclaration(
                        name="target",
                        direction="inout",
                        size=Expression(expr="1"),
                    )
                },
            )
        },
        body=[
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_qubits"),
                    "port_size": Expression(expr="num_qubits"),
                },
                inputs={"qbv": "q_in"},
                outputs={"qbv": "q_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="gate_operand",
                                inputs={
                                    "target": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                },
                                outputs={
                                    "target": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                },
                            ),
                        ]
                    ),
                },
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="grover_search",
        param_decls={"num_qubits": Integer(), "reps": Integer()},
        port_declarations={
            "gsq": PortDeclaration(
                name="gsq",
                size=Expression(expr="num_qubits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        operand_declarations={
            "oracle_op": QuantumOperandDeclaration(
                name="oracle_op",
                param_decls={"num_qubits": Integer()},
                port_declarations={
                    "oq": PortDeclaration(
                        name="oq",
                        direction="inout",
                        size=Expression(expr="num_qubits"),
                    )
                },
            )
        },
        body=[
            QuantumFunctionCall(
                function="uniform_superposition",
                params={"num_qubits": {"expr": "num_qubits"}},
                inputs={"q": "gsq_in"},
                outputs={"q": "w2"},
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": {"expr": "reps"},
                    "port_size": {"expr": "num_qubits"},
                },
                inputs={"qbv": "w2"},
                outputs={"qbv": "gsq_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="grover_operator",
                                inputs={"p": "qbv_in"},
                                outputs={"p": "qbv_out"},
                                params={"num_qubits": Expression(expr="num_qubits")},
                                operands={
                                    "oracle_op": QuantumLambdaFunction(
                                        body=[
                                            QuantumFunctionCall(
                                                function="oracle_op",
                                                params={
                                                    "num_qubits": Expression(
                                                        expr="num_qubits"
                                                    )
                                                },
                                                inputs={"oq": "oq_in"},
                                                outputs={"oq": "oq_out"},
                                            )
                                        ]
                                    ),
                                    "sp_op": QuantumLambdaFunction(
                                        body=[
                                            QuantumFunctionCall(
                                                function="uniform_superposition",
                                                params={
                                                    "num_qubits": Expression(
                                                        expr="num_qubits"
                                                    )
                                                },
                                                inputs={"q": "spq_in"},
                                                outputs={"q": "spq_out"},
                                            )
                                        ]
                                    ),
                                },
                            )
                        ]
                    )
                },
            ),
        ],
    ),
]
