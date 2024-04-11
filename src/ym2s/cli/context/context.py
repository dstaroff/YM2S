"""Typed CLI context."""

from dataclasses import dataclass
import logging

import inflect


@dataclass
class Context:
    """Typed CLI context."""

    logger: logging.Logger
    inflect_engine: inflect.engine
