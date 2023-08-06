from classiq.interface.generator.functions.classical_type import (
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.types.struct_declaration import StructDeclaration

COMBINATORIAL_OPTIMIZATION_SOLUTION = StructDeclaration(
    name="CombinatorialOptimizationSolution",
    variables={
        "probability": Real(),
        "cost": Real(),
        "solution": ClassicalList(element_type=Integer()),
        "count": Integer(),
    },
)
