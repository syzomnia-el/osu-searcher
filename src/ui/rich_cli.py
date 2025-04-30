# -*- coding: utf-8 -*-
import os
from argparse import ArgumentParser
from functools import partial
from typing import NamedTuple, Self, override

from model import Beatmap
from ui import IOUtils, Parser, Printer

try:
    from rich import traceback
    from rich.console import Console
    from rich.table import Table
    from rich.theme import Theme
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        'The rich library is not installed.'
        ' Please install it by running `python -m pip install rich`.'
    )

__all__ = ['CLIRichUtils', 'CommandRichParser', 'BeatmapRichPrinter', 'console']

traceback.install(show_locals=True, word_wrap=True)

console = Console(theme=Theme(
    {
        'info': 'bold blue',
        'success': 'bold green',
        'warning': 'bold yellow',
        'error': 'bold red',
        'debug': 'bold grey50'
    }
))
console.info = partial(console.print, style='info')
console.success = partial(console.print, style='success')
console.warning = partial(console.print, style='warning')
console.error = partial(console.print, style='error')
console.debug = partial(console.print, style='debug')


class CLIRichUtils(IOUtils):
    """
    The class implements the utility for the command line interface.
    Using the library `rich` to print rich-text.
    """

    def __new__(cls) -> Self:
        """ The class cannot be instantiated. """
        raise NotImplementedError('The class cannot be instantiated.')

    @staticmethod
    @override
    def input() -> str:
        """ Get the user input. """
        return console.input('[bold cyan]>>> [/]').strip()

    @staticmethod
    def clear_screen() -> None:
        """ Clears the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause() -> None:
        """ Pauses the program until the user presses the Enter key. """
        console.input('[white]Press Enter to continue...[/]')


class Command(NamedTuple):
    """ The class represents a command. """
    key: str = ''
    args: list[str] | None = None


class CommandRichParser(Parser):
    """
    The class implements the parser for the command line interface.
    Using the standard library `argparse` to parse the user input.
    Using the library `rich` to print rich-text.
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
        input_args = CLIRichUtils.input().split()
        args = self._parser.parse_args(input_args)
        return Command(args.key, args.args)


class BeatmapRichPrinter(Printer):
    """
    The class implements the printer for the command line interface.
    Using the library `rich` to print rich-text.
    """

    @override
    def print(self, output: list[Beatmap]) -> None:
        """ Prints the beatmaps. """
        if not isinstance(output, list) or not all(isinstance(i, Beatmap) for i in output):
            console.error('Invalid beatmaps.')
            return

        table = Table(border_style='bold grey70')
        table.add_column('sid', style='dark_sea_green3', header_style='bold dark_sea_green3', min_width=8, no_wrap=True)
        table.add_column('artist', style='light_cyan3', header_style='bold light_cyan3', min_width=42, no_wrap=True)
        table.add_column('name', style='grey100', header_style='bold grey100', no_wrap=True)

        for i in output:
            table.add_row(str(i.sid), i.artist, i.name)

        console.print(table)
        console.print(f'Total: {len(output)}', style='bold yellow')
