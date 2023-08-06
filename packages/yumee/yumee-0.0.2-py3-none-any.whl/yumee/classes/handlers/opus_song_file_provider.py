from pathlib import Path

from yumee.classes.handlers import AbstractSongFileProvider
from yumee.classes.song_files import OpusSongFile
from yumee.interfaces import BaseSongFile

__all__ = ["OpusSongFileProvider"]


class OpusSongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "opus"

    def _new_song_file(self, path: Path) -> BaseSongFile:
        return OpusSongFile(path)
