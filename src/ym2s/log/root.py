import logging
import sys

from ym2s.log.format import ColoredFormatter


def get_root_logger():
    logger = logging.getLogger('YM2S')
    logger.setLevel(logging.DEBUG)
    stdout = logging.StreamHandler(sys.stdout)
    stdout.setFormatter(ColoredFormatter())
    logger.addHandler(stdout)

    return logger
