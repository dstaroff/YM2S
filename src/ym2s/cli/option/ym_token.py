import cloup

ym_token_option = cloup.option(
    '-t',
    '--ym-token',
    'ym_token',
    help='Access token for Yandex Music account.',
    type=str,
    show_envvar=True,
    allow_from_autoenv=True,
    required=True,
)
