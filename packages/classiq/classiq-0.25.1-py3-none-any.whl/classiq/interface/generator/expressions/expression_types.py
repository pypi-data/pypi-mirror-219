from typing import Union

from sympy import Expr
from sympy.logic.boolalg import Boolean

from classiq.interface.generator.expressions.operand_list_identifier import (
    OperandListProxy,
)
from classiq.interface.generator.expressions.qmod_struct_instance import (
    QmodStructInstance,
)
from classiq.interface.generator.expressions.type_proxy import TypeProxy

RuntimeConstant = Union[
    int, float, list, bool, QmodStructInstance, OperandListProxy, TypeProxy
]
RuntimeExpression = Union[Expr, Boolean]
ExpressionValue = Union[RuntimeConstant, RuntimeExpression]
