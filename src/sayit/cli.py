"""SayIt CLI entry point."""

import click
from sayit import __version__


@click.group()
@click.version_option(version=__version__, prog_name="sayit")
def main():
    """SayIt - Local, privacy-focused voice-to-text."""
    pass


if __name__ == "__main__":
    main()
