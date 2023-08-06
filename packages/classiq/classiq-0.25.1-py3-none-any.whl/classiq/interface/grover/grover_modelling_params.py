import pydantic
from pydantic import BaseModel

from classiq.interface.generator.oracles import ArithmeticOracle


class GroverParams(BaseModel):
    oracle: ArithmeticOracle = pydantic.Field(
        description="An arithmatic oracle for the grover search."
    )
    num_shots: int = pydantic.Field(description="The number circuit executions.")
    num_reps: int = pydantic.Field(
        default=1, description="The number of repetitions of the " "grover block."
    )
