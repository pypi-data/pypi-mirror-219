import ast
from typing import Any, Mapping, Optional, Type

import pydantic
from pydantic import PrivateAttr

from classiq.interface.generator.expressions.atomic_expression_functions import (
    SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS,
)
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.sympy_supported_expressions import (
    SYMPY_SUPPORTED_EXPRESSIONS,
)
from classiq.interface.generator.function_params import validate_expression_str
from classiq.interface.helpers.hashable_pydantic_base_model import (
    HashablePydanticBaseModel,
)

from classiq.exceptions import ClassiqError


class Expression(HashablePydanticBaseModel):
    expr: str
    _evaluated_expr: Optional[EvaluatedExpression] = PrivateAttr(default=None)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self._try_to_immediate_evaluate()

    @pydantic.validator("expr")
    def validate_expression(cls, expr: str) -> str:
        supported_functions = (
            SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS | SYMPY_SUPPORTED_EXPRESSIONS
        )
        validate_expression_str(
            "expression", expr, supported_functions=supported_functions
        )
        return expr

    def is_evaluated(self) -> bool:
        return self._evaluated_expr is not None

    def as_constant(self, constant_type: Type) -> Any:
        if self._evaluated_expr is None:
            raise ClassiqError(f"Trying to access unevaluated value {self.expr}")

        return self._evaluated_expr.as_constant_type(constant_type)

    def to_int_value(self) -> int:
        return self.as_constant(int)

    def to_bool_value(self) -> bool:
        return self.as_constant(bool)

    def to_float_value(self) -> float:
        return self.as_constant(float)

    def to_struct_dict(self) -> Mapping[str, Any]:
        if self._evaluated_expr is None:
            raise ClassiqError(f"Trying to access unevaluated value {self.expr}")

        return self._evaluated_expr.to_struct_dict()

    def _try_to_immediate_evaluate(self) -> None:
        try:
            result = ast.literal_eval(self.expr)
            if isinstance(result, (int, float, bool)):
                self._evaluated_expr = EvaluatedExpression(value=result)
        except Exception:  # nosec B110
            pass

    class Config:
        frozen = True
