from typing import Optional, Union
from taipan_di import ServiceCollection

from mumee.classes import SongMetadata, PlaylistMetadata, SpotifyOptions
from mumee.di import add_mumee
from mumee.interfaces import BaseMetadataClient
from mumee.errors import MetadataClientError


class SongMetadataClient:
    def __init__(self, spotify_options: Optional[SpotifyOptions] = None):
        services = ServiceCollection()
        add_mumee(services)

        if spotify_options is not None:
            services.register(SpotifyOptions).as_singleton().with_instance(spotify_options)

        self._client = services.build().resolve(BaseMetadataClient)

    def search(self, url_or_query: str) -> Union[SongMetadata, PlaylistMetadata]:
        result = self._client.exec(url_or_query)

        if result is None:
            raise MetadataClientError("No result")

        return result
