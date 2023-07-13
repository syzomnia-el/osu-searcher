# -*- coding: utf-8 -*-
import os
import sys
from typing import Callable, NoReturn, Self

from config import Config
from model import Beatmap, BeatmapManager
from ui import Parser
from ui.cli import CommandParser

__all__ = ['Control']


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

    Attributes:
        COMMANDS: The mapping of commands to their corresponding methods.
        config: The config of the program.
        beatmap_manager: The manager of the osu! beatmaps.
    """
    COMMANDS: dict[str, Callable]

    _config: Config
    _beatmap_manager: BeatmapManager
    _instance: Self = None
    _parser: Parser = CommandParser()

    def __new__(cls) -> 'Control':
        """ Overrides the __new__ method to implement the singleton pattern. """
        if cls._instance is None:
            cls._instance = super(Control, cls).__new__(cls)
            cls.COMMANDS = {
                'check': cls.check,
                'exit': cls.exit,
                'find': cls.find,
                'flush': cls.flush,
                'list': cls.list_,
                'path': cls.path
            }
        return cls._instance

    def __init__(self) -> None:
        """ Initializes the class and load the config. """
        self.config = Config()

    @property
    def config(self) -> Config:
        """ Returns the config. """
        return self._config

    @config.setter
    def config(self, config: Config) -> None:
        """ Sets the config and load the beatmaps. """
        self._config = Config() if config is None else config
        self._config.load()

        # If the path is not set, ask the user to input.
        while self._config.path is None:
            self._set_path()
        self.beatmap_manager = BeatmapManager()

    @property
    def beatmap_manager(self) -> BeatmapManager:
        """ Returns the beatmap manager. """
        return self._beatmap_manager

    @beatmap_manager.setter
    def beatmap_manager(self, beatmaps: BeatmapManager) -> None:
        """ Sets the beatmap manager and load the beatmaps. """
        self._beatmap_manager = BeatmapManager() if beatmaps is None else beatmaps
        self._beatmap_manager.load(self.config.path)

    def run(self) -> NoReturn:
        """ The main entry point of the program. Loop until the user inputs `exit`, or an error occurs. """
        try:
            while True:
                self.clear_screen()
                self._prompt()
                self._parse_command()
        except IOError:
            sys.exit(1)

    def check(self) -> None:
        """
        Checks the duplicate beatmaps and lists the result as below:

            sid   | artist   | name  \n
            \u005c-------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>
        """
        self.flush()
        self._print_beatmaps(self.beatmap_manager.check())

    def find(self, key: str = '') -> None:
        """
        Finds beatmaps by a keyword. If the keyword is an empty string, ask the user to input.
        And then lists the result as below:

            sid   | artist   | name  \n
            \u005c-------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>

        Parameters:
            key: The keyword to find.
        """
        if key == '':
            print('keyword:')
            key = input()
        self._print_beatmaps(self.beatmap_manager.filter(key))

    def flush(self) -> None:
        """ Flushes the beatmap data cache. """
        self.config = Config()

    def list_(self) -> None:
        """ Lists all the beatmaps. """
        self._print_beatmaps(self.beatmap_manager.beatmaps)

    def path(self) -> None:
        """ Modifies the saved path of the beatmaps. """
        self._set_path()
        self.flush()

    def _prompt(self) -> None:
        """
        Prints the prompt as below:

        path: <path>\n
        command:\n
        \u005c- check | exit | find <keyword> | flush | list | path`
        """
        self._print_path()
        print('command:')
        print('-', end=' ')
        for i in self.COMMANDS.keys():
            print(f'{i} <keyword>' if i == 'find' else i, end=' | ')
        print()

    def _parse_command(self) -> None:
        """ Parses the command and executes the corresponding method. """
        key, arg = self._parser.parse()
        if key not in self.COMMANDS:
            return

        method = self.COMMANDS[key]
        if key == 'find':
            method(arg)
        else:
            method()

    def _print_path(self) -> None:
        """ Prints the path of the beatmaps. """
        print(f'path: {self.config.path}')

    def _print_beatmaps(self, beatmaps: list[Beatmap]) -> None:
        """
        Prints the beatmaps as below:

            sid   | artist   | name  \n
            \u005c-------------------------\n
            <sid> | <artist> | <name>\n
            total: <total_number>

        Parameters:
            beatmaps: The beatmaps to print.
        """
        label_sid, label_artist, label_name = tuple(beatmaps[0].__dict__.keys())
        print(f'{label_sid:<7} | {label_artist:<60} | {label_name}')
        print(f'{"":-<130}')

        for i in beatmaps:
            print(f'{i.sid:<7} | {i.artist:<60} | {i.name}')

        print(f'total: {len(beatmaps)}')
        self.pause()

    def _set_path(self) -> None:
        """ Sets the path of the beatmaps. If the user inputs `q`, the method will return. """
        self.clear_screen()
        self._print_path()
        print('switch to (enter `q` to cancel):')

        arg = input().strip().lower()
        if arg == 'q':
            return
        self._config.path = arg

    @staticmethod
    def clear_screen() -> None:
        """ Clears the screen. """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause() -> None:
        """ Pauses the program until the user presses the Enter key. """
        input('Press Enter to continue . . .')

    @staticmethod
    def exit() -> None:
        """ Exits the program. """
        sys.exit(0)
