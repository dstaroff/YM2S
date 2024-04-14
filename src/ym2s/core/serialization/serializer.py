"""Serializer interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class ISerializer(ABC):
    """Serializer interface.

    Requires an object to be serializable to/from dict.
    """

    id: str

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Encode object as dict."""

    @classmethod
    @abstractmethod
    def deserialize(cls, obj: dict[str, Any]):
        """Decode object from dict."""

    @abstractmethod
    def __lt__(self, other):
        """Less-than object comparator.

        Needed for sorting objects in exported file.
        """

    @abstractmethod
    def __gt__(self, other):
        """Greater-than object comparator.

        Needed for sorting objects in exported file.
        """

    def __eq__(self, other: object) -> bool:
        """Equality object comparator."""
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Object hash."""
        return hash(self.id)
