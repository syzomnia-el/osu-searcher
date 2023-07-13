# -*- coding: utf-8 -*-
from typing import NamedTuple

from ui import Parser

__all__ = ['CommandParser']

Command = NamedTuple('Command', [('key', str), ('args', str)])


class CommandParser(Parser):
    """ The class implements the parser for the command line interface. """

    def parse(self) -> Command:
        """
        Parses the user input from the command line.
        The first part is the command keyword, and the rest are the arguments.
        If no argument, the argument is an empty string.

        Returns:
            The tuple of the command keyword and the arguments.
        """
        # Splits input string into the command and the keyword
        # For example, 'find 1' -> ('find', '1')
        key, *args = input().strip().lower().split(maxsplit=1)
        arg: str = args[0].strip() if args else ''
        return Command(key=key, args=arg)
