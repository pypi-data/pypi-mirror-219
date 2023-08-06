from pathlib import Path
from taipan_di import ServiceCollection

from yumee.classes import SongMetadata
from yumee.di import add_yumee
from yumee.errors import SongMetadataFileError
from yumee.interfaces import BaseSongFile, BaseSongFileProvider

__all__ = ["SongMetadataEmbedder"]


class SongMetadataEmbedder:
    def __init__(self) -> None:
        services = ServiceCollection()
        add_yumee(services)
        provider = services.build()

        self._provider = provider.resolve(BaseSongFileProvider)

    def embed(self, path: Path, metadata: SongMetadata) -> None:
        with self.open_file(path) as song_file:
            if metadata.album_artist:
                song_file.album_artist = [metadata.album_artist]
            elif metadata.artist:
                song_file.album_artist = [metadata.artist]

            if metadata.album_name:
                song_file.album_name = [metadata.album_name]
            if metadata.artists:
                song_file.artists = metadata.artists
            if metadata.comments:
                song_file.comments = metadata.comments
            if metadata.copyright_text:
                song_file.copyright_text = [metadata.copyright_text]
            if metadata.cover_url:
                song_file.cover_url = metadata.cover_url
            if metadata.date:
                song_file.date = [metadata.date]
            if metadata.disc_number:
                song_file.disc_number = (
                    metadata.disc_number,
                    metadata.disc_count if metadata.disc_count else metadata.disc_number,
                )
            if metadata.explicit:
                song_file.explicit = metadata.explicit
            if metadata.genres:
                song_file.genres = metadata.genres
            if metadata.lyrics:
                song_file.lyrics = [metadata.lyrics]
            if metadata.origin_website:
                song_file.origin_website = [metadata.origin_website]
            if metadata.publisher:
                song_file.publisher = [metadata.publisher]
            if metadata.title:
                song_file.title = [metadata.title]
            if metadata.track_number:
                song_file.track_number = (
                    metadata.track_number,
                    metadata.track_count if metadata.track_count else metadata.track_number,
                )
            if metadata.year:
                song_file.year = metadata.year

    def open_file(self, path: Path) -> BaseSongFile:
        song_file = self._provider.exec(path)

        if song_file is None:
            raise SongMetadataFileError(
                f"Couldn't open file at path {path}. The extension might not be supported."
            )

        return song_file
