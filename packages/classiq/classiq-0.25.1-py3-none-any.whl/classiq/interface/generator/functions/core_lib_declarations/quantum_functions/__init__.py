from classiq.interface.generator.functions.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict

from .atomic_quantum_functions import *  # noqa: F403
from .exponentiation_functions import *  # noqa: F403

QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS.update(
    nameables_to_dict(
        [
            func
            for func in vars().values()
            if isinstance(func, QuantumFunctionDeclaration)
        ]
    )
)
