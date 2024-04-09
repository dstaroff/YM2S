"""YM2S CLI typed context handling package."""

from .model import Context, get_context, set_context
from .settings import CONTEXT_SETTINGS

__all__ = (
    'CONTEXT_SETTINGS',
    'Context',
    'get_context',
    'set_context',
)
