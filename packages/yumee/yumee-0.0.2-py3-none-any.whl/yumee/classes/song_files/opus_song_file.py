__all__ = ["OpusSongFile"]

import base64
from typing import List, Optional, Tuple
from mutagen.flac import Picture
from mutagen.oggopus import OggOpus
import requests

from yumee.classes import TagPreset
from .abstract_song_file import AbstractSongFile


class OpusSongFile(AbstractSongFile[OggOpus]):
    @property
    def tag_preset(self) -> TagPreset:
        return TagPreset(
            album="album",
            artist="artist",
            date="date",
            title="title",
            year="year",
            comment="comment",
            group="group",
            writer="writer",
            genre="genre",
            tracknumber="tracknumber",
            trackcount="tracktotal",
            albumartist="albumartist",
            discnumber="discnumber",
            disccount="disctotal",
            cpil="cpil",
            albumart="metadata_block_picture",
            encodedby="encodedby",
            copyright="copyright",
            tempo="tempo",
            lyrics="lyrics",
            explicit="explicit",
            woas="woas",
        )

    def _load(self) -> OggOpus:
        return OggOpus(self._path)

    # Download URL

    @property
    def comments(self) -> Optional[List[str]]:
        return self._audio_file.get(self.tag_preset.comment)

    @comments.setter
    def comments(self, new_comments: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.comment] = new_comments

    # Track Number

    @property
    def track_number(self) -> Optional[Tuple[int, int]]:
        tracknumber = self._audio_file.get(self.tag_preset.tracknumber)
        trackcount = self._audio_file.get(self.tag_preset.trackcount)

        if not tracknumber:
            return None

        trackn = int(tracknumber[0])
        trackc = int(trackcount[0]) if trackcount else 0

        return (trackn, trackc)

    @track_number.setter
    def track_number(self, new_track_number: Optional[Tuple[int, int]]) -> None:
        if new_track_number is None:
            self._audio_file[self.tag_preset.tracknumber] = None
            self._audio_file[self.tag_preset.trackcount] = None
        else:
            trackn = new_track_number[0]
            trackc = new_track_number[1]

            trackcount = str(trackc)
            tracknumber = str(trackn).zfill(len(trackcount))

            self._audio_file[self.tag_preset.tracknumber] = tracknumber
            self._audio_file[self.tag_preset.trackcount] = trackcount

    # Disc Number

    @property
    def disc_number(self) -> Optional[Tuple[int, int]]:
        discnumber = self._audio_file.get(self.tag_preset.discnumber)
        disccount = self._audio_file.get(self.tag_preset.disccount)

        if not discnumber:
            return None

        discn = int(discnumber[0])
        discc = int(disccount[0]) if disccount else 0

        return (discn, discc)

    @disc_number.setter
    def disc_number(self, new_disc_number: Optional[Tuple[int, int]]) -> None:
        if new_disc_number is None:
            self._audio_file[self.tag_preset.discnumber] = None
            self._audio_file[self.tag_preset.disccount] = None
        else:
            discn = new_disc_number[0]
            discc = new_disc_number[1]

            disccount = str(discc)
            discnumber = str(discn).zfill(len(disccount))

            self._audio_file[self.tag_preset.discnumber] = discnumber
            self._audio_file[self.tag_preset.disccount] = disccount

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

        picture = Picture()
        picture.type = 3
        picture.desc = new_cover_url
        picture.mime = "image/jpeg"
        picture.data = cover_data

        image_data = picture.write()
        encoded_data = base64.b64encode(image_data)
        vcomment_value = encoded_data.decode("ascii")

        self._audio_file[self.tag_preset.albumart] = [vcomment_value]

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
        return self._audio_file.get(self.tag_preset.woas)

    @origin_website.setter
    def origin_website(self, new_origin_website: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.woas] = new_origin_website
