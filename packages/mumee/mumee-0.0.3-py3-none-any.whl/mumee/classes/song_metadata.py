from dataclasses import dataclass
from typing import List, Optional

__all__ = ["SongMetadata"]


@dataclass
class SongMetadata:
    name: str
    artists: List[str]
    artist: str
    genres: List[str]
    disc_number: Optional[int]
    disc_count: Optional[int]
    album_name: Optional[str]
    album_artist: Optional[str]
    duration: int
    year: Optional[int]
    date: Optional[str]
    track_number: Optional[int]
    track_count: Optional[int]
