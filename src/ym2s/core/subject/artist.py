"""Artist model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ym2s.core.serialization import ISerializer


@dataclass
class Artist(ISerializer):
    """Artist model."""

    name: str

    def serialize(self: Artist) -> dict[str, Any]:
        """Serialize artist to dict."""
        return {
            'name': self.name,
            'id': self.id,
        }

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> Artist:
        """Deserialize artist from dict."""
        return cls(
            name=obj['name'],
            id=obj['id'],
        )

    def __lt__(self, other: Artist) -> bool:
        return self.name < other.name

    def __gt__(self, other: Artist) -> bool:
        return self.name > other.name
