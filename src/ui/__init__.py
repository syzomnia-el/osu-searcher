# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

__all__ = ['Parser']


class Parser(metaclass=ABCMeta):
    """ The abstract class defines an interface how to parse the user input. """

    @abstractmethod
    def parse(self):
        """ Parses the user input. """
        pass
