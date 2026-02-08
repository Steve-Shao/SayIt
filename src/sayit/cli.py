"""SayIt CLI entry point."""

import click
from rich.console import Console
from rich.table import Table

from sayit import __version__
from sayit.config import Config
from sayit.logging import setup_logging, get_logger

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="sayit")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose debug output")
@click.pass_context
def main(ctx, verbose):
    """SayIt - Local, privacy-focused voice-to-text."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    setup_logging(verbose=verbose)


@main.command()
@click.pass_context
def start(ctx):
    """Start the SayIt daemon."""
    logger = get_logger()
    logger.info("Starting SayIt daemon")
    logger.debug("Verbose mode enabled" if ctx.obj.get("verbose") else "Normal mode")
    
    console.print("[green]✓[/green] Starting SayIt daemon...")
    console.print("[dim]  (not implemented yet)[/dim]")


@main.command()
def stop():
    """Stop the SayIt daemon."""
    logger = get_logger()
    logger.info("Stopping SayIt daemon")
    
    console.print("[yellow]■[/yellow] Stopping SayIt daemon...")
    console.print("[dim]  (not implemented yet)[/dim]")


@main.command()
def status():
    """Check if SayIt daemon is running."""
    logger = get_logger()
    logger.debug("Checking daemon status")
    
    console.print("[blue]ℹ[/blue] Checking SayIt status...")
    console.print("[dim]  (not implemented yet)[/dim]")


@main.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Configure SayIt settings."""
    if ctx.invoked_subcommand is None:
        # No subcommand, show current config
        cfg = Config.load()
        
        table = Table(title="SayIt Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("hotkey", cfg.hotkey)
        table.add_row("engine", cfg.engine)
        table.add_row("model", cfg.model)
        table.add_row("language", cfg.language)
        table.add_row("sounds_enabled", str(cfg.sounds_enabled))
        table.add_row("min_recording_duration", str(cfg.min_recording_duration))
        
        console.print(table)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value."""
    cfg = Config.load()
    
    # Validate key exists
    if not hasattr(cfg, key):
        console.print(f"[red]✗[/red] Unknown setting: {key}")
        console.print(f"[dim]  Valid settings: hotkey, engine, model, language, sounds_enabled, min_recording_duration[/dim]")
        return
    
    # Convert value to appropriate type
    current_value = getattr(cfg, key)
    if isinstance(current_value, bool):
        value = value.lower() in ("true", "1", "yes", "on")
    elif isinstance(current_value, float):
        value = float(value)
    
    setattr(cfg, key, value)
    cfg.save()
    console.print(f"[green]✓[/green] Set {key} = {value}")


@config.command("reset")
def config_reset():
    """Reset configuration to defaults."""
    Config.reset()
    console.print("[green]✓[/green] Configuration reset to defaults")


if __name__ == "__main__":
    main()
