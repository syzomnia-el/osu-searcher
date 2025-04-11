# -*- coding: utf-8 -*-
import os
from argparse import ArgumentParser
from typing import NamedTuple, Self, override

from model import Beatmap
from ui import IOUtils, Parser, Printer

__all__ = ['CLIUtils', 'CommandParser', 'BeatmapPrinter']


class CLIUtils(IOUtils):
    """ The class implements the utility for the command line interface. """

    def __new__(cls) -> Self:
        """ The class cannot be instantiated. """
        raise NotImplementedError('The class cannot be instantiated.')

    @staticmethod
    @override
    def input() -> str:
        """ Get the user input. """
        return input('>>> ').strip()

    @staticmethod
    def clear_screen() -> None:
        """ Clears the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause() -> None:
        """ Pauses the program until the user presses the Enter key. """
        input('Press Enter to continue...')


class Command(NamedTuple):
    """ The class represents a command. """
    key: str = ''
    args: list[str] | None = None


class CommandParser(Parser):
    """
    The class implements the parser for the command line interface.
    Using the standard library argparse to parse the user input.
    """
    _parser: ArgumentParser

    def __new__(cls) -> Self:
        """
        Initialize the parser.

        User input format: <key> [arg1] [arg2] ...
        """
        cls._parser = ArgumentParser()
        cls._parser.add_argument(
            'key',
            type=str,
            help='The command key.',
            choices=['check', 'exit', 'find', 'flush', 'list', 'path']
        )
        cls._parser.add_argument(
            'args',
            nargs='*',
            help='The command arguments.'
        )
        cls._parser.error = lambda _: Command()
        return super().__new__(cls)

    @override
    def parse(self) -> Command:
        """ Parse the user input and return the command. """
        input_args = CLIUtils.input().split()
        args = self._parser.parse_args(input_args)
        return Command(args.key, args.args)


class BeatmapPrinter(Printer):
    """ The class implements the printer for the command line interface. """
    _WIDTH_SID = 8
    _WIDTH_ARTIST = 42
    _PARTING_LINE = '-' * (_WIDTH_SID + _WIDTH_ARTIST + 10)

    @override
    def print(self, output: list[Beatmap]) -> None:
        """
        Prints the beatmaps as below.

            sid    | artist   | name   \n
            \--------------------------\n
            [<sid> | <artist> | <name>]\n
            ...
            total: <total_number>

        :param output: The beatmaps to print.
        """
        if not isinstance(output, list) or not all(isinstance(i, Beatmap) for i in output):
            print('Invalid beatmaps.')
            return

        print(f"{'sid':<{self._WIDTH_SID}} | {'artist':<{self._WIDTH_ARTIST}} | name")
        print(self._PARTING_LINE)
        for i in output:
            print(
                f'{i.sid:<{self._WIDTH_SID}} | '
                f'{i.artist:<{self._WIDTH_ARTIST}.{self._WIDTH_ARTIST}} | '
                f'{i.name}'
            )
        print(f'total: {len(output)}')
