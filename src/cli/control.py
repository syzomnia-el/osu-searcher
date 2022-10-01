# -*- coding: utf-8 -*-
import os
import sys
from typing import Any, Dict, NewType, Tuple

from conf.config import Configuration
from data.data import SongList


class Control:
    __instance = None
    __config: Configuration
    __song_list: SongList
    __commands: Dict[str, Any]

    def __new__(cls) -> NewType('Control', object):
        if not cls.__instance:
            cls.__instance = super(Control, cls).__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__commands = {
            'check': self.check,
            'exit': self.exit,
            'find': self.find,
            'flush': self.flush,
            'list': self.list,
            'path': self.path
        }
        self.flush()

    @property
    def config(self) -> Configuration:
        return self.__config

    @property
    def song_list(self) -> SongList:
        return self.__song_list

    @config.setter
    def config(self, config: Configuration) -> None:
        self.__config = config
        while self.__config.path is None:
            self.set_path()
        self.__song_list = SongList(self.__config.path)

    def run(self) -> None:
        try:
            while True:
                self.clear_screen()
                self.prompt()
                self.parse()
        except (IOError, KeyboardInterrupt):
            sys.exit(1)

    def prompt(self) -> None:
        self.print_path()
        print('command:')
        print('-', end=' ')
        for i in self.__commands.keys():
            print(f'{i} <keyword>' if i == 'find' else i, end=' | ')
        print()

    def parse(self) -> None:
        command, key = self.read_command()
        if command in self.__commands:
            if command == 'find':
                self.__commands.get(command)(key)
            else:
                self.__commands.get(command)()

    def check(self) -> None:
        self.flush()
        self.print_list(self.__song_list.check())

    def exit(self) -> None:
        self.clear_screen()
        sys.exit(0)

    def find(self, key: str = '') -> None:
        if key == '':
            print('keyword:')
            key = input()
        self.print_list(self.__song_list.find(key))

    def flush(self) -> None:
        self.config = Configuration()

    def list(self) -> None:
        self.print_list(self.__song_list)

    def path(self) -> None:
        self.set_path()
        self.flush()

    def print_path(self) -> None:
        print(f'path: {self.__config.path}')

    def set_path(self) -> None:
        self.clear_screen()
        self.print_path()
        print('switch to (enter `q` to cancel):')
        args = input().lower()
        if args != 'q':
            self.__config.path = args

    def print_list(self, song_list: SongList) -> None:
        print('list:')
        for i in song_list:
            print(i)
        print(f'total: {len(song_list)}')
        self.pause()

    @staticmethod
    def clear_screen() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def pause() -> None:
        input('Press Enter to continue . . .')

    @staticmethod
    def read_command() -> Tuple[str, str]:
        args = input().strip().lower().split(' ', 1)
        command = args[0]
        key = args[1].strip() if len(args) == 2 else ''
        return command, key
