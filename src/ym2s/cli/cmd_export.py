from enum import Enum

import click
import cloup
from humanfriendly.terminal.spinners import AutomaticSpinner

from ym2s.cli.context import get_context
from ym2s.cli.option import ym_token_option
from ym2s.client.yandex import YMClient
from ym2s.importer import ExportedSubjects
from ym2s.model.serialization import SerializationBackend


class SubjectEnum(str, Enum):
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
    help='Subject to be exported.',
    type=cloup.Choice(
        choices=(SubjectEnum.All, SubjectEnum.Tracks), case_sensitive=False
    ),
    multiple=True,
    default=[SubjectEnum.All],
)
@cloup.option(
    '-o',
    '--output',
    help='Path to the file to save exported items to. Format must be one of '
    + ', '.join((SerializationBackend.JSON, SerializationBackend.YAML))
    + '.',
    type=cloup.types.file_path(writable=True, resolve_path=True),
    required=True,
)
@cloup.pass_context
def cmd_export(
    c: cloup.Context, ym_token: str, output: click.Path, subjects: list[SubjectEnum]
):
    backend = None
    for out_format in (SerializationBackend.JSON, SerializationBackend.YAML):
        if str(output).endswith(f'.{out_format}'):
            backend = out_format
    if backend is None:
        click.echo(
            'Unsupported output format. Must be one of '
            + ', '.join((SerializationBackend.JSON, SerializationBackend.YAML)),
            err=True,
        )
        c.exit(1)

    if SubjectEnum.All in subjects:
        if len(subjects) > 1:
            click.echo(
                f'Other subjects could not be specified if {SubjectEnum.All} provided',
                err=True,
            )
            c.exit(1)

        subjects = [
            SubjectEnum.Tracks,
        ]

    ctx = get_context(c)

    ym_client = YMClient(token=ym_token, ie=ctx.inflect_engine, logger=ctx.logger)
    ym_client.init()

    exported_subjects = ExportedSubjects(ctx.inflect_engine, ctx.logger)

    if SubjectEnum.Tracks in subjects:
        with AutomaticSpinner('Exporting tracks'):
            tracks = ym_client.tracks()
            exported_subjects.tracks = tracks

    with AutomaticSpinner(f'Writing subjects to {output}'):
        exported_subjects.dump(str(output), backend)
