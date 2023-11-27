# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

__all__ = ['Parser', 'Printer']


class Parser(metaclass=ABCMeta):
    """ The abstract class defines an interface how to parse the user input. """

    @abstractmethod
    def input(self) -> str:
        """ Gets the user input. """
        pass

    @abstractmethod
    def parse(self) -> object:
        """ Parses the user input. """
        pass


class Printer(metaclass=ABCMeta):
    """ The abstract class defines an interface how to print the output. """

    @abstractmethod
    def print(self, output: object) -> None:
        """ Prints the output. """
        pass
