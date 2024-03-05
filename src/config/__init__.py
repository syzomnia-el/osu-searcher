# -*- coding: utf-8 -*-
import json
import os
import sys
from json import JSONDecodeError
from typing import Optional, TypedDict

from ui import IOUtils

__all__ = ['Config', 'ConfigManager']

_io = IOUtils


class ConfigDict(TypedDict):
    """
    The class is a type hint of the config.

    Attributes:
        path: The path to the Songs directory of osu! game.
    """
    path: Optional[str]


class Config(dict):
    """
    The class defines the config interface.

    Properties:
        path: The path in the config.
    """
    _DEFAULT_CONFIG: ConfigDict = {'path': None}

    def __init__(self, config: ConfigDict = None) -> None:
        """ Initialize the config. """
        if config and isinstance(config, dict):
            config_data = config
        else:
            config_data = self._DEFAULT_CONFIG
        super().__init__(config_data)

    @property
    def path(self) -> Optional[str]:
        """ Returns the path in the config. """
        return self.get('path', None)

    @path.setter
    def path(self, path: str) -> None:
        """ Sets the path in the config. """
        if not _io.is_valid_path(path):
            print(f'invalid path:`{path}`')
            return

        self['path'] = path


class ConfigManager:
    """
    The abstract class defines the config manager interface.

    Attributes:
        CONFIG_FILE: The absolute path to the config file.

    Properties:
        config: The config of the manager.

    Methods:
        load: Loads the config from the file.
        reset: Resets the config.
    """
    CONFIG_FILE: str = os.path.join(sys.path[0], 'config.json')
    _config: Optional[Config] = None

    @property
    def config(self) -> Optional[Config]:
        """ Returns the config. """
        return self._config

    @config.setter
    def config(self, config: Config) -> None:
        """ Sets the config. """
        if not config or not isinstance(config, Config):
            config = Config()

        self._config = config
        self.save()

    def load(self) -> None:
        """ Loads the config from the file. """
        self._read()

    def save(self) -> None:
        """ Saves the config to the file. """
        self._write()

    def reset(self) -> None:
        """ Resets the config. """
        self.config = Config()

    def _read(self) -> None:
        """ Reads the config from the JSON file."""
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self._config = Config(data)
        except (IOError, JSONDecodeError):
            print('Invalid JSON file, reset the config.')
            self.reset()

    def _write(self) -> None:
        """ Writes the config to the JSON file. """
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self._config, f)
