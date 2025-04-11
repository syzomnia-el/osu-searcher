# -*- coding: utf-8 -*-
import os
import sys
from abc import ABC, abstractmethod

__all__ = ['IOUtils', 'Parser', 'Printer']

from typing import Self


class IOUtils(ABC):
    """ The abstract class defines an interface how to interact with the user. """

    def __new__(cls) -> Self:
        """ The class cannot be instantiated. """
        raise NotImplementedError('The class cannot be instantiated.')

    @staticmethod
    @abstractmethod
    def input() -> str:
        """ Get the user input. """

    @staticmethod
    def is_valid_path(path: str) -> bool:
        """ Check if the path is valid. """
        return path and os.path.isdir(path)

    @staticmethod
    def exit(code: int = 0) -> None:
        """ Exit the program. """
        sys.exit(code)


class Parser(ABC):
    """ The abstract class defines an interface how to parse the user input. """

    @abstractmethod
    def parse(self) -> object:
        """ Parses the user input. """


class Printer(ABC):
    """ The abstract class defines an interface how to print the output. """

    @abstractmethod
    def print(self, output: object) -> None:
        """ Prints the output. """
