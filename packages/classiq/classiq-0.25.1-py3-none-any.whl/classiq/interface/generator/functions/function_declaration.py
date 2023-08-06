import abc
from typing import Dict, Mapping, Union

import pydantic
from pydantic.main import BaseModel

from classiq.interface.generator.functions.classical_type import ConcreteClassicalType
from classiq.interface.generator.functions.port_declaration import PortDeclaration

UNRESOLVED_SIZE = 1000


class FunctionDeclaration(BaseModel, abc.ABC):
    """
    Facilitates the creation of a common function interface object.
    """

    name: str = pydantic.Field(description="The name of the function")

    param_decls: Dict[str, ConcreteClassicalType] = pydantic.Field(
        description="The expected interface of the functions parameters",
        default_factory=dict,
    )

    @staticmethod
    def _validate_declaration_names(
        declarations: Mapping[str, Union["FunctionDeclaration", PortDeclaration]],
        declaration_name: str,
    ) -> None:
        if not all(
            [name == declaration.name for (name, declaration) in declarations.items()]
        ):
            raise ValueError(
                f"{declaration_name} declaration names should match the keys of their names."
            )

    class Config:
        extra = pydantic.Extra.forbid


class OperandDeclaration(FunctionDeclaration):
    is_list: bool = pydantic.Field(
        description="Indicate whether the operand expects an unnamed list of lambdas",
        default=False,
    )


FunctionDeclaration.update_forward_refs()
