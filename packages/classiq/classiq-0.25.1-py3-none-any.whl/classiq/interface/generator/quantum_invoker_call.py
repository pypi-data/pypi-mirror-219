from typing import Dict, Mapping, Optional

import pydantic

from classiq.interface.generator.classical_function_call import ClassicalFunctionCall
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_call import check_params_against_declaration
from classiq.interface.generator.functions import QuantumFunctionDeclaration
from classiq.interface.generator.functions.quantum_invoker_declaration import (
    QuantumInvokerDeclaration,
)


class QuantumInvokerCall(ClassicalFunctionCall):
    target_function: str = pydantic.Field(
        description="The name of the quantum function to invoke"
    )

    target_params: Dict[str, Expression] = pydantic.Field(default_factory=dict)

    _func_decl: Optional[QuantumInvokerDeclaration] = pydantic.PrivateAttr(default=None)

    def check_quantum_function_decl(
        self,
        function_dict: Mapping[str, QuantumFunctionDeclaration],
    ):
        if self.target_function not in function_dict:
            raise ValueError(
                f"Error resolving function {self.target_function}, the function is not found in included library."
            )

        check_params_against_declaration(
            set(self.target_params.keys()),
            set(function_dict[self.target_function].param_decls),
            self.target_function,
        )
