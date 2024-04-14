"""Album model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ym2s.core.serialization import ISerializer
from ym2s.core.subject.artist import Artist


@dataclass
class Album(ISerializer):
    """Album model."""

    title: str
    artists: tuple[Artist, ...]

    def serialize(self: Album) -> dict[str, Any]:
        """Serialize album to dict."""
        return {
            'title': self.title,
            'artists': [artist.serialize() for artist in self.artists],
            'id': self.id,
        }

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> Album:
        """Deserialize album from dict."""
        return cls(
            title=obj['title'],
            artists=tuple(Artist.deserialize(artist) for artist in obj['artists']),
            id=obj['id'],
        )

    def __lt__(self, other: Album) -> bool:
        if self.artists < other.artists:
            return True
        return self.title < other.title

    def __gt__(self, other: Album) -> bool:
        if self.artists > other.artists:
            return True
        return self.title > other.title
