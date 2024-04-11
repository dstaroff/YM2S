"""Colored formatter for terminal log."""

from __future__ import annotations

import logging

from colorama import Fore

_FORMAT = '%(message)s'

_FORMATS: dict[int, str] = {
    logging.DEBUG: Fore.WHITE + _FORMAT + Fore.RESET,
    logging.INFO: Fore.LIGHTWHITE_EX + _FORMAT + Fore.RESET,
    logging.WARNING: Fore.LIGHTYELLOW_EX + _FORMAT + Fore.RESET,
    logging.ERROR: Fore.RED + _FORMAT + Fore.RESET,
    logging.CRITICAL: Fore.LIGHTRED_EX + _FORMAT + Fore.RESET,
}


class ColoredFormatter(logging.Formatter):
    """Colored formatter for terminal log."""

    def format(self, record: logging.LogRecord):
        """Format specified record with colors based on log level."""
        self._style._fmt = _FORMATS[record.levelno]  # noqa:SLF001
        return super().format(record)
