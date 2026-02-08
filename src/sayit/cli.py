"""SayIt CLI entry point."""

import click
from rich.console import Console

from sayit import __version__

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="sayit")
def main():
    """SayIt - Local, privacy-focused voice-to-text."""
    pass


@main.command()
def start():
    """Start the SayIt daemon."""
    console.print("[green]✓[/green] Starting SayIt daemon...")
    console.print("[dim]  (not implemented yet)[/dim]")


@main.command()
def stop():
    """Stop the SayIt daemon."""
    console.print("[yellow]■[/yellow] Stopping SayIt daemon...")
    console.print("[dim]  (not implemented yet)[/dim]")


@main.command()
def status():
    """Check if SayIt daemon is running."""
    console.print("[blue]ℹ[/blue] Checking SayIt status...")
    console.print("[dim]  (not implemented yet)[/dim]")


@main.command()
def config():
    """Configure SayIt settings."""
    console.print("[cyan]⚙[/cyan] SayIt Configuration")
    console.print("[dim]  (not implemented yet)[/dim]")


if __name__ == "__main__":
    main()
