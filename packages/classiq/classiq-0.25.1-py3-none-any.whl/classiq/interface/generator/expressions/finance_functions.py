from typing import Dict

from classiq.interface.generator.expressions.classical_enum import ClassicalEnum


class FinanceFunction(ClassicalEnum):
    VAR = 0
    SHORTFALL = 1
    X_SQUARE = 2
    EUROPEAN_CALL_OPTION = 3

    def to_name(self) -> str:
        return f"Finance_Function_{self.name}"

    @staticmethod
    def from_string(func_str: str) -> "FinanceFunction":
        return FINANCE_FUNCTION_STRING[func_str]


FINANCE_FUNCTION_STRING: Dict[str, FinanceFunction] = {
    "var": FinanceFunction.VAR,
    "expected short fall": FinanceFunction.SHORTFALL,
    "x**2": FinanceFunction.X_SQUARE,
    "european call option": FinanceFunction.EUROPEAN_CALL_OPTION,
}
