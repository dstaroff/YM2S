from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SerializerMixin(ABC):
    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """
        Encodes object to internal dict representation
        """

    @classmethod
    @abstractmethod
    def deserialize(cls, obj: dict[str, Any]):
        """
        Decodes object from internal dict representation
        """
