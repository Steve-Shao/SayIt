"""SayIt hotkey listener for global keyboard events."""

import platform
import subprocess
import threading
from typing import Callable, Optional

from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from sayit.logging import get_logger


# Key name mapping for configuration
KEY_MAP = {
    "fn": None,  # Special handling for Fn key
    "ctrl": Key.ctrl,
    "ctrl_l": Key.ctrl_l,
    "ctrl_r": Key.ctrl_r,
    "alt": Key.alt,
    "alt_l": Key.alt_l,
    "alt_r": Key.alt_r,
    "option": Key.alt,  # macOS alias
    "cmd": Key.cmd,
    "cmd_l": Key.cmd_l,
    "cmd_r": Key.cmd_r,
    "command": Key.cmd,  # macOS alias
    "shift": Key.shift,
    "shift_l": Key.shift_l,
    "shift_r": Key.shift_r,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
}


class HotkeyListener:
    """Listens for global hotkey press/release events."""
    
    def __init__(
        self,
        key: str,
        on_press: Callable[[], None],
        on_release: Callable[[], None],
    ):
        """Initialize the hotkey listener.
        
        Args:
            key: Key name (e.g., "fn", "ctrl", "f5").
            on_press: Callback when key is pressed.
            on_release: Callback when key is released.
        """
        self.key_name = key.lower()
        self.on_press_callback = on_press
        self.on_release_callback = on_release
        self.logger = get_logger()
        
        self._listener: Optional[keyboard.Listener] = None
        self._is_pressed = False
        self._target_key = self._resolve_key(self.key_name)
    
    def _resolve_key(self, key_name: str) -> Optional[Key | KeyCode]:
        """Resolve key name to pynput Key object."""
        if key_name in KEY_MAP:
            return KEY_MAP[key_name]
        
        # Single character key
        if len(key_name) == 1:
            return KeyCode.from_char(key_name)
        
        self.logger.warning(f"Unknown key: {key_name}, defaulting to 'fn'")
        return None
    
    def _on_press(self, key: Key | KeyCode | None) -> None:
        """Handle key press event."""
        if self._is_pressed:
            return  # Ignore key repeat
        
        if self._matches_key(key):
            self._is_pressed = True
            self.logger.debug(f"Hotkey pressed: {self.key_name}")
            try:
                self.on_press_callback()
            except Exception as e:
                self.logger.error(f"Error in on_press callback: {e}")
    
    def _on_release(self, key: Key | KeyCode | None) -> None:
        """Handle key release event."""
        if not self._is_pressed:
            return
        
        if self._matches_key(key):
            self._is_pressed = False
            self.logger.debug(f"Hotkey released: {self.key_name}")
            try:
                self.on_release_callback()
            except Exception as e:
                self.logger.error(f"Error in on_release callback: {e}")
    
    def _matches_key(self, key: Key | KeyCode | None) -> bool:
        """Check if the pressed key matches our target key."""
        if self._target_key is None:
            # Fn key: pynput doesn't detect it directly on macOS
            # We use a workaround: check for Key.fn if available
            return hasattr(Key, 'fn') and key == Key.fn
        
        return key == self._target_key
    
    def start(self) -> bool:
        """Start listening for hotkey events.
        
        Returns:
            True if started successfully, False otherwise.
        """
        if self._listener is not None:
            self.logger.warning("Listener already running")
            return False
        
        # Check accessibility permissions on macOS
        if platform.system() == "Darwin" and not self._check_accessibility():
            return False
        
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release,
        )
        self._listener.start()
        self.logger.info(f"Hotkey listener started (key: {self.key_name})")
        return True
    
    def stop(self) -> None:
        """Stop listening for hotkey events."""
        if self._listener is not None:
            self._listener.stop()
            self._listener = None
            self._is_pressed = False
            self.logger.info("Hotkey listener stopped")
    
    def is_running(self) -> bool:
        """Check if listener is running."""
        return self._listener is not None and self._listener.is_alive()
    
    def _check_accessibility(self) -> bool:
        """Check if accessibility permissions are granted on macOS.
        
        Returns:
            True if permissions are granted or not on macOS.
        """
        if platform.system() != "Darwin":
            return True
        
        # Try to create a test listener to check permissions
        # If it fails, pynput will raise an exception
        try:
            # Use AppleScript to check accessibility status
            script = '''
            tell application "System Events"
                return true
            end tell
            '''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                timeout=5,
            )
            if result.returncode != 0:
                self._show_accessibility_instructions()
                return False
            return True
        except subprocess.TimeoutExpired:
            self._show_accessibility_instructions()
            return False
        except Exception as e:
            self.logger.debug(f"Accessibility check error: {e}")
            # Assume permissions are OK, let pynput handle it
            return True
    
    def _show_accessibility_instructions(self) -> None:
        """Show instructions for granting accessibility permissions."""
        self.logger.error(
            "Accessibility permission required for global hotkey detection.\n"
            "Please grant permission:\n"
            "  1. Open System Preferences → Privacy & Security → Accessibility\n"
            "  2. Click the lock to make changes\n"
            "  3. Add and enable your terminal app (Terminal, iTerm, etc.)\n"
            "  4. Restart SayIt"
        )
