from typing import Optional, Union

import pydantic

from classiq.interface.generator.classical_function_call import ClassicalFunctionCall
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.statement import Statement
from classiq.interface.generator.quantum_invoker_call import QuantumInvokerCall

ConcreteExpression = Union[Expression, QuantumInvokerCall, ClassicalFunctionCall]


class ExpressionStatement(Statement):
    invoked_expression: ConcreteExpression = pydantic.Field(
        description="The expression this statement invokes."
    )

    _evaluation_result: Optional[EvaluatedExpression] = pydantic.PrivateAttr(
        default=None
    )
