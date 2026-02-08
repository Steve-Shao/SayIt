"""Tests for hotkey listener.

Run manual test:
    python -m tests.test_hotkey

This will start a listener and print when keys are pressed/released.
Press Ctrl+C to stop.
"""

import pytest
from unittest.mock import MagicMock, patch

from sayit.hotkey import HotkeyListener, KEY_MAP


class TestHotkeyListener:
    """Unit tests for HotkeyListener."""
    
    def test_init_with_valid_key(self):
        """Test initialization with valid key names."""
        on_press = MagicMock()
        on_release = MagicMock()
        
        listener = HotkeyListener("ctrl", on_press, on_release)
        assert listener.key_name == "ctrl"
        assert listener._target_key == KEY_MAP["ctrl"]
    
    def test_init_with_fn_key(self):
        """Test initialization with fn key."""
        listener = HotkeyListener("fn", MagicMock(), MagicMock())
        assert listener.key_name == "fn"
        assert listener._target_key is None  # fn has special handling
    
    def test_init_with_uppercase_key(self):
        """Test that key names are case-insensitive."""
        listener = HotkeyListener("CTRL", MagicMock(), MagicMock())
        assert listener.key_name == "ctrl"
    
    def test_init_with_single_char(self):
        """Test initialization with single character key."""
        listener = HotkeyListener("a", MagicMock(), MagicMock())
        assert listener.key_name == "a"
        assert listener._target_key is not None
    
    def test_is_running_initially_false(self):
        """Test that listener is not running initially."""
        listener = HotkeyListener("ctrl", MagicMock(), MagicMock())
        assert not listener.is_running()
    
    def test_stop_when_not_running(self):
        """Test that stop() is safe when not running."""
        listener = HotkeyListener("ctrl", MagicMock(), MagicMock())
        listener.stop()  # Should not raise
    
    @patch('sayit.hotkey.keyboard.Listener')
    @patch('sayit.hotkey.platform.system', return_value='Linux')
    def test_start_creates_listener(self, mock_system, mock_listener_class):
        """Test that start() creates a keyboard listener."""
        mock_listener = MagicMock()
        mock_listener_class.return_value = mock_listener
        
        listener = HotkeyListener("ctrl", MagicMock(), MagicMock())
        result = listener.start()
        
        assert result is True
        mock_listener_class.assert_called_once()
        mock_listener.start.assert_called_once()
    
    @patch('sayit.hotkey.keyboard.Listener')
    @patch('sayit.hotkey.platform.system', return_value='Linux')
    def test_start_twice_returns_false(self, mock_system, mock_listener_class):
        """Test that starting twice returns False."""
        mock_listener = MagicMock()
        mock_listener_class.return_value = mock_listener
        
        listener = HotkeyListener("ctrl", MagicMock(), MagicMock())
        listener.start()
        result = listener.start()
        
        assert result is False
    
    def test_key_map_contains_expected_keys(self):
        """Test that KEY_MAP contains expected modifier keys."""
        expected_keys = ["fn", "ctrl", "alt", "cmd", "shift", "f1", "f12"]
        for key in expected_keys:
            assert key in KEY_MAP


# Manual test script
if __name__ == "__main__":
    import time
    from sayit.logging import setup_logging
    
    setup_logging(verbose=True)
    
    print("=" * 50)
    print("Hotkey Listener Manual Test")
    print("=" * 50)
    print()
    print("This test will listen for the RIGHT OPTION key.")
    print("(Using alt_r because fn key is hard to detect)")
    print()
    print("Press and hold RIGHT OPTION to test.")
    print("Press Ctrl+C to exit.")
    print()
    
    def on_press():
        print(">>> KEY PRESSED!")
    
    def on_release():
        print("<<< KEY RELEASED!")
    
    # Use alt_r (right option) for testing since fn is tricky
    listener = HotkeyListener("alt_r", on_press, on_release)
    
    if listener.start():
        print("Listener started. Waiting for key events...")
        print()
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print()
            print("Stopping...")
            listener.stop()
            print("Done.")
    else:
        print("Failed to start listener. Check accessibility permissions.")
