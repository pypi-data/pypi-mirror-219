from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import Integer, Real
from classiq.interface.generator.functions.port_declaration import (
    PortDeclaration,
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)

H_FUNCTION = QuantumFunctionDeclaration(
    name="H",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


X_FUNCTION = QuantumFunctionDeclaration(
    name="X",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


Y_FUNCTION = QuantumFunctionDeclaration(
    name="Y",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)

Z_FUNCTION = QuantumFunctionDeclaration(
    name="Z",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


I_FUNCTION = QuantumFunctionDeclaration(
    name="I",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


S_FUNCTION = QuantumFunctionDeclaration(
    name="S",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


T_FUNCTION = QuantumFunctionDeclaration(
    name="T",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


SDG_FUNCTION = QuantumFunctionDeclaration(
    name="SDG",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


TDG_FUNCTION = QuantumFunctionDeclaration(
    name="TDG",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


PHASE_FUNCTION = QuantumFunctionDeclaration(
    name="PHASE",
    param_decls={"theta": Real()},
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


RX_FUNCTION = QuantumFunctionDeclaration(
    name="RX",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


RY_FUNCTION = QuantumFunctionDeclaration(
    name="RY",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


RZ_FUNCTION = QuantumFunctionDeclaration(
    name="RZ",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        )
    },
)


RXX_FUNCTION = QuantumFunctionDeclaration(
    name="RXX",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        )
    },
)


RYY_FUNCTION = QuantumFunctionDeclaration(
    name="RYY",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        )
    },
)


RZZ_FUNCTION = QuantumFunctionDeclaration(
    name="RZZ",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="2"),
        )
    },
)


CH_FUNCTION = QuantumFunctionDeclaration(
    name="CH",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CX_FUNCTION = QuantumFunctionDeclaration(
    name="CX",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CY_FUNCTION = QuantumFunctionDeclaration(
    name="CY",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CZ_FUNCTION = QuantumFunctionDeclaration(
    name="CZ",
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CRX_FUNCTION = QuantumFunctionDeclaration(
    name="CRX",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CRY_FUNCTION = QuantumFunctionDeclaration(
    name="CRY",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CRZ_FUNCTION = QuantumFunctionDeclaration(
    name="CRZ",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


CPHASE_FUNCTION = QuantumFunctionDeclaration(
    name="CPHASE",
    param_decls={
        "theta": Real(),
    },
    port_declarations={
        "target": PortDeclaration(
            name="target",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "control": PortDeclaration(
            name="control",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


SWAP_FUNCTION = QuantumFunctionDeclaration(
    name="SWAP",
    port_declarations={
        "qbit0": PortDeclaration(
            name="qbit0",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
        "qbit1": PortDeclaration(
            name="qbit1",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="1"),
        ),
    },
)


IDENTITY_FUNCTION = QuantumFunctionDeclaration(
    name="IDENTITY",
    param_decls={"port_size": Integer()},
    port_declarations={
        "p": PortDeclaration(
            name="p",
            direction=PortDeclarationDirection.Inout,
            size=Expression(expr="port_size"),
        )
    },
)


__all__ = [
    "H_FUNCTION",
    "X_FUNCTION",
    "Y_FUNCTION",
    "Z_FUNCTION",
    "I_FUNCTION",
    "S_FUNCTION",
    "T_FUNCTION",
    "SDG_FUNCTION",
    "TDG_FUNCTION",
    "PHASE_FUNCTION",
    "RX_FUNCTION",
    "RY_FUNCTION",
    "RZ_FUNCTION",
    "RXX_FUNCTION",
    "RYY_FUNCTION",
    "RZZ_FUNCTION",
    "CH_FUNCTION",
    "CX_FUNCTION",
    "CY_FUNCTION",
    "CZ_FUNCTION",
    "CRX_FUNCTION",
    "CRY_FUNCTION",
    "CRZ_FUNCTION",
    "CPHASE_FUNCTION",
    "SWAP_FUNCTION",
    "IDENTITY_FUNCTION",
]
