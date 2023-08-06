import dataclasses
from typing import Optional

import numpy as np

from classiq.interface.executor.optimizer_preferences import OptimizerType


@dataclasses.dataclass
class ChemistryExecutionParameters:
    num_shots: int
    optimizer: OptimizerType
    initial_point: Optional[np.ndarray]
    max_iteration: int
    tolerance: float = dataclasses.field(default=0.0)
    step_size: float = dataclasses.field(default=0.0)
    skip_compute_variance: bool = dataclasses.field(default=False)
