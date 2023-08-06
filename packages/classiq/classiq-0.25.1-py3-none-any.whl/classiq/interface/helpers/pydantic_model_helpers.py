from typing import Any, Dict, Protocol, Sequence, TypeVar

import pydantic


def get_discriminator_field(default: str, **kwargs) -> Any:
    return pydantic.Field(default_factory=lambda: default, **kwargs)


class Nameable(Protocol):
    name: str


NameableType = TypeVar("NameableType", bound=Nameable)


def nameables_to_dict(nameables: Sequence[NameableType]) -> Dict[str, NameableType]:
    return {value.name: value for value in nameables}
