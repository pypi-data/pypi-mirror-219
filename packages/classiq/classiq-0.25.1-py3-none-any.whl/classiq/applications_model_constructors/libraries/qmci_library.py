from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.standard_gates.standard_gates import ZGate
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
from classiq.applications_model_constructors.libraries.ampltitude_estimation_library import (
    AE_LIBRARY,
)
from classiq.applications_model_constructors.libraries.linear_pauli_rotation_library import (
    LPR_LIBRARY,
)

QMCI_LIBRARY = [
    *AE_LIBRARY,
    *LPR_LIBRARY,
    NativeFunctionDefinition(
        name="qmci",
        param_decls={
            "num_phase_qubits": Integer(),
            "num_unitary_qubits": Integer(),
        },
        port_declarations={
            "phase_port": PortDeclaration(
                name="phase_port",
                size=Expression(expr="num_phase_qubits"),
                direction=PortDeclarationDirection.Output,
            ),
            "unitary_port": PortDeclaration(
                name="unitary_port",
                size=Expression(expr="num_unitary_qubits"),
                direction=PortDeclarationDirection.Output,
            ),
        },
        operand_declarations={
            "sp_op": QuantumOperandDeclaration(
                name="sp_op",
                param_decls={"num_unitary_qubits": Integer()},
                port_declarations={
                    "reg": PortDeclaration(
                        name="reg",
                        direction="inout",
                        size=Expression(expr="num_unitary_qubits-1"),
                    ),
                    "ind": PortDeclaration(
                        name="ind",
                        direction="inout",
                        size=Expression(expr="1"),
                    ),
                },
            ),
        },
        body=[
            QuantumFunctionCall(
                function="amplitude_estimation",
                params={
                    "num_unitary_qubits": {"expr": "num_unitary_qubits"},
                    "num_phase_qubits": {"expr": "num_phase_qubits"},
                },
                outputs={
                    "phase_port": "phase_port_out",
                    "unitary_port": "unitary_port_out",
                },
                operands={
                    "oracle_op": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="ZGate",
                                function_params=ZGate(),
                                inputs={
                                    "TARGET": PortBinding(
                                        name="oq_in",
                                        start=Expression(expr="num_unitary_qubits-1"),
                                        end=Expression(expr="num_unitary_qubits-1"),
                                    ),
                                },
                                outputs={
                                    "TARGET": PortBinding(
                                        name="oq_out",
                                        start=Expression(expr="num_unitary_qubits-1"),
                                        end=Expression(expr="num_unitary_qubits-1"),
                                    ),
                                },
                            ),
                        ]
                    ),
                    "sp_op": QuantumLambdaFunction(
                        body=[
                            QuantumFunctionCall(
                                function="sp_op",
                                params={
                                    "num_unitary_qubits": Expression(
                                        expr="num_unitary_qubits"
                                    )
                                },
                                inputs={
                                    "reg": PortBinding(
                                        name="spq_in",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="num_unitary_qubits-2"),
                                    ),
                                    "ind": PortBinding(
                                        name="spq_in",
                                        start=Expression(expr="num_unitary_qubits-1"),
                                        end=Expression(expr="num_unitary_qubits-1"),
                                    ),
                                },
                                outputs={
                                    "reg": PortBinding(
                                        name="spq_out",
                                        start=Expression(expr="0"),
                                        end=Expression(expr="num_unitary_qubits-2"),
                                    ),
                                    "ind": PortBinding(
                                        name="spq_out",
                                        start=Expression(expr="num_unitary_qubits-1"),
                                        end=Expression(expr="num_unitary_qubits-1"),
                                    ),
                                },
                            )
                        ],
                    ),
                },
            ),
        ],
    ),
]
