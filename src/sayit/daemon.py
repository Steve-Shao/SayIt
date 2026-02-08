"""SayIt daemon process management."""

import os
import signal
import sys
import time
from pathlib import Path

from sayit.logging import get_logger

PID_DIR = Path.home() / ".config" / "sayit"
PID_FILE = PID_DIR / "sayit.pid"


class Daemon:
    """Manages the SayIt background daemon process."""
    
    def __init__(self):
        self.logger = get_logger()
    
    def _read_pid(self) -> int | None:
        """Read PID from file. Returns None if not exists or invalid."""
        if not PID_FILE.exists():
            return None
        try:
            return int(PID_FILE.read_text().strip())
        except (ValueError, OSError):
            return None
    
    def _write_pid(self, pid: int) -> None:
        """Write PID to file."""
        PID_DIR.mkdir(parents=True, exist_ok=True)
        PID_FILE.write_text(str(pid))
    
    def _remove_pid(self) -> None:
        """Remove PID file."""
        if PID_FILE.exists():
            PID_FILE.unlink()
    
    def _is_process_running(self, pid: int) -> bool:
        """Check if a process with given PID is running."""
        try:
            os.kill(pid, 0)  # Signal 0 doesn't kill, just checks
            return True
        except OSError:
            return False
    
    def is_running(self) -> tuple[bool, int | None]:
        """Check if daemon is running.
        
        Returns:
            Tuple of (is_running, pid).
        """
        pid = self._read_pid()
        if pid is None:
            return False, None
        
        if self._is_process_running(pid):
            return True, pid
        
        # Stale PID file
        self._remove_pid()
        return False, None
    
    def start(self, run_func: callable) -> bool:
        """Start the daemon process.
        
        Args:
            run_func: The main function to run in the daemon.
        
        Returns:
            True if started successfully, False otherwise.
        """
        running, pid = self.is_running()
        if running:
            self.logger.warning(f"Daemon already running (PID: {pid})")
            return False
        
        # Fork the process
        try:
            pid = os.fork()
        except OSError as e:
            self.logger.error(f"Fork failed: {e}")
            return False
        
        if pid > 0:
            # Parent process - wait briefly and check if child started
            time.sleep(0.1)
            running, child_pid = self.is_running()
            if running:
                self.logger.info(f"Daemon started (PID: {child_pid})")
                return True
            else:
                self.logger.error("Daemon failed to start")
                return False
        
        # Child process
        try:
            # Create new session
            os.setsid()
            
            # Second fork to prevent zombie processes
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
            
            # Write PID file
            self._write_pid(os.getpid())
            
            # Setup signal handlers
            signal.signal(signal.SIGTERM, self._signal_handler)
            signal.signal(signal.SIGINT, self._signal_handler)
            
            # Run the main function
            run_func()
            
        except Exception as e:
            self.logger.error(f"Daemon error: {e}")
            self._remove_pid()
            sys.exit(1)
        finally:
            self._remove_pid()
            sys.exit(0)
    
    def _signal_handler(self, signum, frame):
        """Handle termination signals."""
        self.logger.info(f"Received signal {signum}, shutting down")
        self._remove_pid()
        sys.exit(0)
    
    def stop(self) -> bool:
        """Stop the daemon process.
        
        Returns:
            True if stopped successfully, False otherwise.
        """
        running, pid = self.is_running()
        if not running:
            self.logger.info("Daemon is not running")
            return True
        
        try:
            os.kill(pid, signal.SIGTERM)
            
            # Wait for process to terminate
            for _ in range(50):  # 5 seconds max
                time.sleep(0.1)
                if not self._is_process_running(pid):
                    self._remove_pid()
                    self.logger.info("Daemon stopped")
                    return True
            
            # Force kill if still running
            os.kill(pid, signal.SIGKILL)
            self._remove_pid()
            self.logger.warning("Daemon force killed")
            return True
            
        except OSError as e:
            self.logger.error(f"Failed to stop daemon: {e}")
            return False
    
    def status(self) -> tuple[bool, int | None]:
        """Get daemon status.
        
        Returns:
            Tuple of (is_running, pid).
        """
        return self.is_running()
