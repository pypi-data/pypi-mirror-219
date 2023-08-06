from classiq.interface.generator.expressions.classical_enum import ClassicalEnum


class Optimizer(ClassicalEnum):
    COBYLA = 1
    SPSA = 2
    L_BFGS_B = 3
    NELDER_MEAD = 4
    ADAM = 5

    def to_name(self) -> str:
        return f"Optimizer_{self.name}"
