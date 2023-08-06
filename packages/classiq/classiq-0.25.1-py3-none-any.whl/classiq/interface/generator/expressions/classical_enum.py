import abc
import enum
from typing import Dict


class ABCEnumMeta(enum.EnumMeta, abc.ABCMeta):
    pass


class ClassicalEnum(int, abc.ABC, enum.Enum, metaclass=ABCEnumMeta):
    @abc.abstractmethod
    def to_name(self) -> str:
        raise NotImplementedError()

    @classmethod
    def enum_values(cls) -> Dict[str, int]:
        return {cls.to_name(elem): elem.value for elem in cls}
