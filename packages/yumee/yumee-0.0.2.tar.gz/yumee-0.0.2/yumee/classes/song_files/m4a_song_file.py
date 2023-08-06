__all__ = ["M4ASongFile"]

from typing import List, Optional, Tuple, cast
from mutagen.mp4 import MP4, MP4Cover
import requests

from yumee.classes import TagPreset
from .abstract_song_file import AbstractSongFile


class M4ASongFile(AbstractSongFile[MP4]):
    @property
    def tag_preset(self) -> TagPreset:
        return TagPreset(
            album="\xa9alb",
            artist="\xa9ART",
            date="\xa9day",
            title="\xa9nam",
            year="\xa9day",
            comment="\xa9cmt",
            group="\xa9grp",
            writer="\xa9wrt",
            genre="\xa9gen",
            tracknumber="trkn",
            albumartist="aART",
            discnumber="disk",
            cpil="cpil",
            albumart="covr",
            encodedby="\xa9too",
            copyright="cprt",
            tempo="tmpo",
            lyrics="\xa9lyr",
            explicit="rtng",
            woas="----:song-metadata-embedder:WOAS",
        )

    def _load(self) -> MP4:
        return MP4(self._path)

    # Comments

    @property
    def comments(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.comment)

    @comments.setter
    def comments(self, new_comments: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.comment] = new_comments

    # Track Number

    @property
    def track_number(self) -> Optional[Tuple[int, int]]:
        trackinfos = self._audio_file.get(self.tag_preset.tracknumber)

        if not trackinfos:
            return None

        return trackinfos[0]

    @track_number.setter
    def track_number(self, new_track_number: Optional[Tuple[int, int]]) -> None:
        self._audio_file[self.tag_preset.tracknumber] = [new_track_number]

    # Disc Number

    @property
    def disc_number(self) -> Optional[Tuple[int, int]]:
        discinfos = self._audio_file.get(self.tag_preset.discnumber)

        if not discinfos:
            return None

        return discinfos[0]

    @disc_number.setter
    def disc_number(self, new_disc_number: Optional[Tuple[int, int]]) -> None:
        self._audio_file[self.tag_preset.discnumber] = [new_disc_number]

    # Explicit

    @property
    def explicit(self) -> Optional[bool]:
        explicit = self._audio_file.get(self.tag_preset.explicit)

        return explicit is not None and explicit[0] == 4

    @explicit.setter
    def explicit(self, new_explicit: Optional[bool]) -> None:
        if new_explicit is None:
            self._audio_file[self.tag_preset.explicit] = None
        else:
            self._audio_file[self.tag_preset.explicit] = (4 if new_explicit else 2,)

    # Cover URL

    @property
    def cover_url(self) -> Optional[str]:
        if self._audio_file.get(self.tag_preset.albumart):
            return "Cover"

        return None

    @cover_url.setter
    def cover_url(self, new_cover_url: Optional[str]) -> None:
        if new_cover_url is None:
            self._audio_file[self.tag_preset.albumart] = None
            return None

        try:
            cover_data = requests.get(new_cover_url, timeout=10).content
        except Exception:
            self._logger.error(
                "Wasn't able to fetch the cover data at URL `%s`", new_cover_url
            )
            return None

        self._audio_file[self.tag_preset.albumart] = [
            MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)
        ]

    # Lyrics

    @property
    def lyrics(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.lyrics)

    @lyrics.setter
    def lyrics(self, new_lyrics: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.lyrics] = new_lyrics

    ## Origin website

    @property
    def origin_website(self) -> Optional[List[str]]:
        origin_website = self._audio_file.get(self.tag_preset.woas)

        if not origin_website:
            return None

        origin_website = cast(List[bytes], origin_website)
        return [s.decode("utf-8") for s in origin_website]

    @origin_website.setter
    def origin_website(self, new_origin_website: Optional[List[str]]) -> None:
        if new_origin_website is None:
            self._audio_file[self.tag_preset.woas] = None
        else:
            self._audio_file[self.tag_preset.woas] = [
                s.encode("utf-8") for s in new_origin_website
            ]
