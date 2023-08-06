from dataclasses import dataclass
from typing import List, Optional

__all__ = ["SongMetadata"]


@dataclass
class SongMetadata:
    title: Optional[str] = None
    artist: Optional[str] = None
    artists: Optional[List[str]] = None
    album_name: Optional[str] = None
    album_artist: Optional[str] = None
    track_number: Optional[int] = None
    track_count: Optional[int] = None
    disc_number: Optional[int] = None
    disc_count: Optional[int] = None
    genres: Optional[List[str]] = None
    date: Optional[str] = None
    year: Optional[int] = None
    explicit: Optional[bool] = None
    cover_url: Optional[str] = None
    lyrics: Optional[str] = None
    comments: Optional[List[str]] = None
    origin_website: Optional[str] = None
    publisher: Optional[str] = None
    copyright_text: Optional[str] = None
