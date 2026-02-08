"""Text injection for inserting transcribed text at cursor position."""

import logging
import subprocess

logger = logging.getLogger(__name__)


class TextInjector:
    """Injects text at the current cursor position.
    
    On macOS, uses AppleScript via osascript to simulate keyboard input.
    Falls back to clipboard if text injection fails.
    """

    def __init__(self):
        self._last_error: str | None = None

    def inject(self, text: str) -> bool:
        """Type text at current cursor position.
        
        Args:
            text: Text to inject.
            
        Returns:
            True if injection succeeded, False if fell back to clipboard.
        """
        if not text:
            logger.debug("Empty text, nothing to inject")
            return True

        # Try keyboard simulation first
        if self._inject_via_keystroke(text):
            logger.debug(f"Injected {len(text)} chars via keystroke")
            return True

        # Fallback to clipboard
        logger.warning("Keystroke injection failed, falling back to clipboard")
        self._copy_to_clipboard(text)
        return False

    def _inject_via_keystroke(self, text: str) -> bool:
        """Inject text using AppleScript keystroke.
        
        Args:
            text: Text to type.
            
        Returns:
            True if successful.
        """
        # Escape special characters for AppleScript
        escaped = self._escape_for_applescript(text)
        
        # AppleScript to type text
        script = f'tell application "System Events" to keystroke "{escaped}"'
        
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                self._last_error = result.stderr.strip()
                logger.error(f"osascript failed: {self._last_error}")
                return False
            return True
        except subprocess.TimeoutExpired:
            self._last_error = "osascript timeout"
            logger.error(self._last_error)
            return False
        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Injection error: {e}")
            return False

    def _escape_for_applescript(self, text: str) -> str:
        """Escape text for use in AppleScript string.
        
        Args:
            text: Raw text.
            
        Returns:
            Escaped text safe for AppleScript.
        """
        # Escape backslashes first, then quotes
        escaped = text.replace("\\", "\\\\")
        escaped = escaped.replace('"', '\\"')
        return escaped

    def _copy_to_clipboard(self, text: str) -> None:
        """Copy text to system clipboard.
        
        Args:
            text: Text to copy.
        """
        try:
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE,
            )
            process.communicate(input=text.encode("utf-8"))
            logger.info("Text copied to clipboard")
        except Exception as e:
            logger.error(f"Clipboard copy failed: {e}")

    def check_accessibility(self) -> bool:
        """Check if accessibility permissions are granted.
        
        Returns:
            True if permissions appear to be granted.
        """
        # Try a simple keystroke test
        script = 'tell application "System Events" to keystroke ""'
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=2,
            )
            return result.returncode == 0
        except Exception:
            return False

    @property
    def last_error(self) -> str | None:
        """Return the last error message, if any."""
        return self._last_error
