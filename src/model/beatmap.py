# -*- coding: utf-8 -*-
import os
from collections import Counter
from dataclasses import dataclass, field
from functools import total_ordering

from ui import IOUtils

__all__ = ['Beatmap', 'BeatmapManager']

_io = IOUtils


@dataclass(frozen=True)
@total_ordering
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

    _artist_lower: str = field(default='', repr=False)
    _name_lower: str = field(default='', repr=False)

    def __post_init__(self) -> None:
        """ Cache the lower case of the artist and name for searching. """
        # It is a little bit tricky to use the magic method,
        # but I cannot find other better way to do this.
        object.__setattr__(self, '_artist_lower', self.artist.lower())
        object.__setattr__(self, '_name_lower', self.name.lower())

    def __contains__(self, s: str) -> bool:
        """ Returns whether a string belongs to the beatmap. """
        s_lower = s.lower()
        return any(s_lower in value for value in (self.sid, self._artist_lower, self._name_lower))

    def __hash__(self) -> int:
        """ Returns the hash value of the beatmap. """
        return hash(int(self.sid))

    def __eq__(self, other: 'Beatmap') -> bool:
        """ Returns whether the beatmap is equal to the other beatmap. """
        return self.sid == other.sid

    def __lt__(self, other: 'Beatmap') -> bool:
        """ Compares the beatmap with the other beatmap by the name string. """
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
        if not _io.is_valid_path(path):
            return

        filenames = list(map(lambda x: x.name, os.scandir(path)))
        if not filenames:
            return

        beatmaps = sorted(filter(None, map(self._parse_beatmap, filenames)))
        # It is a little bit tricky to use the magic method,
        # but I cannot find other better way to do this.
        object.__setattr__(self, 'beatmaps', beatmaps)

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
    def _parse_beatmap(filename: str) -> Beatmap | None:
        """
        Parses beatmap data from the filename.

        :param filename: The filename of the beatmap.
        :return: A Beatmap object parsed from the filename.
        """
        try:
            tmp, *name = filename.strip().rsplit(' - ', 1)
            sid, *artist = tmp.split(' ', 1)
            artist = artist[0].strip() if artist else ''
            name = name[0] if name else ''
            return Beatmap(sid, artist, name)
        except ValueError:
            print(f'Invalid beatmap filename: {filename}')
            return None
