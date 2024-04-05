from dataclasses import dataclass
from typing import Any

from ym2s.model.serialization import SerializerMixin


@dataclass
class Track(SerializerMixin):
    artists: list[str]
    title: str

    def serialize(self) -> dict[str, Any]:
        return {
            'artists': self.artists,
            'title': self.title,
        }

    @classmethod
    def deserialize(cls, obj: dict[str, Any]) -> 'Track':
        return cls(
            artists=obj['artists'],
            title=obj['title'],
        )
