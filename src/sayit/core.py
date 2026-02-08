"""SayIt core event loop with tkinter mainloop and hotkey integration."""

import queue
import signal
import sys
import threading
import tkinter as tk
from typing import Optional

from sayit.config import Config
from sayit.engines.base import get_engine, TranscriptionEngine
from sayit.hotkey import HotkeyListener
from sayit.indicator import StatusIndicator
from sayit.injector import TextInjector
from sayit.logging import get_logger
from sayit.recorder import AudioRecorder
from sayit.sounds import SoundPlayer


class SayItCore:
    """Core application managing hotkey, recording, and feedback.
    
    Threading model:
    - Main thread: tkinter mainloop (required for GUI on macOS)
    - Background thread: hotkey listener (pynput)
    - Communication: thread-safe queue + tkinter after() polling
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
        self._indicator: Optional[StatusIndicator] = None
        self._engine: Optional[TranscriptionEngine] = None
        self._injector: Optional[TextInjector] = None
        
        # Thread-safe event queue
        self._event_queue: queue.Queue = queue.Queue()
        
        # State
        self._running = False
        self._transcribing = False
        self._last_audio_path: Optional[str] = None
    
    def _setup_components(self) -> None:
        """Initialize all components."""
        # Hidden tkinter root window
        self._root = tk.Tk()
        self._root.withdraw()  # Hide the window
        
        # Prevent Dock icon on macOS
        try:
            self._root.tk.call('::tk::unsupported::MacWindowStyle', 'style', 
                              self._root._w, 'plain', 'none')
        except tk.TclError:
            pass  # Not on macOS or unsupported
        
        # Audio recorder
        self._recorder = AudioRecorder(
            min_duration=self.config.min_recording_duration
        )
        
        # Sound player
        self._sounds = SoundPlayer(enabled=self.config.sounds_enabled)
        
        # Status indicator
        self._indicator = StatusIndicator(self._root)
        
        # Transcription engine
        try:
            self._engine = get_engine(self.config.engine)
            self._engine.load_model(self.config.model)
            self.logger.info(f"Engine loaded: {self.config.engine}")
        except Exception as e:
            self.logger.error(f"Failed to load engine: {e}")
            self._engine = None
        
        # Text injector
        self._injector = TextInjector()
        
        # Hotkey listener with callbacks
        self._hotkey = HotkeyListener(
            key=self.config.hotkey,
            on_press=self._on_hotkey_press,
            on_release=self._on_hotkey_release,
        )
    
    def _on_hotkey_press(self) -> None:
        """Handle hotkey press event (called from background thread)."""
        self.logger.debug("Hotkey press callback triggered")
        self._event_queue.put("press")
    
    def _on_hotkey_release(self) -> None:
        """Handle hotkey release event (called from background thread)."""
        self.logger.debug("Hotkey release callback triggered")
        self._event_queue.put("release")
    
    def _process_events(self) -> None:
        """Process events from queue (runs on main thread)."""
        try:
            while True:
                event = self._event_queue.get_nowait()
                if event == "press":
                    self._start_recording()
                elif event == "release":
                    self._stop_recording()
                elif isinstance(event, tuple):
                    event_type, data = event
                    if event_type == "inject":
                        self._inject_text(data)
                    elif event_type == "done":
                        if self._indicator:
                            self._indicator.hide()
                    elif event_type == "error":
                        self.logger.error(f"Event error: {data}")
                        if self._indicator:
                            self._indicator.hide()
        except queue.Empty:
            pass
        
        # Schedule next check
        if self._running and self._root:
            self._root.after(10, self._process_events)
    
    def _start_recording(self) -> None:
        """Start recording (runs on main thread)."""
        if self._recorder is None or self._sounds is None:
            self.logger.warning("Recorder or sounds not initialized")
            return
        
        self.logger.info("Recording started")
        self._sounds.play_start()
        self._recorder.start_recording()
        
        # Show indicator
        if self._indicator:
            self._indicator.show()
    
    def _stop_recording(self) -> None:
        """Stop recording and process audio (runs on main thread)."""
        if self._recorder is None or self._sounds is None:
            self.logger.warning("Recorder or sounds not initialized")
            return
        
        audio_path = self._recorder.stop_recording()
        self._sounds.play_stop()
        
        if audio_path:
            self._last_audio_path = audio_path
            self.logger.info(f"Recording saved: {audio_path}")
            # Start transcription in background thread
            self._transcribe_and_inject(audio_path)
        else:
            self.logger.info("Recording discarded (too short)")
            # Hide indicator since no transcription needed
            if self._indicator:
                self._indicator.hide()
    
    def _transcribe_and_inject(self, audio_path: str) -> None:
        """Transcribe audio and inject text (runs transcription in background)."""
        if self._engine is None:
            self.logger.error("No transcription engine available")
            if self._indicator:
                self._indicator.hide()
            return
        
        if self._transcribing:
            self.logger.warning("Already transcribing, skipping")
            return
        
        self._transcribing = True
        
        # Update indicator to show processing state
        if self._indicator:
            self._indicator.set_processing()
        
        def transcribe_task():
            try:
                self.logger.debug(f"Transcribing: {audio_path}")
                text = self._engine.transcribe(audio_path, language=self.config.language)
                text = text.strip()
                
                if text:
                    self.logger.info(f"Transcribed: {text[:50]}..." if len(text) > 50 else f"Transcribed: {text}")
                    # Schedule injection on main thread
                    self._event_queue.put(("inject", text))
                else:
                    self.logger.info("Transcription returned empty text")
                    self._event_queue.put(("done", None))
            except Exception as e:
                self.logger.error(f"Transcription failed: {e}")
                self._event_queue.put(("error", str(e)))
            finally:
                self._transcribing = False
        
        # Run transcription in background thread
        thread = threading.Thread(target=transcribe_task, daemon=True)
        thread.start()
    
    def _inject_text(self, text: str) -> None:
        """Inject transcribed text at cursor (runs on main thread)."""
        self.logger.debug(f"_inject_text called with: {text[:30]}...")
        
        if self._injector is None:
            self.logger.error("Text injector not available")
            return
        
        success = self._injector.inject(text)
        if success:
            self.logger.info("Text injected successfully")
        else:
            self.logger.warning(f"Text injection failed: {self._injector.last_error}")
        
        # Hide indicator after injection
        if self._indicator:
            self._indicator.hide()
    
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
        
        # Start event processing loop
        if self._root:
            self._root.after(10, self._process_events)
        
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
        
        if self._indicator:
            self._indicator.destroy()
            self._indicator = None
        
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
