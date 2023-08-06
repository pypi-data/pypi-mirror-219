from pathlib import Path

from yumee.classes.handlers import AbstractSongFileProvider
from yumee.classes.song_files import Mp3SongFile
from yumee.interfaces import BaseSongFile

__all__ = ["Mp3SongFileProvider"]


class Mp3SongFileProvider(AbstractSongFileProvider):
    @property
    def encoding(self) -> str:
        return "mp3"

    def _new_song_file(self, path: Path) -> BaseSongFile:
        return Mp3SongFile(path)
