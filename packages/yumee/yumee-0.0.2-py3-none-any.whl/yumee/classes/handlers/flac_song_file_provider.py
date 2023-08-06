from pathlib import Path

from yumee.classes.handlers import AbstractSongFileProvider
from yumee.classes.song_files import FlacSongFile
from yumee.interfaces import BaseSongFile

__all__ = ["FlacSongFileProvider"]


class FlacSongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "flac"

    def _new_song_file(self, path: Path) -> BaseSongFile:
        return FlacSongFile(path)
