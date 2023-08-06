__all__ = ["Mp3SongFile"]

from typing import List, Optional, Tuple, cast
from contextlib import contextmanager
import requests

from mutagen.mp3 import MP3, EasyMP3
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, COMM, WOAS, USLT, SYLT
from mutagen.id3._specs import Encoding

from yumee.classes import TagPreset, LRCHelper
from .abstract_song_file import AbstractSongFile


class Mp3SongFile(AbstractSongFile[MP3]):
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
            albumartist="albumartist",
            discnumber="discnumber",
            cpil="cpil",
            albumart="APIC",
            encodedby="encodedby",
            copyright="copyright",
            tempo="tempo",
            lyrics="lyrics",
            explicit="explicit",
            woas="woas",
        )

    def _load(self) -> MP3:
        return EasyMP3(self._path)

    def save(self) -> None:
        self._audio_file.save(v2_version=3)

    @contextmanager
    def _full_mp3(self):
        self.save()
        mp3 = MP3(self._path)

        try:
            yield mp3
        finally:
            mp3.save()
            self._audio_file = self._load()

    # Artists

    @property
    def artists(self) -> Optional[List[str]]:
        artists = self._audio_file.get(self.tag_preset.artist)

        if artists is None:
            return None

        return [a for artist in artists for a in artist.split("/")]

    @artists.setter
    def artists(self, new_artists: Optional[List[str]]) -> None:
        self._audio_file[self.tag_preset.artist] = new_artists

    # Comments

    @property
    def comments(self) -> Optional[List[str]]:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)
            comms = tags.getall("COMM")

            return [
                comment
                for comm in comms
                for text in comm.text
                for comment in text.split("/")
            ]

    @comments.setter
    def comments(self, new_comments: Optional[List[str]]) -> None:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)

            if new_comments is None:
                tags.delall("COMM")
            else:
                tags.add(COMM(encoding=3, text=new_comments))

    # Track Number

    @property
    def track_number(self) -> Optional[Tuple[int, int]]:
        tracknumber = self._audio_file.get(self.tag_preset.tracknumber)

        if not tracknumber:
            return None

        trackinfo = cast(str, tracknumber[0])
        [trackn, trackc] = trackinfo.split("/")

        return (int(trackn), int(trackc))

    @track_number.setter
    def track_number(self, new_track_number: Optional[Tuple[int, int]]) -> None:
        if new_track_number is None:
            self._audio_file[self.tag_preset.tracknumber] = None
        else:
            trackn = new_track_number[0]
            trackc = new_track_number[1]

            trackinfo = f"{str(trackn)}/{str(trackc)}"

            self._audio_file[self.tag_preset.tracknumber] = [trackinfo]

    # Disc Number

    @property
    def disc_number(self) -> Optional[Tuple[int, int]]:
        discnumber = self._audio_file.get(self.tag_preset.discnumber)

        if not discnumber:
            return None

        discinfo = cast(str, discnumber[0])
        [discn, discc] = discinfo.split("/")

        return (int(discn), int(discc))

    @disc_number.setter
    def disc_number(self, new_disc_number: Optional[Tuple[int, int]]) -> None:
        if new_disc_number is None:
            self._audio_file[self.tag_preset.discnumber] = None
        else:
            discn = new_disc_number[0]
            discc = new_disc_number[1]

            discinfo = f"{str(discn)}/{str(discc)}"

            self._audio_file[self.tag_preset.discnumber] = [discinfo]

    # Genres

    @property
    def genres(self) -> Optional[List[str]]:
        genres = self._audio_file.get(self.tag_preset.genre)

        if genres is None:
            return None

        return [g for genre in genres for g in genre.split("/")]

    @genres.setter
    def genres(self, new_genres: Optional[List[str]]) -> None:
        if new_genres is None:
            self._audio_file[self.tag_preset.genre] = None
        else:
            self._audio_file[self.tag_preset.genre] = [
                genre.title() for genre in new_genres
            ]

    # Cover URL

    @property
    def cover_url(self) -> Optional[str]:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)
            apic = tags.getall("APIC")

            if len(apic) < 1:
                return None

            return [tag.desc for tag in apic if tag.desc][0]

    @cover_url.setter
    def cover_url(self, new_cover_url: Optional[str]) -> None:
        if new_cover_url is None:
            with self._full_mp3() as mp3:
                tags = cast(ID3, mp3.tags)
                tags.delall("APIC")

            return None

        try:
            cover_data = requests.get(new_cover_url, timeout=10).content
        except Exception:
            self._logger.error(
                "Wasn't able to fetch the cover data at URL `%s`", new_cover_url
            )
            return None

        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)

            tags[self.tag_preset.albumart] = APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,
                desc=new_cover_url,
                data=cover_data,
            )

    # Lyrics

    @property
    def lyrics(self) -> Optional[List[str]]:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)
            sylt = tags.getall("SYLT")
            uslt = tags.getall("USLT")

            if len(sylt) > 0:
                # There are lyrics in synchronized format
                # Return a lrc formatted string
                return [LRCHelper.generate_lrc(tag.text) for tag in sylt if tag.text]

            if len(uslt) > 0:
                # There are no lyrics in synchronized format
                # Return the raw lyrics
                return [tag.text for tag in uslt if tag.text]

            return None

    @lyrics.setter
    def lyrics(self, new_lyrics: Optional[List[str]]) -> None:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)

            if not new_lyrics:
                tags.delall("USLT")
                tags.delall("SYLT")
            else:
                self._embed_lyrics(tags, new_lyrics[0])

    def _embed_lyrics(self, tags: ID3, lyrics: str) -> None:
        if not LRCHelper.is_lrc(lyrics):
            # Lyrics are not in lrc format
            # Embed them normally
            tags.add(USLT(encoding=Encoding.UTF8, text=lyrics))
        else:
            # Lyrics are in lrc format
            # Embed them as SYLT id3 tag
            lrc_data = LRCHelper.extract_data(lyrics)

            tags.add(USLT(encoding=3, text=lyrics))
            tags.add(SYLT(encoding=Encoding.UTF8, text=lrc_data, format=2, type=1))

    ## Origin website

    @property
    def origin_website(self) -> Optional[List[str]]:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)
            woas = tags.getall("WOAS")

            return [f.url for f in woas]

    @origin_website.setter
    def origin_website(self, new_origin_website: Optional[List[str]]) -> None:
        with self._full_mp3() as mp3:
            tags = cast(ID3, mp3.tags)

            if new_origin_website is None:
                tags.delall("WOAS")
            else:
                tags.add(WOAS(encoding=3, url=new_origin_website[0]))
