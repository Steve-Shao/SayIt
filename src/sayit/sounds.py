"""SayIt sound player for audio feedback."""

import subprocess
import threading
from pathlib import Path


class SoundPlayer:
    """Plays audio feedback for recording state transitions.
    
    Uses macOS afplay command with system sounds.
    Sounds play asynchronously to avoid blocking.
    """
    
    # macOS system sound paths
    SOUND_START = "/System/Library/Sounds/Tink.aiff"
    SOUND_STOP = "/System/Library/Sounds/Pop.aiff"
    
    def __init__(self, enabled: bool = True):
        """Initialize sound player.
        
        Args:
            enabled: Whether sounds are enabled.
        """
        self._enabled = enabled
    
    @property
    def enabled(self) -> bool:
        """Whether sounds are enabled."""
        return self._enabled
    
    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Set whether sounds are enabled."""
        self._enabled = value
    
    def _play_async(self, sound_path: str) -> None:
        """Play sound asynchronously using afplay.
        
        Args:
            sound_path: Path to the sound file.
        """
        if not self._enabled:
            return
        
        if not Path(sound_path).exists():
            return
        
        def play():
            try:
                subprocess.run(
                    ["afplay", sound_path],
                    capture_output=True,
                    check=False
                )
            except FileNotFoundError:
                # afplay not available (non-macOS)
                pass
        
        thread = threading.Thread(target=play, daemon=True)
        thread.start()
    
    def play_start(self) -> None:
        """Play recording start sound."""
        self._play_async(self.SOUND_START)
    
    def play_stop(self) -> None:
        """Play recording stop sound."""
        self._play_async(self.SOUND_STOP)
