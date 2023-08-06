from typing import List

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

from classiq import Integer

QFT_LIBRARY: List[NativeFunctionDefinition] = [
    NativeFunctionDefinition(
        name="qft_step",
        param_decls={"num_qbits": Integer()},
        port_declarations={
            "qbv": PortDeclaration(
                name="qbv",
                size=Expression(expr="num_qbits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="H",
                inputs={
                    "target": PortBinding(
                        name="qbv_in",
                        start=Expression(expr="0"),
                        end=Expression(expr="0"),
                    ),
                },
                outputs={
                    "target": PortBinding(
                        name="h_out",
                        start=Expression(expr="0"),
                        end=Expression(expr="0"),
                    ),
                },
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_qbits-1"),
                    "port_size": Expression(expr="num_qbits"),
                },
                inputs={"qbv": "h_out"},
                outputs={"qbv": "qbv_out"},
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
                                        start=Expression(expr="index+1"),
                                        end=Expression(expr="index+1"),
                                    ),
                                    "target": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="0"),
                                    ),
                                },
                                outputs={
                                    "ctrl": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="index+1"),
                                        end=Expression(expr="index+1"),
                                    ),
                                    "target": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="0"),
                                    ),
                                },
                                operands={
                                    "operand": QuantumLambdaFunction(
                                        body=[
                                            QuantumFunctionCall(
                                                function="PHASE",
                                                params={
                                                    "theta": Expression(
                                                        expr="pi/2**(index+1)"
                                                    )
                                                },
                                                inputs={"target": "target_in"},
                                                outputs={"target": "target_out"},
                                            )
                                        ],
                                    ),
                                },
                            )
                        ],
                    ),
                },
            ),
        ],
    ),
    NativeFunctionDefinition(
        name="qft",
        param_decls={"num_qbits": Integer()},
        port_declarations={
            "qbv": PortDeclaration(
                name="qbv",
                size=Expression(expr="num_qbits"),
                direction=PortDeclarationDirection.Inout,
            ),
        },
        body=[
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_qbits//2"),
                    "port_size": Expression(expr="num_qbits"),
                },
                inputs={"qbv": "qbv_in"},
                outputs={"qbv": "wire_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="SWAP",
                                inputs={
                                    "qbit0": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                    "qbit1": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="num_qbits-1-index"),
                                        end=Expression(expr="num_qbits-1-index"),
                                    ),
                                },
                                outputs={
                                    "qbit0": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="index"),
                                    ),
                                    "qbit1": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="num_qbits-1-index"),
                                        end=Expression(expr="num_qbits-1-index"),
                                    ),
                                },
                            )
                        ],
                    ),
                },
            ),
            QuantumFunctionCall(
                function="repeat",
                params={
                    "count": Expression(expr="num_qbits"),
                    "port_size": Expression(expr="num_qbits"),
                },
                inputs={"qbv": "wire_out"},
                outputs={"qbv": "qbv_out"},
                operands={
                    "iteration": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="qft_step",
                                params={
                                    "num_qbits": Expression(expr="num_qbits-index")
                                },
                                inputs={
                                    "qbv": PortBinding(
                                        name="qbv_in",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="num_qbits-1"),
                                    ),
                                },
                                outputs={
                                    "qbv": PortBinding(
                                        name="qbv_out",
                                        start=Expression(expr="index"),
                                        end=Expression(expr="num_qbits-1"),
                                    ),
                                },
                            )
                        ],
                    )
                },
            ),
        ],
    ),
]
