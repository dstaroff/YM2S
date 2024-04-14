"""Model serialization package."""

from .backend import SerializationBackend
from .serializer import ISerializer

__all__ = (
    'ISerializer',
    'SerializationBackend',
)
