"""Tests for hotkey listener.

Run manual test:
    python -m tests.test_hotkey

This will start a listener and print when keys are pressed/released.
Press Ctrl+C to stop.
"""

import pytest
from unittest.mock import MagicMock, patch

from sayit.hotkey import HotkeyListener, SUPPORTED_KEYS


class TestHotkeyListener:
    """Unit tests for HotkeyListener."""
    
    def test_init_with_valid_key(self):
        """Test initialization with valid key names."""
        on_press = MagicMock()
        on_release = MagicMock()
        
        listener = HotkeyListener("alt_r", on_press, on_release)
        assert listener.key_name == "alt_r"
        assert listener._target_key == SUPPORTED_KEYS["alt_r"]
    
    def test_init_with_uppercase_key(self):
        """Test that key names are case-insensitive."""
        listener = HotkeyListener("ALT_R", MagicMock(), MagicMock())
        assert listener.key_name == "alt_r"
    
    def test_is_running_initially_false(self):
        """Test that listener is not running initially."""
        listener = HotkeyListener("alt_r", MagicMock(), MagicMock())
        assert not listener.is_running()
    
    def test_stop_when_not_running(self):
        """Test that stop() is safe when not running."""
        listener = HotkeyListener("alt_r", MagicMock(), MagicMock())
        listener.stop()  # Should not raise
    
    @patch('sayit.hotkey.keyboard.Listener')
    @patch('sayit.hotkey.platform.system', return_value='Linux')
    def test_start_creates_listener(self, mock_system, mock_listener_class):
        """Test that start() creates a keyboard listener."""
        mock_listener = MagicMock()
        mock_listener_class.return_value = mock_listener
        
        listener = HotkeyListener("alt_r", MagicMock(), MagicMock())
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
        
        listener = HotkeyListener("alt_r", MagicMock(), MagicMock())
        listener.start()
        result = listener.start()
        
        assert result is False
    
    def test_is_valid_key(self):
        """Test is_valid_key static method."""
        assert HotkeyListener.is_valid_key("alt_r") is True
        assert HotkeyListener.is_valid_key("ALT_R") is True  # Case insensitive
        assert HotkeyListener.is_valid_key("ctrl_l") is True
        assert HotkeyListener.is_valid_key("f1") is True
        assert HotkeyListener.is_valid_key("fn") is False
        assert HotkeyListener.is_valid_key("invalid") is False
    
    def test_get_supported_keys(self):
        """Test get_supported_keys static method."""
        keys = HotkeyListener.get_supported_keys()
        assert "alt_r" in keys
        assert "alt_l" in keys
        assert "ctrl_r" in keys
        assert "f1" in keys
        assert "f12" in keys
        assert "fn" not in keys
    
    def test_supported_keys_matches_spec(self):
        """Test that SUPPORTED_KEYS matches the spec."""
        expected_keys = [
            "alt_r", "alt_l", "ctrl_r", "ctrl_l", "cmd_r", "cmd_l",
            "shift_r", "shift_l", "f1", "f2", "f3", "f4", "f5", "f6",
            "f7", "f8", "f9", "f10", "f11", "f12",
        ]
        for key in expected_keys:
            assert key in SUPPORTED_KEYS, f"Missing key: {key}"
        
        # Ensure no extra keys
        assert len(SUPPORTED_KEYS) == len(expected_keys)


# Manual test script
if __name__ == "__main__":
    import time
    from sayit.logging import setup_logging
    
    setup_logging(verbose=True)
    
    print("=" * 50)
    print("Hotkey Listener Manual Test")
    print("=" * 50)
    print()
    print("This test will listen for the RIGHT OPTION key (alt_r).")
    print()
    print("Press and hold RIGHT OPTION to test.")
    print("Press Ctrl+C to exit.")
    print()
    
    def on_press():
        print(">>> KEY PRESSED!")
    
    def on_release():
        print("<<< KEY RELEASED!")
    
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
