# -*- coding: utf-8 -*-
import json
import sys
from json.decoder import JSONDecodeError
from typing import Optional, TypedDict

__all__ = ['Config']


class ConfigType(TypedDict):
    """
    The class is a type hint of the config.

    Attributes:
        path: The path to the Songs directory of osu! game.
    """
    path: Optional[str]


class Config:
    """
    The class provides APIs to config management.

    Attributes:
        CONFIG_FILE: The path to the config file.
    """
    CONFIG_FILE: str = f'{sys.path[0]}/config.json'
    _config: Optional[ConfigType] = None

    def load(self) -> None:
        """ Loads the config from the file. """
        self._read_config()

    def reset(self) -> None:
        """ Resets the config. """
        self._config = {'path': None}
        self._write_config()

    @property
    def path(self) -> Optional[str]:
        """ Returns path in the config. """
        return self._config.get('path', None)

    @path.setter
    def path(self, path: str) -> None:
        """ Sets path in the config. """
        if self._config is None:
            self._config = {}

        self._config['path'] = path
        self._write_config()

    def _read_config(self) -> None:
        """ Reads the config from the file. """
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                self._config = json.load(f)
        except (IOError, JSONDecodeError):
            self.reset()

    def _write_config(self) -> None:
        """ Writes the config to the file. """
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self._config, f)
