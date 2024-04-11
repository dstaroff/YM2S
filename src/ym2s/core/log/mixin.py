"""Mixin to include a logger into an object."""

from logging import Logger

_LOGGER_ATTR_NAME = '_logger'


class LoggableMixin:
    """Mixin to include a logger into an object."""

    def logger(self) -> Logger:
        """Get logger."""
        logger = getattr(self, _LOGGER_ATTR_NAME, None)
        if logger is None:
            raise LoggerNotInitializedError
        return logger

    def _set_logger(self, logger: Logger) -> None:
        """Set logger."""
        setattr(self, _LOGGER_ATTR_NAME, logger)


class LoggerNotInitializedError(RuntimeError):
    """LoggableMixin based class instance should call _set_logger method."""

    def __init__(self):
        super().__init__('Not initialized logger object requested.')
