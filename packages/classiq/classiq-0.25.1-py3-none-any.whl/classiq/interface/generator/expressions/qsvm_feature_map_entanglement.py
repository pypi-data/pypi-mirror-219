from classiq.interface.generator.expressions.classical_enum import ClassicalEnum


class QSVMFeatureMapEntanglement(ClassicalEnum):
    FULL = 0
    LINEAR = 1
    CIRCULAR = 2
    SCA = 3
    PAIRWISE = 4

    def to_name(self) -> str:
        return f"QSVMFeatureMapEntanglement_{self.name}"
