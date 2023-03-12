import click

from tictot.app import TictotApp
from tictot.commands.export import export


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        app = TictotApp()
        app.run()
    else:
        ctx.invoked_subcommand


cli.add_command(export)

if __name__ == "__main__":
    cli()
