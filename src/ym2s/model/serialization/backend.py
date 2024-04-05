from enum import Enum


class SerializationBackend(str, Enum):
    """
    Backend to use for data serialization
    """

    JSON = 'json'
    YAML = 'yaml'

    def __str__(self) -> str:
        return self.value
