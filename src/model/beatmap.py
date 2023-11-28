# -*- coding: utf-8 -*-
import contextlib
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

    def __contains__(self, x: str) -> bool:
        """
        Checks whether the string belongs to the beatmap.

        Args:
            x: The string to check.
            
        Returns:
            True if the string belongs to the beatmap, otherwise False.
        """

        return any(x.lower() in value.lower() for value in vars(self).values())

    def __hash__(self) -> int:
        """ Returns the hash value of the beatmap. """
        return hash(int(self.sid))

    def __lt__(self, other: 'Beatmap') -> bool:
        """
        Compares the beatmap with the other beatmap.

        Args:
            other: The other beatmap to compare.

        Returns:
            True if the name of the beatmap is less than the other beatmap, otherwise False.
        """
        return self.name.lower() < other.name.lower()


@dataclass(frozen=True)
class BeatmapManager:
    """ The class provides API to beatmap management. """
    beatmaps: list[Beatmap] = field(default_factory=list, repr=False)

    def load(self, path: str = None) -> None:
        """
        Loads beatmap data from the path.

        Args:
            path: The path to the Songs directory of osu! game.
        """
        if not path or not os.path.exists(path):
            return

        for i in os.listdir(path):
            with contextlib.suppress(ValueError):
                beatmap = self._parse_beatmap(i)
                self.beatmaps.append(beatmap)

    def filter(self, key: str = '') -> list[Beatmap]:
        """
        Returns the beatmaps matching the keyword.
        The keyword is case-insensitive.
        If the keyword is an empty string, returns all the beatmaps.

       Args:
            key: The keyword to filter.

        Returns:
            A list of beatmaps matching the keyword.
        """
        return [beatmap for beatmap in self.beatmaps if key in beatmap]

    def check(self) -> list[Beatmap]:
        """
        Checks whether any duplicated sid is in the beatmaps.

        Returns:
            A list of beatmaps with the duplicated sid.
        """
        return [beatmap for beatmap, count in Counter(self.beatmaps).items() if count > 1]

    @staticmethod
    def _parse_beatmap(filename: str) -> Beatmap:
        """
        Parses beatmap data from the filename.

        Args:
            filename: The filename of the beatmap.

        Returns:
            A Beatmap object parsed from the filename.
        """
        tmp, name = filename.split(' - ', 1)
        sid, artist = tmp.strip().split(' ', 1)
        return Beatmap(sid, artist, name)
