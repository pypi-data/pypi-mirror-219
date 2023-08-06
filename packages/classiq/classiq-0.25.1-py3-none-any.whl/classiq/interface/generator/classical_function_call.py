from typing import Any, Optional

import pydantic

from classiq.interface.generator.function_call import FunctionCall
from classiq.interface.generator.functions.classical_function_declaration import (
    ClassicalFunctionDeclaration,
)
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)

from classiq.exceptions import ClassiqValueError


class ClassicalFunctionCall(FunctionCall):
    _func_decl: Optional[ClassicalFunctionDeclaration] = pydantic.PrivateAttr(
        default=None
    )

    _return_value: Optional[Any] = pydantic.PrivateAttr(default=None)

    @property
    def func_decl(self) -> Optional[ClassicalFunctionDeclaration]:
        return self._func_decl

    def set_func_decl(self, fd: Optional[FunctionDeclaration]) -> None:
        if fd is not None and not isinstance(fd, ClassicalFunctionDeclaration):
            raise ClassiqValueError(
                "the declaration of a quantum function call cannot be set to a non-quantum function declaration."
            )
        super().set_func_decl(fd)
