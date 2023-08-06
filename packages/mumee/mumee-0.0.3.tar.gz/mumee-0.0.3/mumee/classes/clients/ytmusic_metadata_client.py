from typing import Any, Dict, List, Tuple
from ytmusicapi import YTMusic
from rapidfuzz import fuzz
from slugify import slugify

from mumee.classes import SongMetadata, PlaylistMetadata
from mumee.errors import MetadataClientError

__all__ = ["YTMusicMetadataClient"]


class YTMusicMetadataClient:
    def __init__(self) -> None:
        self._client = YTMusic()

    def get_track(self, url: str) -> SongMetadata:
        if "music.youtube.com" not in url or "watch?v" not in url:
            raise MetadataClientError(f"Invalid Youtube Music track URL: {url}")

        start_index = url.find("?v=") + len("?v=")
        end_index = url.find("&", start_index) if url.find("&", start_index) >= 0 else None
        track_info = self._client.get_song(url[start_index:end_index])

        if not track_info or track_info["playabilityStatus"]["status"] == "ERROR":
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL: {url}"
            )

        return self.search(
            f"{track_info['videoDetails']['title']} - {track_info['videoDetails']['author']}"
        )

    def get_playlist(self, url: str) -> PlaylistMetadata:
        if "music.youtube.com" not in url or "playlist?list" not in url:
            raise MetadataClientError(f"Invalid Youtube Music playlist URL: {url}")

        start_index = url.find("?list=") + len("?list=")
        end_index = url.find("&", start_index) if url.find("&", start_index) >= 0 else None
        playlist_info = self._client.get_playlist(url[start_index:end_index], None)  # type: ignore

        if not playlist_info:
            raise MetadataClientError(
                f"Couldn't get metadata associated with this URL: {url}"
            )

        result = PlaylistMetadata(
            name=playlist_info["title"],
            description=playlist_info["description"],
            author=playlist_info["author"]["name"],
            tracks=[
                self.search(
                    f"{track['title']} - {', '.join([artist['name'] for artist in track['artists']])}"
                )
                for track in playlist_info["tracks"]
            ],
        )
        return result

    def search(self, query: str) -> SongMetadata:
        search_results = self._client.search(query, "songs")

        if search_results is None or len(search_results) == 0:
            raise MetadataClientError(f"No result found for '{query}'")

        best_result = self._get_best_result(query, search_results)

        if best_result[2] < 55:
            raise MetadataClientError(
                "Best match found isn't close enough to your query. "
                f"Best match : {best_result[1]}, query: {query}"
            )

        track_info = best_result[0]
        if track_info.get("album", {}).get("id") is not None:
            album_info = self._client.get_album(track_info["album"]["id"])
        else:
            album_info = None

        result = SongMetadata(
            name=track_info["title"],
            artists=[artist["name"] for artist in track_info["artists"]],
            artist=track_info["artists"][0]["name"],
            album_name=album_info["title"] if album_info is not None else None,
            album_artist=album_info["artists"][0]["name"]
            if album_info is not None
            else None,
            disc_number=None,
            disc_count=None,
            track_number=[
                idx
                for idx, track in enumerate(album_info["tracks"])
                if fuzz.ratio(track["title"], track_info["title"]) > 80
            ][0]
            if album_info is not None
            else None,
            track_count=album_info["trackCount"] if album_info is not None else None,
            genres=[],
            duration=track_info["duration_seconds"],
            date=None,
            year=int(album_info["year"]) if album_info is not None else None,
        )

        return result

    def _get_best_result(
        self, query: str, tracks_info: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], str, float]:
        best_score = 0
        best_result = None
        best_query = ""
        has_album = False

        for track in tracks_info:
            track_name = track["title"]
            track_artists = [artist["name"] for artist in track["artists"]]
            track_query = f"{track_name} - {', '.join(track_artists)}"
            track_has_album = (
                track["album"] is not None and track["album"]["id"] is not None
            )

            score = fuzz.ratio(slugify(track_query), slugify(query))

            if score > best_score or (
                score == best_score and track_has_album and not has_album
            ):
                best_score = score
                best_result = track
                best_query = track_query
                has_album = track_has_album

        return best_result or {}, best_query, best_score
