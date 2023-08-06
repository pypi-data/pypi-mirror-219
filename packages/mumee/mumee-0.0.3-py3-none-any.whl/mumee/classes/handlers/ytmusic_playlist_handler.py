from typing import Callable, Union

from mumee.interfaces import BaseMetadataClient
from mumee.classes import (
    YTMusicMetadataClient,
    SongMetadata,
    PlaylistMetadata,
)

__all__ = ["YTMusicPlaylistHandler"]


class YTMusicPlaylistHandler(BaseMetadataClient):
    def __init__(self, client: YTMusicMetadataClient) -> None:
        super().__init__()
        self._client = client

    def _handle(
        self, request: str, next: Callable[[str], Union[SongMetadata, PlaylistMetadata]]
    ) -> Union[SongMetadata, PlaylistMetadata]:
        if "music.youtube.com" not in request or "playlist?list" not in request:
            return next(request)

        return self._client.get_playlist(request)
