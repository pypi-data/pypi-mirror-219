from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Pauli,
    Real,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclaration,
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.generator.types.builtin_struct_declarations.pauli_struct_declarations import (
    Hamiltonian,
)

SINGLE_PAULI_EXPONENT_FUNCTION = QuantumFunctionDeclaration(
    name="single_pauli_exponent",
    param_decls={
        "pauli_string": ClassicalList(element_type=Pauli()),
        "coefficient": Real(),
    },
    port_declarations={
        "qbv": PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="len(pauli_string)"),
        )
    },
)


SUZUKI_TROTTER_FUNCTION = QuantumFunctionDeclaration(
    name="suzuki_trotter",
    param_decls={
        "pauli_operator": Hamiltonian(),
        "evolution_coefficient": Real(),
        "order": Integer(),
        "repetitions": Integer(),
    },
    port_declarations={
        "qbv": PortDeclaration(
            name="qbv",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="len(get_field(pauli_operator[0], pauli))"),
        )
    },
)

__all__ = ["SINGLE_PAULI_EXPONENT_FUNCTION", "SUZUKI_TROTTER_FUNCTION"]
