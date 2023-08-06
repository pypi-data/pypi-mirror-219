from pathlib import Path

from yumee.classes.handlers import AbstractSongFileProvider
from yumee.classes.song_files import OggSongFile
from yumee.interfaces import BaseSongFile

__all__ = ["OggSongFileProvider"]


class OggSongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "ogg"

    def _new_song_file(self, path: Path) -> BaseSongFile:
        return OggSongFile(path)
