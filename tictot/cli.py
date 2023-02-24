import click

from tictot.app import TictotApp


@click.command()
def run():
    app = TictotApp()
    app.run()


if __name__ == "__main__":
    run()
