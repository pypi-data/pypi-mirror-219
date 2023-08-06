import abc
from typing import Callable
from pathlib import Path

from yumee.interfaces import BaseSongFile, BaseSongFileProvider

__all__ = ["AbstractSongFileProvider"]


class AbstractSongFileProvider(BaseSongFileProvider, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def encoding(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def _new_song_file(self, path: Path) -> BaseSongFile:
        raise NotImplementedError

    def _handle(self, request: Path, next: Callable[[Path], BaseSongFile]) -> BaseSongFile:
        encoding = request.suffix[1:]

        if encoding != self.encoding:
            return next(request)

        return self._new_song_file(request)
