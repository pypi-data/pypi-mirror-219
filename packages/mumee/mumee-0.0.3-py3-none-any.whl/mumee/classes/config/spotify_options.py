from dataclasses import dataclass
from typing import Optional

__all__ = ["SpotifyOptions"]


@dataclass
class SpotifyOptions:
    use_auth: bool = False
    client_id: Optional[str] = "ae6813fb038e438c88c9632208855f47"
    client_secret: Optional[str] = "ac0804faddcb4145ad61f392d87e272c"
    auth_token: Optional[str] = None
    use_cache: bool = False
    cache_path: Optional[str] = None
    headless: bool = False
