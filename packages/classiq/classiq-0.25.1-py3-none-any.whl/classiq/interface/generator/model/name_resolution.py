from typing import Any, Mapping

from classiq.interface.generator.classical_function_call import ClassicalFunctionCall
from classiq.interface.generator.functions import (
    QuantumFunctionDeclaration,
    SynthesisNativeFunctionDefinition,
)
from classiq.interface.generator.quantum_function_call import (
    SynthesisQuantumFunctionCall,
)
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall
from classiq.interface.generator.visitor import Transformer

from classiq import ClassicalFunctionDeclaration


class FunctionCallResolver(Transformer):
    def __init__(
        self,
        classical_function_dict: Mapping[str, ClassicalFunctionDeclaration],
        quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
    ):
        self._classical_function_dict = classical_function_dict
        self._quantum_function_dict = quantum_function_dict

    def visit_ClassicalFunctionCall(
        self, fc: ClassicalFunctionCall
    ) -> ClassicalFunctionCall:
        fc.resolve_function_decl(self._classical_function_dict)
        return fc

    def visit_QuantumInvokerCall(self, fc: QuantumInvokerCall) -> QuantumInvokerCall:
        self.visit_ClassicalFunctionCall(fc)
        fc.check_quantum_function_decl(self._quantum_function_dict)
        return fc

    def visit_SynthesisQuantumFunctionCall(
        self, fc: SynthesisQuantumFunctionCall
    ) -> SynthesisQuantumFunctionCall:
        fc.resolve_function_decl(self._quantum_function_dict)
        self.visit_BaseModel(fc)
        return fc

    def visit_SynthesisNativeFunctionDefinition(
        self, func_def: SynthesisNativeFunctionDefinition
    ):
        curr_dict = self._quantum_function_dict
        self._quantum_function_dict = {
            **self._quantum_function_dict,
            **func_def.operand_declarations,
        }
        self.visit_BaseModel(func_def)
        self._quantum_function_dict = curr_dict
        return func_def


def resolve_function_calls(
    root: Any,
    classical_function_dict: Mapping[str, ClassicalFunctionDeclaration],
    quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    FunctionCallResolver(
        {
            **ClassicalFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **classical_function_dict,
        },
        {
            **QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **quantum_function_dict,
        },
    ).visit(root)
