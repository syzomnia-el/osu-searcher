# -*- coding: utf-8 -*-
from core.control import Control

__all__ = ['OSSApplication']


class OSSApplication:
    """ OSSApplication is the main class of the application. """
    _control: Control

    def __init__(self) -> None:
        self._control = Control()

    def run(self):
        self._control.run()

    def exit(self):
        self._control.exit()
