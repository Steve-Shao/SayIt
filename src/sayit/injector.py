"""Text injection for inserting transcribed text at cursor position."""

import logging
import subprocess

logger = logging.getLogger(__name__)


class TextInjector:
    """Injects text at the current cursor position.
    
    On macOS, uses clipboard + Cmd+V paste for reliable Unicode support.
    """

    def __init__(self):
        self._last_error: str | None = None

    def inject(self, text: str) -> bool:
        """Inject text at current cursor position via clipboard + paste.
        
        Args:
            text: Text to inject.
            
        Returns:
            True if injection succeeded, False otherwise.
        """
        if not text:
            logger.debug("Empty text, nothing to inject")
            return True

        # Copy to clipboard
        if not self._copy_to_clipboard(text):
            return False

        # Paste via Cmd+V
        if not self._paste():
            logger.warning("Paste failed, text remains in clipboard")
            return False

        logger.debug(f"Injected {len(text)} chars via clipboard+paste")
        return True

    def _copy_to_clipboard(self, text: str) -> bool:
        """Copy text to system clipboard.
        
        Args:
            text: Text to copy.
            
        Returns:
            True if successful.
        """
        try:
            process = subprocess.Popen(
                ["pbcopy"],
                stdin=subprocess.PIPE,
            )
            process.communicate(input=text.encode("utf-8"))
            if process.returncode != 0:
                self._last_error = "pbcopy failed"
                logger.error(self._last_error)
                return False
            return True
        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Clipboard copy failed: {e}")
            return False

    def _paste(self) -> bool:
        """Simulate Cmd+V paste.
        
        Returns:
            True if successful.
        """
        script = 'tell application "System Events" to keystroke "v" using command down'
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode != 0:
                self._last_error = result.stderr.strip()
                logger.error(f"Paste failed: {self._last_error}")
                return False
            return True
        except subprocess.TimeoutExpired:
            self._last_error = "osascript timeout"
            logger.error(self._last_error)
            return False
        except Exception as e:
            self._last_error = str(e)
            logger.error(f"Paste error: {e}")
            return False

    def check_accessibility(self) -> bool:
        """Check if accessibility permissions are granted.
        
        Returns:
            True if permissions appear to be granted.
        """
        script = 'tell application "System Events" to keystroke "v" using command down'
        try:
            # Just check if osascript can run without error
            # Note: This doesn't actually paste since we're just checking
            result = subprocess.run(
                ["osascript", "-e", 'tell application "System Events" to key code 9'],
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
