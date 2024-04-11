"""CLI root command."""

import cloup
import inflect

from ym2s.cli.cmd import export_cmd
from ym2s.cli.context import CONTEXT_SETTINGS, Context, set_context
from ym2s.core.log import get_root_logger


@cloup.group(
    'ym2s',
    context_settings=CONTEXT_SETTINGS,
)
@cloup.pass_context
def cli(ctx: cloup.Context):
    """Yandex Music to Spotify syncer."""
    logger = get_root_logger()
    set_context(
        ctx,
        Context(
            logger=logger,
            inflect_engine=inflect.engine(),
        ),
    )


cli.add_command(export_cmd)
