from pathlib import Path

from yumee.classes.handlers import AbstractSongFileProvider
from yumee.classes.song_files import M4ASongFile
from yumee.interfaces import BaseSongFile

__all__ = ["M4ASongFileProvider"]


class M4ASongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "m4a"

    def _new_song_file(self, path: Path) -> BaseSongFile:
        return M4ASongFile(path)
