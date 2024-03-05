# -*- coding: utf-8 -*-
from core.control import Control

__all__ = ['OSSApplication']


class OSSApplication:
    """ OSSApplication is the main class of the application. """
    _control: Control = Control()

    def run(self):
        """ Run the application."""
        while True:
            try:
                self._control.run()
            except IOError:
                self._control.exit(1)

    def shutdown(self):
        """ Exit the application."""
        self._control.exit(0)
