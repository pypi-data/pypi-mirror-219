from __future__ import annotations

from typing import Dict, Mapping, Optional, Set, Union

import pydantic
from pydantic import BaseModel, Extra

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)


class OperandIdentifier(BaseModel):
    name: str
    index: Expression


class FunctionCall(BaseModel):
    function: Union[str, OperandIdentifier] = pydantic.Field(
        description="The function that is called"
    )
    params: Dict[str, Expression] = pydantic.Field(default_factory=dict)
    _func_decl: Optional[FunctionDeclaration] = pydantic.PrivateAttr(default=None)

    @property
    def func_decl(self) -> Optional[FunctionDeclaration]:
        return self._func_decl

    def set_func_decl(self, fd: Optional[FunctionDeclaration]) -> None:
        self._func_decl = fd

    def resolve_function_decl(
        self,
        function_dict: Mapping[str, FunctionDeclaration],
    ) -> None:
        if self.func_decl is not None:
            return
        func_decl = function_dict.get(self.func_name)
        if func_decl is None:
            raise ValueError(
                f"Error resolving function {self.func_name}, the function is not found in included library."
            )
        self.set_func_decl(func_decl)
        check_params_against_declaration(
            set(self.params.keys()),
            set(func_decl.param_decls.keys()),
            func_decl.name,
        )

    def get_param_exprs(self) -> Dict[str, Expression]:
        return self.params

    @property
    def func_name(self) -> str:
        if isinstance(self.function, OperandIdentifier):
            return self.function.name
        return self.function

    class Config:
        extra = Extra.forbid


def check_params_against_declaration(
    call_params: Set[str], param_decls: Set[str], callee_name: str
) -> None:
    unknown_params = call_params - param_decls
    if unknown_params:
        raise ValueError(
            f"Unknown parameters {unknown_params} in call to {callee_name!r}."
        )

    missing_params = param_decls - call_params
    if missing_params:
        raise ValueError(
            f"Missing parameters {missing_params} in call to {callee_name!r}."
        )
