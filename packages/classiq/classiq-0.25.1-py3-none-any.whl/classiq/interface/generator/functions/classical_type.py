from abc import abstractmethod
from typing import Any, Dict, List, Literal, Union

import pydantic
from pydantic import Extra, Field
from sympy import IndexedBase, Symbol
from typing_extensions import Annotated

from classiq.interface.generator.expressions.expression_types import RuntimeExpression
from classiq.interface.generator.expressions.ladder_operator import (
    LadderOperator as LadderOperatorEnum,
)
from classiq.interface.generator.expressions.pauli import Pauli as PauliEnum
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)
from classiq.interface.helpers.pydantic_model_helpers import get_discriminator_field

NamedSymbol = Union[IndexedBase, Symbol]


class ClassicalType(HashablePydanticBaseModel):
    def as_symbolic(self, name: str) -> Union[NamedSymbol, List[NamedSymbol]]:
        return Symbol(name)

    @property
    @abstractmethod
    def default_value(self) -> Any:
        raise NotImplementedError(
            f"{self.__class__.__name__} type has no default value"
        )

    class Config:
        extra = Extra.forbid


class Integer(ClassicalType):
    kind: Literal["int"] = get_discriminator_field(default="int")

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, integer=True)

    @property
    def default_value(self) -> int:
        return 0


class Real(ClassicalType):
    kind: Literal["real"] = get_discriminator_field(default="real")

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, real=True)

    @property
    def default_value(self) -> float:
        return 0


class Bool(ClassicalType):
    kind: Literal["bool"] = get_discriminator_field(default="bool")

    @property
    def default_value(self) -> bool:
        return False


class ClassicalList(ClassicalType):
    kind: Literal["list"] = get_discriminator_field(default="list")
    element_type: "ConcreteClassicalType"

    def as_symbolic(self, name: str) -> Symbol:
        return IndexedBase(name)

    @property
    def default_value(self) -> List:
        return []


class Pauli(ClassicalType):
    kind: Literal["pauli"] = get_discriminator_field(default="pauli")

    @property
    def default_value(self) -> PauliEnum:
        return PauliEnum.I


class TypeProxy(ClassicalType):
    kind: Literal["type_proxy"] = get_discriminator_field(default="type_proxy")

    @property
    def default_value(self) -> Any:
        return super().default_value


class Struct(ClassicalType):
    kind: Literal["struct_instance"] = get_discriminator_field(
        default="struct_instance"
    )
    name: str = pydantic.Field(description="The struct type of the instance")

    @property
    def default_value(self) -> Any:
        return super().default_value


class ClassicalArray(ClassicalType):
    kind: Literal["array"] = get_discriminator_field(default="array")
    element_type: "ConcreteClassicalType"
    size: pydantic.PositiveInt

    def as_symbolic(self, name: str) -> list:
        return [self.element_type.as_symbolic(f"{name}_{i}") for i in range(self.size)]

    @property
    def default_value(self) -> Any:
        return super().default_value


class OpaqueHandle(ClassicalType):
    @property
    def default_value(self) -> int:
        return 0


class VQEResult(OpaqueHandle):
    kind: Literal["vqe_result"] = get_discriminator_field(default="vqe_result")


class Histogram(OpaqueHandle):
    kind: Literal["histogram"] = get_discriminator_field(default="histogram")


class Estimation(OpaqueHandle):
    kind: Literal["estimation_result"] = get_discriminator_field(
        default="estimation_result"
    )


class LadderOperator(ClassicalType):
    kind: Literal["ladder_operator"] = get_discriminator_field(
        default="ladder_operator"
    )

    @property
    def default_value(self) -> LadderOperatorEnum:
        return LadderOperatorEnum.PLUS


ConcreteClassicalType = Annotated[
    Union[
        Integer,
        Real,
        Bool,
        ClassicalList,
        Pauli,
        TypeProxy,
        Struct,
        ClassicalArray,
        VQEResult,
        Histogram,
        Estimation,
        LadderOperator,
    ],
    Field(discriminator="kind"),
]
ClassicalList.update_forward_refs()
ClassicalArray.update_forward_refs()


def as_symbolic(symbols: Dict[str, ClassicalType]) -> Dict[str, RuntimeExpression]:
    return {
        param_name: param_type.as_symbolic(param_name)
        for param_name, param_type in symbols.items()
    }


class QmodPyObject:
    pass
