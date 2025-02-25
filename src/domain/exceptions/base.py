from dataclasses import dataclass


@dataclass(eq=False)
class DomainException(Exception):
    
    @property
    def message(self):
        return "An error has occurred in the domain"