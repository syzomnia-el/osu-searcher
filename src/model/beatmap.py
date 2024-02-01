# -*- coding: utf-8 -*-
import os
from collections import Counter
from dataclasses import dataclass, field

__all__ = ['Beatmap', 'BeatmapManager']


@dataclass(frozen=True)
class Beatmap:
    """
    The class implements the beatmap datatype.

    Attributes:
        sid: The sid of the beatmap.
        artist: The artist of the beatmap.
        name: The name of the beatmap.
    """
    sid: str = ''
    artist: str = ''
    name: str = ''

    _artist_lower: str = field(init=False, repr=False)
    _name_lower: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """ Initializes the attributes. """
        object.__setattr__(self, '_artist_lower', self.artist.lower())
        object.__setattr__(self, '_name_lower', self.name.lower())

    def __contains__(self, s: str) -> bool:
        """ Returns whether a string belongs to the beatmap. """
        return any(s.lower() in value for value in (self.sid, self._artist_lower, self._name_lower))

    def __hash__(self) -> int:
        """ Returns the hash value of the beatmap. """
        return hash(int(self.sid))

    def __eq__(self, other: 'Beatmap') -> bool:
        """ Returns whether the beatmap is equal to the other beatmap. """
        return self.sid == other.sid

    def __lt__(self, other: 'Beatmap') -> bool:
        """
        Compares the beatmap with the other beatmap by the name string.

        :param other: The other beatmap to compare.
        :return: True if he beatmap is less than the other beatmap, otherwise False.
        """
        return self.name < other.name


@dataclass(frozen=True)
class BeatmapManager:
    """
    The class provides API to beatmap management.

    Attributes:
        beatmaps: The list of beatmaps.
    """
    beatmaps: list[Beatmap] = field(default_factory=list, repr=False)

    def load(self, path: str = None) -> None:
        """
        Loads beatmap data from the path.

        :param path: The path to the Songs directory of osu! game.
        """
        if not path or not os.path.exists(path) or not os.path.isdir(path):
            return

        filenames = list(map(lambda x: x.name, os.scandir(path)))
        if not filenames:
            return

        object.__setattr__(self, 'beatmaps', sorted(map(self._parse_beatmap, filenames)))

    def filter(self, key: str = '') -> list[Beatmap]:
        """
        Filters beatmaps by the keyword.
        The keyword is case-insensitive.
        If the keyword is an empty string, returns all beatmaps.

        :param key: The keyword to filter.
        :return: A list of beatmaps matching the keyword.
        """
        return [beatmap for beatmap in self.beatmaps if key in beatmap]

    def check(self) -> list[Beatmap]:
        """
        Checks duplicated beatmaps by the sid.

        :return: A list of beatmaps with the duplicated sid.
        """
        return [beatmap for beatmap, count in Counter(self.beatmaps).items() if count > 1]

    @staticmethod
    def _parse_beatmap(filename: str) -> Beatmap:
        """
        Parses beatmap data from the filename.

        :param filename: The filename of the beatmap.
        :return: A Beatmap object parsed from the filename.
        """
        try:
            tmp, name = filename.strip().rsplit(' - ', 1)
            sid, artist = tmp.split(' ', 1)
            return Beatmap(sid, artist.strip(), name)
        except ValueError:
            print(f'Invalid beatmap filename: {filename}')
            return Beatmap()
