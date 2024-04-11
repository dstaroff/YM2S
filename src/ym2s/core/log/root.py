"""Root logger getter."""

import logging
import sys

from ym2s.core.log.colored_formatter import ColoredFormatter


def get_root_logger():
    """Get root logger for YM2S."""
    logger = logging.getLogger('YM2S')
    logger.setLevel(logging.DEBUG)
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(ColoredFormatter())
    logger.addHandler(stdout)

    return logger
