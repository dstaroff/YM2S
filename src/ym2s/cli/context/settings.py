from cloup import Context, HelpFormatter, HelpTheme

CONTEXT_SETTINGS = Context.settings(
    help_option_names=["-h", "--help"],
    terminal_width=120,
    align_option_groups=False,
    align_sections=True,
    show_constraints=True,
    show_default=True,
    auto_envvar_prefix='YM2S',
    formatter_settings=HelpFormatter.settings(
        theme=HelpTheme.light(),
    ),
)
