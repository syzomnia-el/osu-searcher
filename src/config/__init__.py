# -*- coding: utf-8 -*-
import json
import os.path
import sys
from json import JSONDecodeError
from typing import TypedDict

from ui import IOUtils

try:
    from ui.rich_cli import console
except ModuleNotFoundError:
    from ui.cli import console

__all__ = ['Config', 'ConfigManager']

_io = IOUtils


class ConfigDict(TypedDict):
    """
    The class is a type hint of the config.

    Attributes:
        path: The path to the Songs directory of the game osu!.
    """
    path: str | None


class Config(dict):
    """
    The class defines the config data structure.

    Properties:
        path: The path in the config.
    """
    _DEFAULT_CONFIG: ConfigDict = {'path': None}

    def __init__(self, config: ConfigDict = None) -> None:
        """ Initialize the config. """
        config_data = config if config and isinstance(config, dict) else self._DEFAULT_CONFIG
        super().__init__(config_data)

    @property
    def path(self) -> str | None:
        """ Returns the path in the config. """
        return self.get('path', None)

    @path.setter
    def path(self, path: str) -> None:
        """ Sets the path in the config. """
        if not _io.is_valid_path(path):
            console.error(f'invalid path:`{path}`')
            return

        self['path'] = path


class ConfigManager:
    """
    The class defines the config manager utils.

    Attributes:
        CONFIG_FILE: The absolute path to the config file.

    Properties:
        config: The config of the manager.

    Methods:
        load: Load the config from the file.
        reset: Reset the config.
        save: Save the config to the file.
    """
    CONFIG_FILE: str = os.path.join(sys.path[0], 'config.json')
    _config: Config | None = None

    @property
    def config(self) -> Config | None:
        """ Return the config. """
        return self._config

    @config.setter
    def config(self, config: Config) -> None:
        """ Set the config. """
        if not config or not isinstance(config, Config):
            config = Config()

        self._config = config
        self.save()

    def load(self) -> None:
        """ Load the config from the file. """
        self._read()

    def save(self) -> None:
        """ Save the config to the file. """
        self._write()

    def reset(self) -> None:
        """ Reset the config. """
        self.config = Config()

    def _read(self) -> None:
        """ Read the config from the JSON file."""
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._config = Config(data)
        except (IOError, JSONDecodeError):
            console.warning('Invalid JSON file, reset the config.')
            self.reset()

    def _write(self) -> None:
        """ Write the config to the JSON file. """
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._config, f)
