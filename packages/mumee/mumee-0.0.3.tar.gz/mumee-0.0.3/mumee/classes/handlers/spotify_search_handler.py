from typing import Callable, Union

from mumee.interfaces import BaseMetadataClient
from mumee.classes import (
    SpotifyMetadataClient,
    SongMetadata,
    PlaylistMetadata,
)

__all__ = ["SpotifySearchHandler"]


class SpotifySearchHandler(BaseMetadataClient):
    def __init__(self, client: SpotifyMetadataClient) -> None:
        super().__init__()
        self._client = client

    def _handle(
        self, request: str, next: Callable[[str], Union[SongMetadata, PlaylistMetadata]]
    ) -> Union[SongMetadata, PlaylistMetadata]:
        try:
            return self._client.search(request)
        except:
            return next(request)
