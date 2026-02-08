"""Tests for daemon process management."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from sayit.daemon import Daemon, PID_FILE


class TestDaemon:
    """Test Daemon class."""
    
    def test_is_running_no_pid_file(self, tmp_path):
        """Test is_running when no PID file exists."""
        pid_file = tmp_path / "sayit.pid"
        
        with patch("sayit.daemon.PID_FILE", pid_file):
            daemon = Daemon()
            running, pid = daemon.is_running()
            assert running is False
            assert pid is None
    
    def test_is_running_stale_pid(self, tmp_path):
        """Test is_running with stale PID file."""
        pid_file = tmp_path / "sayit.pid"
        pid_file.write_text("99999999")  # Non-existent PID
        
        with patch("sayit.daemon.PID_FILE", pid_file), \
             patch("sayit.daemon.PID_DIR", tmp_path):
            daemon = Daemon()
            running, pid = daemon.is_running()
            assert running is False
            assert pid is None
            # Stale PID file should be removed
            assert not pid_file.exists()
    
    def test_write_and_read_pid(self, tmp_path):
        """Test PID file write and read."""
        pid_file = tmp_path / "sayit.pid"
        
        with patch("sayit.daemon.PID_FILE", pid_file), \
             patch("sayit.daemon.PID_DIR", tmp_path):
            daemon = Daemon()
            daemon._write_pid(12345)
            assert pid_file.exists()
            assert daemon._read_pid() == 12345
    
    def test_remove_pid(self, tmp_path):
        """Test PID file removal."""
        pid_file = tmp_path / "sayit.pid"
        pid_file.write_text("12345")
        
        with patch("sayit.daemon.PID_FILE", pid_file):
            daemon = Daemon()
            daemon._remove_pid()
            assert not pid_file.exists()
    
    def test_status_returns_tuple(self, tmp_path):
        """Test status returns correct tuple format."""
        pid_file = tmp_path / "sayit.pid"
        
        with patch("sayit.daemon.PID_FILE", pid_file):
            daemon = Daemon()
            result = daemon.status()
            assert isinstance(result, tuple)
            assert len(result) == 2
