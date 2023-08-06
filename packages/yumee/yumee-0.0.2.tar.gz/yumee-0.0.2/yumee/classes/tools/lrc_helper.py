__all__ = ["LRCHelper"]

import re
from typing import List, Tuple


class LRCHelper:
    LRC_REGEX = re.compile(r"(\[\d{2}:\d{2}.\d{2,3}\])")

    @classmethod
    def is_lrc(cls, lyrics: str) -> bool:
        # Check if the lyrics are in lrc format
        # using regex on the first 5 lines
        lrc_lines = lyrics.splitlines()[:5]
        return any(line and cls.LRC_REGEX.match(line) for line in lrc_lines)

    @classmethod
    def extract_data(cls, lrc_string: str) -> List[Tuple[str, float]]:
        lrc_data = []

        for line in lrc_string.splitlines():
            time_tag = line.split("]", 1)[0] + "]"
            text = line.replace(time_tag, "")

            time_tag = time_tag.replace("[", "")
            time_tag = time_tag.replace("]", "")
            time_tag = time_tag.replace(".", ":")
            time_tag_vals = time_tag.split(":")
            if len(time_tag_vals) != 3 or any(
                not isinstance(tag, int) for tag in time_tag_vals
            ):
                continue

            minute, sec, millisecond = time_tag_vals
            time = cls._to_ms(min=int(minute), sec=int(sec), ms=int(millisecond))
            lrc_data.append((text, time))

        return lrc_data

    @classmethod
    def _to_ms(cls, hour: int = 0, min: int = 0, sec: int = 0, ms: int = 0) -> float:
        return 3600 * 1000 * hour + min * 60 * 1000 + sec * 1000 + ms

    @classmethod
    def generate_lrc(cls, lrc_data: List[Tuple[str, float]]) -> str:
        lrc_lines: List[str] = []

        for data in lrc_data:
            text, time = data

            ms = int(data[1] % 1000)
            sec = int(((time - ms) / 1000) % 60)
            min = int(((time - 1000 * sec - ms) / 60_000) % 60)

            lrc_lines.append(f"[{min}:{sec}.{ms}]{text}")

        return "\n".join(lrc_lines)
