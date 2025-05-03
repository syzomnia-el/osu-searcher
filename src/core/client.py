# -*- coding: utf-8 -*-
from collections.abc import Callable
from typing import NoReturn

from config import ConfigManager
from model import Beatmap, BeatmapManager
from model.beatmap import ConditionType
from ui import Parser, Printer

__EXIST_RICH__ = False
try:
    from ui.rich_cli import BeatmapRichPrinter, CLIRichUtils, CommandRichParser, console
    from rich.panel import Panel

    __EXIST_RICH__ = True
except ModuleNotFoundError:
    from ui.cli import BeatmapPrinter, CLIUtils, CommandParser, console

__all__ = ['Client']

_io = CLIRichUtils if __EXIST_RICH__ else CLIUtils


class Client:
    """
    The class is a singleton provides APIs for the user to interact with the program.
    All the commands are listed as below:

        - check: Check the duplicate beatmaps.
        - exit: Exit the program.
        - find: Find beatmaps by a keyword.
        - flush: Flush the beatmap data cache.
        - list: List all the beatmaps.
        - path: Modify the saved path of the beatmaps.

    Methods:
        run: The main entry point. Loop until the user inputs `exit`, or an error occurs.
        shutdown: Exits the program.
    """
    _COMMANDS: dict[str, Callable]

    _config_manager: ConfigManager
    _beatmap_manager: BeatmapManager
    _parser: Parser = CommandRichParser() if __EXIST_RICH__ else CommandParser()
    _printer: Printer = BeatmapRichPrinter() if __EXIST_RICH__ else BeatmapPrinter()

    def __init__(self) -> None:
        """ Initializes the class and load the config. """
        self._COMMANDS = {
            'check': self._check,
            'exit': self.exit,
            'find': self._find,
            'flush': self._flush,
            'list': self._list,
            'path': self._path
        }
        self.config_manager = ConfigManager()

    @property
    def config_manager(self) -> ConfigManager:
        """ Returns the config. """
        return self._config_manager

    @config_manager.setter
    def config_manager(self, config_manager: ConfigManager) -> None:
        """ Sets the config and load the beatmaps. """
        if not config_manager or not isinstance(config_manager, ConfigManager):
            config_manager = ConfigManager()

        self._config_manager = config_manager
        self._config_manager.load()
        # If the path is not set, ask the user to input.
        while not self._config_manager.config.path:
            self._set_path()
        self.beatmap_manager = BeatmapManager()

    @property
    def beatmap_manager(self) -> BeatmapManager:
        """ Returns the beatmap manager. """
        return self._beatmap_manager

    @beatmap_manager.setter
    def beatmap_manager(self, beatmap_manager: BeatmapManager) -> None:
        """ Sets the beatmap manager and load the beatmaps. """
        if not beatmap_manager or not isinstance(beatmap_manager, BeatmapManager):
            beatmap_manager = BeatmapManager()

        self._beatmap_manager = beatmap_manager
        self._beatmap_manager.load(self.config_manager.config.path)

    def run(self) -> NoReturn:
        """ The main entry point of the program. """
        self._parse_command()

    @staticmethod
    def exit(code: int = 0) -> NoReturn:
        """ Exits the program. """
        _io.clear_screen()
        _io.exit(code)

    def _check(self) -> None:
        """
        Checks the duplicate beatmaps and prints the result as below.

            sid   | artist   | name  \n
            \------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>
        """
        self._flush()
        self._print_beatmaps(self.beatmap_manager.check())

    def _find(self, condition: str = '') -> None:
        """
        Finds beatmaps by a keyword, and prints the result as below.
        If the keyword is not given, ask the user to input.
        Use `condition=keyword` for specific conditions filtering including sid, name or artist.

            sid   | artist   | name  \n
            \------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>

       :param condition: The condition to find.
        """
        if not condition:
            if __EXIST_RICH__:
                console.print('[magenta]keyword[/]:')
            else:
                console.print('keyword:')
            # get the condition from the user input.
            condition = _io.input()

        args = condition.split('=', 1)
        if len(args) == 2 and args[0] in ConditionType:
            condition = {ConditionType(args[0]): args[1]}

        self._print_beatmaps(self.beatmap_manager.filter(condition))

    def _flush(self) -> None:
        """ Flushes the config and beatmap data cache. """
        self.config_manager = ConfigManager()

    def _list(self) -> None:
        """ Lists all the beatmaps. """
        self._print_beatmaps(self.beatmap_manager.beatmaps)

    def _path(self) -> None:
        """ Modifies the saved path of the beatmaps. """
        self._set_path()
        self._flush()

    def _prompt(self) -> None:
        """
        Prints the prompt.

        path: <path>\n
        command:\n
        \- check | exit | find [condition=]<keyword> | flush | list | path`
        """
        self._print_path()
        if __EXIST_RICH__:
            output = Panel(
                '\n'.join(
                    f"[red]-[/] {f'{i} [italic grey50]\[condition=][/][italic magenta]<keyword>[/]' if i == 'find' else i}"
                    for i in self._COMMANDS
                ),
                title='Command',
                border_style='green'
            )
        else:
            output = (
                "command:\n"
                f"- {' | '.join(
                    f'{i} [condition=]<keyword>' if i == 'find' else i
                    for i in self._COMMANDS
                )}"
            )
        console.print(output)

    def _parse_command(self) -> None:
        """ Parses the command and executes the corresponding method. """
        _io.clear_screen()
        self._prompt()
        # parse the command from the user input.
        command, args = self._parser.parse()
        self._execute_command(command, args)

    def _execute_command(self, command: str, args: list[str]) -> None:
        """ Executes the corresponding method based on the command. """
        if command not in self._COMMANDS:
            return
        if not args:
            args = ['']

        method = self._COMMANDS[command]
        match command:
            case 'find':
                condition = args[0]
                method(condition)
            case _:
                method()

    def _print_path(self) -> None:
        """ Prints the path of the beatmaps. """
        count = len(self.beatmap_manager.beatmaps)
        if __EXIST_RICH__:
            output = Panel(
                f'{self.config_manager.config.path} [grey70]([cyan]{count}[/])[/]',
                title='Path',
                border_style='blue'
            )
        else:
            output = f'path: {self.config_manager.config.path} ({count})'
        console.print(output)

    def _print_beatmaps(self, beatmaps: list[Beatmap]) -> None:
        """ Prints the beatmaps. """
        self._printer.print(beatmaps)
        _io.pause()

    def _set_path(self) -> None:
        """ Sets the path of the beatmaps. If the user inputs `q`, the method will return. """
        while True:
            _io.clear_screen()
            self._print_path()
            if __EXIST_RICH__:
                console.print('switch to (enter `[warning]q[/]` to cancel):')
            else:
                console.print('switch to (enter `q` to cancel):')

            command = _io.input().lower()
            if command == 'q':
                return
            if _io.is_valid_path(command):
                break

            console.error('invalid path.')
            _io.pause()
        # set the path in the config and save into the file.
        config = self.config_manager.config
        config.path = command
        self.config_manager.config = config
