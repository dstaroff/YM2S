"""Track model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ym2s.core.serialization import ISerializer


@dataclass
class Track(ISerializer):
    """Track model."""

    artists: list[str]
    title: str

    def serialize(self: Track) -> dict[str, Any]:
        """Serialize track to dict."""
        return {
            'artists': self.artists,
            'title': self.title,
        }

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> Track:
        """Deserialize track from dict."""
        return cls(
            artists=obj['artists'],
            title=obj['title'],
        )
