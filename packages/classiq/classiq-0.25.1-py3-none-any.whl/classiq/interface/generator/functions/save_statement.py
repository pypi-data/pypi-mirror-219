import pydantic

from classiq.interface.generator.functions.statement import Statement


class SaveStatement(Statement):
    saved_variable: str = pydantic.Field(
        description="The name of the variable to be saved."
    )
