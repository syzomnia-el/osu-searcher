# -*- coding: utf-8 -*-
import os
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from functools import total_ordering

from ui import IOUtils

__all__ = ['Beatmap', 'BeatmapManager', 'Condition', 'ConditionType']

_io = IOUtils


class ConditionType(Enum):
    """
    The class defines the condition type for the beatmap searching.

    Attributes:
        SID: The sid of the beatmap.
        ARTIST: The artist of the beatmap.
        NAME: The name of the beatmap.
    """
    SID = 'sid'
    ARTIST = 'artist'
    NAME = 'name'

    @classmethod
    def __numbers__(cls) -> list[str]:
        """
        Returns the list of all condition types.

        :return: A list of condition types.
        """
        return [condition.value for condition in cls]


type Condition = str | dict[ConditionType, str]


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

    _artist_lower: str = field(init=False, repr=False)
    _name_lower: str = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """ Cache the lower case of the artist and name for searching. """
        object.__setattr__(self, '_artist_lower', self.artist.lower())
        object.__setattr__(self, '_name_lower', self.name.lower())

    def __contains__(self, s: Condition) -> bool:
        """ Returns whether a string belongs to the beatmap. """
        if isinstance(s, str):
            return any(s.lower() in attr for attr in (self.sid, self._artist_lower, self._name_lower))

        if not isinstance(s, dict):
            raise TypeError(f'Expected str or dict[ConditionType, str], got {type(s).__name__}')
        if any(not isinstance(key := k, ConditionType) for k in s.keys()):
            raise TypeError(f'Invalid key, expected ConditionType, got {type(key).__name__}')
        if any(not isinstance(value := v, str) for v in s.values()):
            raise TypeError(f'Invalid value, expected str, got {type(value).__name__}')

        return all(v.lower() in getattr(self, k.value) for k, v in s.items())

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
    beatmaps: list[Beatmap] = field(default_factory=list)

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
        object.__setattr__(self, 'beatmaps', beatmaps)

    def filter(self, condition: Condition) -> list[Beatmap]:
        """
        Filters beatmaps by the condition.

        If condition is a string, it is treated as a keyword.
        If condition is a dict, it is treated as a type-keyword pair.

        The keyword is case-insensitive.
        If the keyword is an empty string, returns all beatmaps.

        The keyword type is one of sid, artist or name as ConditionType.

        :param condition: The condition to filter the beatmaps as a string or a dict.
        :return: A list of beatmaps matching the keyword.
        """
        return [beatmap for beatmap in self.beatmaps if condition in beatmap]

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
