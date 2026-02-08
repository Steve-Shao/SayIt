"""SayIt core event loop with tkinter mainloop and hotkey integration."""

import signal
import sys
import tkinter as tk
from typing import Optional

from sayit.config import Config
from sayit.hotkey import HotkeyListener
from sayit.logging import get_logger
from sayit.recorder import AudioRecorder
from sayit.sounds import SoundPlayer


class SayItCore:
    """Core application managing hotkey, recording, and feedback.
    
    Threading model:
    - Main thread: tkinter mainloop (required for GUI on macOS)
    - Background thread: hotkey listener (pynput)
    - Communication: root.after() for thread-safe GUI updates
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the core application.
        
        Args:
            config: Configuration object. Loads from file if not provided.
        """
        self.config = config or Config.load()
        self.logger = get_logger()
        
        # Components
        self._root: Optional[tk.Tk] = None
        self._hotkey: Optional[HotkeyListener] = None
        self._recorder: Optional[AudioRecorder] = None
        self._sounds: Optional[SoundPlayer] = None
        
        # State
        self._running = False
        self._last_audio_path: Optional[str] = None
    
    def _setup_components(self) -> None:
        """Initialize all components."""
        # Hidden tkinter root window
        self._root = tk.Tk()
        self._root.withdraw()  # Hide the window
        
        # Audio recorder
        self._recorder = AudioRecorder(
            min_duration=self.config.min_recording_duration
        )
        
        # Sound player
        self._sounds = SoundPlayer(enabled=self.config.sounds_enabled)
        
        # Hotkey listener with callbacks
        self._hotkey = HotkeyListener(
            key=self.config.hotkey,
            on_press=self._on_hotkey_press,
            on_release=self._on_hotkey_release,
        )
    
    def _on_hotkey_press(self) -> None:
        """Handle hotkey press event (called from background thread)."""
        if self._root is None:
            return
        # Schedule on main thread
        self._root.after(0, self._start_recording)
    
    def _on_hotkey_release(self) -> None:
        """Handle hotkey release event (called from background thread)."""
        if self._root is None:
            return
        # Schedule on main thread
        self._root.after(0, self._stop_recording)
    
    def _start_recording(self) -> None:
        """Start recording (runs on main thread)."""
        if self._recorder is None or self._sounds is None:
            return
        
        self.logger.info("Recording started")
        self._sounds.play_start()
        self._recorder.start_recording()
    
    def _stop_recording(self) -> None:
        """Stop recording and process audio (runs on main thread)."""
        if self._recorder is None or self._sounds is None:
            return
        
        audio_path = self._recorder.stop_recording()
        self._sounds.play_stop()
        
        if audio_path:
            self._last_audio_path = audio_path
            self.logger.info(f"Recording saved: {audio_path}")
            # TODO: Phase 3 will add transcription here
        else:
            self.logger.info("Recording discarded (too short)")
    
    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def handle_signal(signum, frame):
            self.logger.info(f"Received signal {signum}, shutting down...")
            self.stop()
        
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)
    
    def run(self) -> None:
        """Run the main event loop.
        
        This method blocks until stop() is called or a signal is received.
        """
        if self._running:
            self.logger.warning("Already running")
            return
        
        self._running = True
        self._setup_components()
        self._setup_signal_handlers()
        
        # Start hotkey listener in background thread
        if self._hotkey and not self._hotkey.start():
            self.logger.error("Failed to start hotkey listener")
            self._running = False
            return
        
        self.logger.info(
            f"SayIt started (hotkey: {self.config.hotkey}, "
            f"sounds: {'on' if self.config.sounds_enabled else 'off'})"
        )
        
        # Run tkinter mainloop on main thread
        try:
            if self._root:
                self._root.mainloop()
        except KeyboardInterrupt:
            pass
        finally:
            self._cleanup()
    
    def stop(self) -> None:
        """Stop the event loop and cleanup."""
        if not self._running:
            return
        
        self._running = False
        
        # Quit tkinter mainloop
        if self._root:
            self._root.quit()
    
    def _cleanup(self) -> None:
        """Cleanup all components."""
        self.logger.debug("Cleaning up...")
        
        if self._hotkey:
            self._hotkey.stop()
            self._hotkey = None
        
        if self._root:
            try:
                self._root.destroy()
            except tk.TclError:
                pass  # Already destroyed
            self._root = None
        
        self._recorder = None
        self._sounds = None
        self._running = False
        
        self.logger.info("SayIt stopped")
