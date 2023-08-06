from taipan_di import PipelineLink
from pathlib import Path

from .base_song_file import BaseSongFile

__all__ = ["BaseSongFileProvider"]


BaseSongFileProvider = PipelineLink[Path, BaseSongFile]
