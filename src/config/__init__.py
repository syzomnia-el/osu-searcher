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
    _config: ConfigType

    def load(self) -> None:
        """ Loads the config from the file. """
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                self._config = json.load(f)
        except (IOError, JSONDecodeError):
            self.reset()

    def reset(self) -> None:
        """ Resets the config. """
        self._config = {'path': None}
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self._config, f)

    @property
    def path(self) -> str:
        """ Returns path in the config. """
        return self._config.get('path', None)

    @path.setter
    def path(self, path: str) -> None:
        """ Sets path in the config. """
        self._config['path'] = path
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self._config, f)
