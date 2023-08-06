from classiq.interface.generator.expressions.expression import Expression
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

from classiq import Integer
from classiq.applications_model_constructors.libraries.qft_library import QFT_LIBRARY

QPE_LIBRARY = [
    *QFT_LIBRARY,
    NativeFunctionDefinition(
        name="qpe",
        param_decls={"reg_size": Integer(), "qpe_reg_size": Integer()},
        port_declarations={
            "x": PortDeclaration(
                name="x",
                size=Expression(expr="reg_size"),
                direction=PortDeclarationDirection.Inout,
            ),
            "q": PortDeclaration(
                name="q",
                size=Expression(expr="qpe_reg_size"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        operand_declarations={
            "qfunc": QuantumOperandDeclaration(
                name="qfunc",
                port_declarations={
                    "target": PortDeclaration(
                        name="target",
                        direction=PortDeclarationDirection.Inout,
                        size=Expression(expr="reg_size"),
                    )
                },
            )
        },
        body=[
            QuantumFunctionCall(
                function="uniform_superposition",
                params={"num_qubits": {"expr": "qpe_reg_size"}},
                inputs={"q": "q_in"},
                outputs={"q": "qwire_0"},
            ),
            QuantumFunctionCall(
                function="join",
                params={
                    "in1_size": Expression(expr="reg_size"),
                    "in2_size": Expression(expr="qpe_reg_size"),
                },
                inputs={"in1": "x_in", "in2": "qwire_0"},
                outputs={"out": "repeat_in"},
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="qpe_reg_size"),
                    "port_size": Expression(expr="reg_size + qpe_reg_size"),
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
                                    "target_size": Expression(expr="reg_size"),
                                },
                                inputs={
                                    "ctrl": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="reg_size+index"),
                                        end=Expression(expr="reg_size+index"),
                                    ),
                                    "target": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="reg_size-1"),
                                    ),
                                },
                                outputs={
                                    "ctrl": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="reg_size+index"),
                                        end=Expression(expr="reg_size+index"),
                                    ),
                                    "target": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="reg_size-1"),
                                    ),
                                },
                                operands={
                                    "operand": QuantumLambdaFunction(
                                        body=[
                                            QuantumFunctionCall(
                                                function="repeat",
                                                params={
                                                    "count": Expression(
                                                        expr="2**index"
                                                    ),
                                                    "port_size": Expression(
                                                        expr="reg_size"
                                                    ),
                                                },
                                                inputs={"qbv": "target_in"},
                                                outputs={"qbv": "target_out"},
                                                operands={
                                                    "iteration": QuantumLambdaFunction(
                                                        body=[
                                                            QuantumFunctionCall(
                                                                function="qfunc",
                                                                inputs={
                                                                    "target": "qbv_in"
                                                                },
                                                                outputs={
                                                                    "target": "qbv_out"
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
                        ]
                    ),
                },
            ),
            QuantumFunctionCall(
                function="split",
                params={
                    "out1_size": Expression(expr="reg_size"),
                    "out2_size": Expression(expr="qpe_reg_size"),
                },
                inputs={"in": "repeat_out"},
                outputs={"out1": "x_out", "out2": "iqft_in"},
            ),
            QuantumFunctionCall(
                function="invert",
                params={
                    "target_size": Expression(expr="qpe_reg_size"),
                },
                inputs={"target": "iqft_in"},
                outputs={"target": "q_out"},
                operands={
                    "operand": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="qft",
                                params={"num_qbits": Expression(expr="qpe_reg_size")},
                                inputs={"qbv": "target_in"},
                                outputs={"qbv": "target_out"},
                            )
                        ]
                    )
                },
            ),
        ],
    ),
]
