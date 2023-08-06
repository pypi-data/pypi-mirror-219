"""
Provides a common class for crateman errors.
"""

from abc import abstractmethod

class CratemanException(Exception):
    """
    Base class for every `crateman` error possible.
    If crateman error was thrown - that is a usage error.
    If any other python exception was thrown - that is a crateman bug, and should be reported.
    """

    def __init__(self, exit_code: int):
        super().__init__()
        self.exit_code = exit_code

    @abstractmethod
    def __str__(self) -> str: pass
