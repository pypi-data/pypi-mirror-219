from classiq.interface.generator.expressions.classical_enum import ClassicalEnum


class Pauli(ClassicalEnum):
    I = 0  # noqa: E741
    X = 1
    Y = 2
    Z = 3

    def to_name(self) -> str:
        return f"Pauli_{self.name}"
