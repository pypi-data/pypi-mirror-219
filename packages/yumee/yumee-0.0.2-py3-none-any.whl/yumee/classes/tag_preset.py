from dataclasses import dataclass
from typing import Optional

__all__ = ["TagPreset"]


@dataclass
class TagPreset:
    album: str
    artist: str
    date: str
    title: str
    year: str
    comment: str
    group: str
    writer: str
    genre: str
    tracknumber: str
    albumartist: str
    discnumber: str
    cpil: str
    albumart: str
    encodedby: str
    copyright: str
    tempo: str
    lyrics: str
    explicit: str
    woas: str
    trackcount: Optional[str] = None
    disccount: Optional[str] = None
