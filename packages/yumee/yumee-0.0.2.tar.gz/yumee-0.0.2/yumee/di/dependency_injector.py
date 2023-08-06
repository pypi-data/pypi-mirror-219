from taipan_di import ServiceCollection

from yumee.classes import (
    FlacSongFileProvider,
    M4ASongFileProvider,
    Mp3SongFileProvider,
    OggSongFileProvider,
    OpusSongFileProvider,
)
from yumee.interfaces import BaseSongFileProvider

__all__ = ["add_yumee"]


def add_yumee(services: ServiceCollection) -> ServiceCollection:
    services.register_pipeline(BaseSongFileProvider).add(FlacSongFileProvider).add(
        M4ASongFileProvider
    ).add(Mp3SongFileProvider).add(OggSongFileProvider).add(
        OpusSongFileProvider
    ).as_factory()

    return services
