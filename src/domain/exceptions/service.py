from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(eq=False)
class IgnoredMessageExistException(DomainException):

    @property
    def message(self):
        return "The ignored message already exists"