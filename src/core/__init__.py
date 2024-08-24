# -*- coding: utf-8 -*-
from core.client import Client

__all__ = ['OSSApplication']


class OSSApplication:
    """ OSSApplication is the main class of the application. """
    _client = Client()

    def run(self):
        """ Run the application."""
        while True:
            try:
                self._client.run()
            except IOError:
                self._client.exit(-1)

    def shutdown(self):
        """ Exit the application."""
        self._client.exit(0)
