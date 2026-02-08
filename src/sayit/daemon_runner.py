"""SayIt daemon runner - standalone entry point for background process.

This module is invoked via `python -m sayit.daemon_runner` to avoid
fork issues with tkinter on macOS.
"""

import os
import signal
import sys
from pathlib import Path

from sayit.core import SayItCore
from sayit.logging import setup_logging, get_logger


PID_DIR = Path.home() / ".config" / "sayit"
PID_FILE = PID_DIR / "sayit.pid"


def write_pid() -> None:
    """Write current process PID to file."""
    PID_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))


def remove_pid() -> None:
    """Remove PID file."""
    if PID_FILE.exists():
        PID_FILE.unlink()


def main() -> None:
    """Run the daemon process."""
    setup_logging()
    logger = get_logger()
    
    # Write PID file
    write_pid()
    logger.info(f"Daemon started (PID: {os.getpid()})")
    
    # Create and store core instance for signal handler
    core = SayItCore()
    
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        core.stop()
        remove_pid()
        sys.exit(0)
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        core.run()
    except Exception as e:
        logger.error(f"Daemon error: {e}")
        raise
    finally:
        remove_pid()


if __name__ == "__main__":
    main()
