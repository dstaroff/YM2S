"""Serializer interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ISerializer(ABC):
    """Serializer interface.

    Requires an object to be serializable to/from dict.
    """

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """Encode object as dict."""

    @classmethod
    @abstractmethod
    def deserialize(cls, obj: dict[str, Any]):
        """Decode object from dict."""
