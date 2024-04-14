"""Track model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mustopt import MustOpt

from ym2s.core.serialization import ISerializer
from ym2s.core.subject.album import Album
from ym2s.core.subject.artist import Artist


@dataclass
class Track(ISerializer):
    """Track model."""

    title: str
    artists: tuple[Artist, ...]
    album: MustOpt[Album]

    def serialize(self: Track) -> dict[str, Any]:
        """Serialize track to dict."""
        res: dict[str, Any] = {
            'title': self.title,
            'artists': [artist.serialize() for artist in self.artists],
            'id': self.id,
        }
        if self.album.valid():
            res.update({'album': self.album.must().serialize()})
        return res

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> Track:
        """Deserialize track from dict."""
        return cls(
            title=obj['title'],
            artists=tuple(Artist.deserialize(artist) for artist in obj['artists']),
            album=MustOpt.new(Album.deserialize(obj['album'])) if obj.get('album') is not None else MustOpt[Album](),
            id=obj['id'],
        )

    def __lt__(self, other: Track) -> bool:
        if sorted(self.artists) < sorted(other.artists):
            return True
        return self.title < other.title

    def __gt__(self, other: Track) -> bool:
        if sorted(self.artists) > sorted(other.artists):
            return True
        return self.title > other.title
