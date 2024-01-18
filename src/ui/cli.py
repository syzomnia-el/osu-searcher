# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from typing import NamedTuple

from model import Beatmap
from ui import Parser, Printer

__all__ = ['CommandParser', 'BeatmapPrinter']


class Command(NamedTuple):
    """ The class represents a command. """
    key: str
    args: list[str]


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
        self._parser.add_argument(
            'key',
            type=str,
            help='The command key.',
            choices=['check', 'exit', 'find', 'flush', 'list', 'path']
        )
        self._parser.add_argument(
            'args',
            nargs='*',
            help='The command arguments.'
        )
        self._parser.error = self._handle_error

    def input(self) -> str:
        """ Get the user input. """
        return input('>>> ').strip()

    def parse(self) -> Command:
        """ Parse the user input and return the command. """
        input_args = self.input().split()
        args = self._parser.parse_args(input_args)
        return Command(args.key, args.args)

    @staticmethod
    def _handle_error(_) -> Command:
        """ Handle the error message. """
        return Command('', [''])


class BeatmapPrinter(Printer):
    """ The class implements the printer for the command line interface. """
    _WIDTH_SID = 8
    _WIDTH_ARTIST = 42
    _PARTING_LINE = '-' * (_WIDTH_SID + _WIDTH_ARTIST + 10)

    def print(self, beatmaps: list[Beatmap]) -> None:
        """
        Prints the beatmaps as below.

            sid | artist | name \n
            \u005c-------------------------\n
            [<sid> | <artist> | <name>]\n
            ...
            total: <total_number>

        :param beatmaps: The beatmaps to print.
        """
        if not isinstance(beatmaps, list) or not all(isinstance(i, Beatmap) for i in beatmaps):
            print('Invalid beatmaps.')
            return

        print(f'{'sid':<{self._WIDTH_SID}} | {'artist':<{self._WIDTH_ARTIST}} | name')
        print(self._PARTING_LINE)

        for i in beatmaps:
            print(f'{i.sid:<{self._WIDTH_SID}} | {i.artist:<{self._WIDTH_ARTIST}.{self._WIDTH_ARTIST}} | {i.name}')

        print(f'total: {len(beatmaps)}')
