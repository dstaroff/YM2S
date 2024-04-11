"""Typed CLI context handling module."""

from cloup import Context as CloupContext

from .context import Context
from .settings import CONTEXT_SETTINGS


def get_context(ctx: CloupContext) -> Context:
    """Get Context object stored in CLI context object."""
    return ctx.obj


def set_context(ctx: CloupContext, new_ctx: Context):
    """Put Context object into CLI context object."""
    ctx.obj = new_ctx


__all__ = (
    'CONTEXT_SETTINGS',
    'Context',
    'get_context',
    'set_context',
)
