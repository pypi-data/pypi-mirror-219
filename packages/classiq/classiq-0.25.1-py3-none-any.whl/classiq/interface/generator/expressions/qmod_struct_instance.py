import types
from typing import TYPE_CHECKING, Any, Mapping

from classiq.exceptions import ClassiqValueError

if TYPE_CHECKING:
    from classiq.interface.generator.expressions.expression_types import ExpressionValue
    from classiq.interface.generator.types.struct_declaration import StructDeclaration


class QmodStructInstance:
    def __init__(
        self,
        struct_declaration: "StructDeclaration",
        fields: Mapping[str, "ExpressionValue"],
    ):
        if set(struct_declaration.variables.keys()) != {
            field for field in fields.keys()
        }:
            raise ClassiqValueError(
                f"Invalid fields for {struct_declaration.name} instance"
            )
        self.struct_declaration = struct_declaration
        self._fields = fields

    @property
    def fields(self) -> Mapping[str, Any]:
        return types.MappingProxyType(self._fields)

    def __repr__(self) -> str:
        return repr(self._fields)
