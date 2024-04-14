"""Playlist model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mustopt import MustOpt

from ym2s.core.serialization import ISerializer
from ym2s.core.subject.track import Track


@dataclass
class Playlist(ISerializer):
    """Playlist model."""

    title: str
    tracks: tuple[Track, ...]
    cover: MustOpt[bytes]

    def serialize(self: Playlist) -> dict[str, Any]:
        """Serialize playlist to dict."""
        res: dict[str, Any] = {
            'title': self.title,
            'tracks': [track.serialize() for track in self.tracks],
            'id': self.id,
        }
        if self.cover.valid():
            res.update({'cover': self.cover.must().decode('ascii')})
        return res

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> Playlist:
        """Deserialize playlist from dict."""
        return cls(
            title=obj['title'],
            tracks=tuple(Track.deserialize(track) for track in obj['tracks']),
            cover=MustOpt.new(bytes(str(obj['cover']).encode('ascii')))
            if obj.get('cover') is not None
            else MustOpt[bytes](),
            id=obj['id'],
        )

    def __lt__(self, other: Playlist) -> bool:
        if self.tracks < other.tracks:
            return True
        return self.title < other.title

    def __gt__(self, other: Playlist) -> bool:
        if self.tracks > other.tracks:
            return True
        return self.title > other.title
