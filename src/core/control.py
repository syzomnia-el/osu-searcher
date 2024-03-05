# -*- coding: utf-8 -*-
from typing import Callable, NoReturn

from config import ConfigManager
from model import Beatmap, BeatmapManager
from ui import Parser, Printer
from ui.cli import BeatmapPrinter, CLIUtils, CommandParser

__all__ = ['Control']

_io = CLIUtils


class Control:
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
        run: The main entry point of the program. Loop until the user inputs `exit`, or an error occurs.
        shutdown: Exits the program.
    """
    _COMMANDS: dict[str, Callable]

    _config_manager: ConfigManager
    _beatmap_manager: BeatmapManager
    _parser: Parser = CommandParser()
    _printer: Printer = BeatmapPrinter()

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

        # If the path is not set, ask user to input.
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
            \u005c-------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>
        """
        self._flush()
        self._print_beatmaps(self.beatmap_manager.check())

    def _find(self, key: str = '') -> None:
        """
        Finds beatmaps by a keyword and prints the result as below.
        If the keyword is not given, ask the user to input.

            sid   | artist   | name  \n
            \u005c-------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>

       :param key: The keyword to find.
        """
        if not key:
            print('keyword:')
            key = _io.input()

        self._print_beatmaps(self.beatmap_manager.filter(key))

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
        Prints the prompt as below.

        path: <path>\n
        command:\n
        \u005c- check | exit | find <keyword> | flush | list | path`
        """
        self._print_path()
        print('command:')
        print('-', end=' ')
        for i in self._COMMANDS.keys():
            print(f'{i} <keyword>' if i == 'find' else i, end=' | ')
        print()

    def _parse_command(self) -> None:
        """ Parses the command and executes the corresponding method. """
        _io.clear_screen()
        self._prompt()

        # parse the command from the user input.
        key, args = self._parser.parse()
        if key not in self._COMMANDS:
            return
        if not args:
            args = ['']

        # execute the corresponding method.
        method = self._COMMANDS[key]
        match key:
            case 'find':
                method(args[0])
            case _:
                method()

    def _print_path(self) -> None:
        """ Prints the path of the beatmaps. """
        print(f'path: {self.config_manager.config.path}')

    def _print_beatmaps(self, beatmaps: list[Beatmap]) -> None:
        """ Prints the beatmaps. """
        self._printer.print(beatmaps)
        _io.pause()

    def _set_path(self) -> None:
        """ Sets the path of the beatmaps. If the user inputs `q`, the method will return. """
        while True:
            _io.clear_screen()
            self._print_path()
            print('switch to (enter `q` to cancel):')
            command = _io.input().lower()

            if command == 'q':
                return
            if _io.is_valid_path(command):
                break

            print('invalid path.')
            _io.pause()

        # set the path in the config and save into the file.
        config = self.config_manager.config
        config.path = command
        self.config_manager.config = config
