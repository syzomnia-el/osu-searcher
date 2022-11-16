# -*- coding: utf-8 -*-
import json
from json.decoder import JSONDecodeError


class Configuration:
    __CONFIG_PATH: str = 'config.json'
    __config: dict

    def __init__(self) -> None:
        try:
            with open(self.__CONFIG_PATH) as f:
                self.__config = json.load(f)
        except (IOError, JSONDecodeError):
            self.reset()

    def reset(self) -> None:
        self.__config = {'path': None}
        with open(self.__CONFIG_PATH, 'w') as f:
            json.dump(self.__config, f)

    @property
    def path(self) -> str:
        return self.__config.get('path', None)

    @path.setter
    def path(self, path: str) -> None:
        path = path.strip()
        self.__config['path'] = None if path == '' else path
        with open(self.__CONFIG_PATH, 'w') as f:
            json.dump(self.__config, f)
