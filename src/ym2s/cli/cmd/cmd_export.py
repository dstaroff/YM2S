"""Export command."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

import click
import cloup
from humanfriendly.terminal.spinners import AutomaticSpinner

from ym2s.cli.context import get_context
from ym2s.cli.option import ym_token_option
from ym2s.core.client import YMClient
from ym2s.core.serialization import SerializationBackend
from ym2s.core.subject import Subjects

if TYPE_CHECKING:
    from pathlib import Path


class Subject(str, Enum):
    """Subjects available for an export."""

    All = 'all'
    Tracks = 'tracks'

    def __str__(self) -> str:
        return self.value


@cloup.command(
    'export',
    short_help='Exports subjects from Yandex Music.',
    help='Exports subjects (liked tracks, albums, etc., and playlists) from Yandex Music.',
)
@ym_token_option
@cloup.option(
    '-s',
    '--subjects',
    'subjects_to_export',
    help='Subject to be exported.',
    type=cloup.Choice(choices=(Subject.All, Subject.Tracks), case_sensitive=False),
    multiple=True,
    default=[Subject.All],
)
@cloup.option(
    '-o',
    '--output',
    help='Path to the file to save exported items to. Format must be one of '
    + ', '.join((SerializationBackend.JSON, SerializationBackend.YAML))  # noqa: FLY002
    + '.',
    type=cloup.types.file_path(writable=True, resolve_path=True),
    required=True,
)
@cloup.pass_context
def export_cmd(c: cloup.Context, ym_token: str, output: Path, subjects_to_export: list[Subject]):
    """Export subjects."""
    backend = None
    for out_format in (SerializationBackend.JSON, SerializationBackend.YAML):
        if str(output).endswith(f'.{out_format}'):
            backend = out_format
    if backend is None:
        click.echo(
            'Unsupported output format. Must be one of '
            + ', '.join((SerializationBackend.JSON, SerializationBackend.YAML)),  # noqa: FLY002
            err=True,
        )
        c.exit(1)

    if Subject.All in subjects_to_export:
        if len(subjects_to_export) > 1:
            click.echo(
                f'Other subjects could not be specified if {Subject.All} provided',
                err=True,
            )
            c.exit(1)

        subjects_to_export = [
            Subject.Tracks,
        ]

    ctx = get_context(c)

    ym_client = YMClient(token=ym_token, ie=ctx.inflect_engine, logger=ctx.logger)
    ym_client.init()

    subjects = Subjects(ctx.inflect_engine, ctx.logger)

    if Subject.Tracks in subjects_to_export:
        with AutomaticSpinner('Exporting tracks'):
            tracks = ym_client.tracks()
            subjects.tracks = tracks

    with AutomaticSpinner(f'Writing subjects to {output}'):
        subjects.dump(output, backend)
