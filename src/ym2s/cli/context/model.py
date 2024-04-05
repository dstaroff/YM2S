import logging
from dataclasses import dataclass

import cloup
import inflect


@dataclass
class Context:
    logger: logging.Logger
    inflect_engine: inflect.engine


def get_context(ctx: cloup.Context) -> Context:
    """
    Gets Context object stored in cli context object
    """
    return ctx.obj


def set_context(ctx: cloup.Context, new_ctx: Context):
    """
    Puts Context object into cli context object
    """
    ctx.obj = new_ctx
