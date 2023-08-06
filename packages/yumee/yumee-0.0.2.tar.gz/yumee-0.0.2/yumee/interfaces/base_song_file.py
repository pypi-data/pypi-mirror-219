from __future__ import annotations

import abc
from typing import List, Optional, Protocol, Tuple

__all__ = ["BaseSongFile"]


class BaseSongFile(Protocol):
    @abc.abstractmethod
    def __enter__(self) -> BaseSongFile:
        ...

    @abc.abstractmethod
    def __exit__(self, type, value, traceback):
        ...

    @abc.abstractmethod
    def save(self) -> None:
        ...

    # Title

    @property
    @abc.abstractmethod
    def title(self) -> Optional[List[str]]:
        ...

    @title.setter
    @abc.abstractmethod
    def title(self, new_title: Optional[List[str]]) -> None:
        ...

    # Artists

    @property
    @abc.abstractmethod
    def artists(self) -> Optional[List[str]]:
        ...

    @artists.setter
    @abc.abstractmethod
    def artists(self, new_artists: Optional[List[str]]) -> None:
        ...

    # Album Name

    @property
    @abc.abstractmethod
    def album_name(self) -> Optional[List[str]]:
        ...

    @album_name.setter
    @abc.abstractmethod
    def album_name(self, new_album_name: Optional[List[str]]) -> None:
        ...

    # Album Artists

    @property
    @abc.abstractmethod
    def album_artist(self) -> Optional[List[str]]:
        ...

    @album_artist.setter
    @abc.abstractmethod
    def album_artist(self, new_album_artist: Optional[List[str]]) -> None:
        ...

    # Track Number

    @property
    @abc.abstractmethod
    def track_number(self) -> Optional[Tuple[int, int]]:
        ...

    @track_number.setter
    @abc.abstractmethod
    def track_number(self, new_track_number: Optional[Tuple[int, int]]) -> None:
        ...

    # Disc Number

    @property
    @abc.abstractmethod
    def disc_number(self) -> Optional[Tuple[int, int]]:
        ...

    @disc_number.setter
    @abc.abstractmethod
    def disc_number(self, new_disc_number: Optional[Tuple[int, int]]) -> None:
        ...

    # Genres

    @property
    @abc.abstractmethod
    def genres(self) -> Optional[List[str]]:
        ...

    @genres.setter
    @abc.abstractmethod
    def genres(self, new_genres: Optional[List[str]]) -> None:
        ...

    # Date

    @property
    @abc.abstractmethod
    def date(self) -> Optional[List[str]]:
        ...

    @date.setter
    @abc.abstractmethod
    def date(self, new_date: Optional[List[str]]) -> None:
        ...

    # Year

    @property
    @abc.abstractmethod
    def year(self) -> Optional[int]:
        ...

    @year.setter
    @abc.abstractmethod
    def year(self, new_year: Optional[int]) -> None:
        ...

    # Explicit

    @property
    @abc.abstractmethod
    def explicit(self) -> Optional[bool]:
        ...

    @explicit.setter
    @abc.abstractmethod
    def explicit(self, new_explicit: Optional[bool]) -> None:
        ...

    # Cover

    @property
    @abc.abstractmethod
    def cover_url(self) -> Optional[str]:
        ...

    @cover_url.setter
    @abc.abstractmethod
    def cover_url(self, new_cover_url: Optional[str]) -> None:
        ...

    # Lyrics

    @property
    @abc.abstractmethod
    def lyrics(self) -> Optional[List[str]]:
        ...

    @lyrics.setter
    @abc.abstractmethod
    def lyrics(self, new_lyrics: Optional[List[str]]) -> None:
        ...

    # Comments

    @property
    @abc.abstractmethod
    def comments(self) -> Optional[List[str]]:
        ...

    @comments.setter
    @abc.abstractmethod
    def comments(self, new_comments: Optional[List[str]]) -> None:
        ...

    # Publisher

    @property
    @abc.abstractmethod
    def publisher(self) -> Optional[List[str]]:
        ...

    @publisher.setter
    @abc.abstractmethod
    def publisher(self, new_publisher: Optional[List[str]]) -> None:
        ...

    # Copyright Text

    @property
    @abc.abstractmethod
    def copyright_text(self) -> Optional[List[str]]:
        ...

    @copyright_text.setter
    @abc.abstractmethod
    def copyright_text(self, new_copyright_text: Optional[List[str]]) -> None:
        ...

    ## Origin website

    @property
    @abc.abstractmethod
    def origin_website(self) -> Optional[List[str]]:
        ...

    @origin_website.setter
    @abc.abstractmethod
    def origin_website(self, new_origin_website: Optional[List[str]]) -> None:
        ...
