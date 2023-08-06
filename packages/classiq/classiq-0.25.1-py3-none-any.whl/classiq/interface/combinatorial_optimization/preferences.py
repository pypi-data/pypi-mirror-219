from typing import List, Literal, Optional, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.combinatorial_optimization.solver_types import QSolver
from classiq.interface.generator.model.constraints import (
    Constraints,
    OptimizationParameter,
)
from classiq.interface.generator.model.preferences.preferences import (
    Preferences,
    TranspilationOption,
)


def get_default_constraints() -> Constraints:
    return Constraints(optimization_parameter=OptimizationParameter.WIDTH)


def get_default_preferences() -> Preferences:
    return Preferences(transpilation_option=TranspilationOption.NONE, random_seed=-1)


class QAOAPreferences(BaseModel):
    qsolver: Literal[
        QSolver.QAOAPenalty, QSolver.QAOAMixer, QSolver.Custom
    ] = pydantic.Field(
        default=QSolver.QAOAPenalty,
        description="Indicates whether to use QAOA with penalty terms (QAOAPenalty), "
        "constraints-preserving QAOA (QAOAMixer) or a user-defined ansatz.",
    )
    qaoa_reps: pydantic.PositiveInt = pydantic.Field(
        default=1, description="Number of layers in qaoa ansatz."
    )
    penalty_energy: float = pydantic.Field(
        default=None,
        description="Penalty energy for invalid solutions. The value affects "
        "the converges rate. Small positive values are preferred",
    )
    initial_state: Optional[List[int]] = pydantic.Field(
        default=None,
        description="Initial state in QAOA ansatz. The state should be a single basis state in the "
        "computational basis. For problems with binary or integer variables the string "
        "consists of binary or integer values respectively.",
    )

    constraints: Constraints = pydantic.Field(default_factory=get_default_constraints)
    preferences: Preferences = pydantic.Field(default_factory=get_default_preferences)

    @pydantic.validator("penalty_energy", pre=True, always=True)
    def check_penalty_energy(cls, penalty_energy, values):
        qsolver = values.get("qsolver")
        if penalty_energy is not None and qsolver not in (
            QSolver.QAOAPenalty,
            QSolver.Custom,
        ):
            raise ValueError(
                "Use penalty_energy only for QSolver.QAOAPenalty or QSolver.Custom."
            )

        if penalty_energy is None and qsolver == QSolver.QAOAPenalty:
            penalty_energy = 2

        return penalty_energy


class GASPreferences(pydantic.BaseModel):
    qsolver: Literal[QSolver.GAS] = pydantic.Field(
        default=QSolver.GAS,
        description="Indicates the qsolver type.",
    )
    num_result_qubits: int = 0
    preferences: Preferences = pydantic.Field(
        default=Preferences(transpilation_option=TranspilationOption.NONE)
    )


QSolverPreferences = Union[QAOAPreferences, GASPreferences]
