# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from typing import NamedTuple

from ui import Parser, Printer

__all__ = ['CommandParser', 'BeatmapPrinter']

Command = NamedTuple('Command', [('key', str), ('args', list[str])])


class CommandParser(Parser):
    """
    The class implements the parser for the command line interface.
    Using the standard library argparse to parse the user input.
    """
    _parser: ArgumentParser

    def __init__(self):
        """
        Initialize the parser.

        User input format: <key> [arg1] [arg2] ...
        """
        self._parser = ArgumentParser()
        self._parser.add_argument('key', type=str, help='The command key.')
        self._parser.add_argument('args', nargs='*', help='The command arguments.')

    def parse(self) -> Command:
        """ Parse the user input and return the command. """
        input_args = input('>>> ').split()
        args = self._parser.parse_args(input_args)
        key = args.key
        arg = args.args[0] if len(args.args) > 1 else ''
        return Command(key, arg)


class BeatmapPrinter(Printer):
    """ The class implements the printer for the command line interface. """
    _WIDTH_SID = 8
    _WIDTH_ARTIST = 42
    _PARTING_LINE = '-' * 100

    def print(self, beatmaps: list) -> None:
        """
        Prints the beatmaps as below:

            sid | artist | name \n
            \u005c-------------------------\n
            [<sid> | <artist> | <name>]\n
            ...
            total: <total_number>

        Parameters:
            beatmaps: The beatmaps to print.
        """
        print(f'{"sid":<{self._WIDTH_SID}} | {"artist":<{self._WIDTH_ARTIST}} | {"name"}')
        print(f'{self._PARTING_LINE}')

        for i in beatmaps:
            print(f'{i.sid:<{self._WIDTH_SID}} | {i.artist:<{self._WIDTH_ARTIST}.{self._WIDTH_ARTIST}} | {i.name}')

        print(f'total: {len(beatmaps)}')
