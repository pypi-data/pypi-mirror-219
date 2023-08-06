from typing import ClassVar, Dict

import pydantic

from classiq.interface.generator.functions.classical_type import ConcreteClassicalType
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)


class StructDeclaration(HashablePydanticBaseModel):
    name: str

    variables: Dict[str, ConcreteClassicalType] = pydantic.Field(
        default_factory=dict,
        description="Dictionary of variable names and their classical type",
    )

    BUILTIN_STRUCT_DECLARATIONS: ClassVar[Dict[str, "StructDeclaration"]] = {}
