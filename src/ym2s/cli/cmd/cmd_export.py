"""Export command."""

from __future__ import annotations

from typing import TYPE_CHECKING

import click
import cloup
from humanfriendly.terminal.spinners import AutomaticSpinner

from ym2s.cli.context import get_context
from ym2s.cli.option import ym_token_option
from ym2s.core.client import YMClient
from ym2s.core.serialization import SerializationBackend
from ym2s.core.subject import Subjects
from ym2s.core.subject.enum import SORT_BY_VARIANTS, SUBJECTS_ALL, SUBJECT_VARIANTS, SubjectSortBy, SubjectType

if TYPE_CHECKING:
    from pathlib import Path


@cloup.command(
    'export',
    short_help='Export subjects from Yandex Music into a file.',
    help='Export subjects (liked tracks, albums, etc., and playlists) from Yandex Music into a file.',
)
@ym_token_option
@cloup.option(
    '-S',
    '--subjects',
    'subjects_to_export',
    help='Subject to be exported.',
    type=cloup.Choice(choices=SUBJECT_VARIANTS, case_sensitive=False),
    multiple=True,
    default=[SubjectType.All],
)
@cloup.option(
    '-s',
    '--sort-by',
    help='Subject sorting order.',
    type=cloup.Choice(choices=SORT_BY_VARIANTS, case_sensitive=False),
    default=SubjectSortBy.LexicalAsc,
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
def export_cmd(
    c: cloup.Context,
    ym_token: str,
    subjects_to_export: list[SubjectType],
    sort_by: SubjectSortBy,
    output: Path,
):
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

    if SubjectType.All in subjects_to_export:
        if len(subjects_to_export) > 1:
            click.echo(
                f'Other subjects could not be specified if {SubjectType.All} provided',
                err=True,
            )
            c.exit(1)

        subjects_to_export = list(SUBJECTS_ALL)

    ctx = get_context(c)

    ym_client = YMClient(token=ym_token, ie=ctx.inflect_engine, logger=ctx.logger)
    ym_client.init()

    subjects = Subjects(ctx.inflect_engine, ctx.logger)
    for subject in [
        {
            'name': SubjectType.Artists,
            'getter': ym_client.artists,
            'setter': subjects.set_artists,
        },
        {
            'name': SubjectType.Albums,
            'getter': ym_client.albums,
            'setter': subjects.set_albums,
        },
        {
            'name': SubjectType.Tracks,
            'getter': ym_client.tracks,
            'setter': subjects.set_tracks,
        },
        {
            'name': SubjectType.Playlists,
            'getter': ym_client.playlists,
            'setter': subjects.set_playlists,
        },
    ]:
        if subject['name'] in subjects_to_export:
            with AutomaticSpinner(f'Exporting {subject["name"]}'):
                subject['setter'](subject['getter']())

    with AutomaticSpinner(f'Writing subjects to {output}'):
        subjects.dump(output, backend, sort_by)
