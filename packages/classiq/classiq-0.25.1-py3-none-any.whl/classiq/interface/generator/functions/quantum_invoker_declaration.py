import pydantic

from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.functions.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)


class QuantumInvokerDeclaration(ClassicalFunctionDeclaration):
    target_function_declaration: QuantumFunctionDeclaration = pydantic.Field(
        description="The invoked quantum function's declaration."
    )
