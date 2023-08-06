from typing import Callable, Union

from mumee.interfaces import BaseMetadataClient
from mumee.classes import (
    SpotifyMetadataClient,
    SongMetadata,
    PlaylistMetadata,
)

__all__ = ["SpotifyPlaylistHandler"]


class SpotifyPlaylistHandler(BaseMetadataClient):
    def __init__(self, client: SpotifyMetadataClient) -> None:
        super().__init__()
        self._client = client

    def _handle(
        self, request: str, next: Callable[[str], Union[SongMetadata, PlaylistMetadata]]
    ) -> Union[SongMetadata, PlaylistMetadata]:
        if "open.spotify.com" not in request or "playlist" not in request:
            return next(request)

        return self._client.get_playlist(request)
