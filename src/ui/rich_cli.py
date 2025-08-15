# -*- coding: utf-8 -*-
import os
from functools import partial
from typing import Self, override

from model import Beatmap
from ui import IOUtils, Printer
from ui.cli import CommandParser

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
        """ Clear the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause() -> None:
        """ Pause the program until the user presses the Enter key. """
        console.input('[white]Press Enter to continue...[/]')


class CommandRichParser(CommandParser):
    """
    The class implements the parser for the command line interface.
    Using the standard library `argparse` to parse the user input.
    Using the library `rich` to print rich-text.
    """
    _io = CLIRichUtils


class BeatmapRichPrinter(Printer):
    """
    The class implements the printer for the command line interface.
    Using the library `rich` to print rich-text.
    """

    @override
    def print(self, output: list[Beatmap]) -> None:
        """ Print the beatmaps. """
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
