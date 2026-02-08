"""SayIt audio recorder for microphone capture."""

import platform
import subprocess
import tempfile
import threading
import wave
from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd

from sayit.logging import get_logger


class AudioRecorder:
    """Records audio from the default microphone."""
    
    def __init__(self, sample_rate: int = 16000, min_duration: float = 0.3):
        """Initialize the audio recorder.
        
        Args:
            sample_rate: Audio sample rate in Hz. Default 16kHz for Whisper.
            min_duration: Minimum recording duration in seconds. Shorter recordings are discarded.
        """
        self.sample_rate = sample_rate
        self.min_duration = min_duration
        self.logger = get_logger()
        
        self._buffer: list[np.ndarray] = []
        self._stream: Optional[sd.InputStream] = None
        self._is_recording = False
        self._lock = threading.Lock()
    
    def _audio_callback(
        self,
        indata: np.ndarray,
        frames: int,
        time_info: dict,
        status: sd.CallbackFlags,
    ) -> None:
        """Callback for audio stream. Appends audio data to buffer."""
        if status:
            self.logger.warning(f"Audio callback status: {status}")
        
        with self._lock:
            if self._is_recording:
                self._buffer.append(indata.copy())
    
    def start_recording(self) -> bool:
        """Begin capturing audio from the default microphone.
        
        Returns:
            True if recording started successfully, False otherwise.
        """
        if self._is_recording:
            self.logger.warning("Already recording")
            return False
        
        # Check microphone availability
        if not self._check_microphone():
            return False
        
        try:
            with self._lock:
                self._buffer = []
                self._is_recording = True
            
            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.float32,
                callback=self._audio_callback,
            )
            self._stream.start()
            self.logger.debug("Recording started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
            self._is_recording = False
            return False
    
    def stop_recording(self) -> Optional[str]:
        """Stop recording and save audio to a WAV file.
        
        Returns:
            Path to the saved WAV file, or None if recording was too short or failed.
        """
        if not self._is_recording:
            self.logger.warning("Not recording")
            return None
        
        try:
            # Stop the stream
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None
            
            with self._lock:
                self._is_recording = False
                buffer_copy = self._buffer.copy()
                self._buffer = []
            
            if not buffer_copy:
                self.logger.warning("No audio data captured")
                return None
            
            # Concatenate all audio chunks
            audio_data = np.concatenate(buffer_copy, axis=0)
            duration = len(audio_data) / self.sample_rate
            
            self.logger.debug(f"Recording stopped, duration: {duration:.2f}s")
            
            # Check minimum duration
            if duration < self.min_duration:
                self.logger.info(f"Recording too short ({duration:.2f}s < {self.min_duration}s), discarding")
                return None
            
            # Save to temp WAV file
            return self._save_wav(audio_data)
        except Exception as e:
            self.logger.error(f"Failed to stop recording: {e}")
            return None
    
    def _save_wav(self, audio_data: np.ndarray) -> str:
        """Save audio data to a temporary WAV file.
        
        Args:
            audio_data: Audio samples as float32 numpy array.
            
        Returns:
            Path to the saved WAV file.
        """
        # Create temp file
        fd, path = tempfile.mkstemp(suffix=".wav", prefix="sayit_")
        
        # Convert float32 to int16
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Write WAV file
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_int16.tobytes())
        
        self.logger.debug(f"Saved recording to {path}")
        return path
    
    def is_recording(self) -> bool:
        """Check if currently recording."""
        return self._is_recording
    
    def _check_microphone(self) -> bool:
        """Check if a microphone is available.
        
        Returns:
            True if microphone is available, False otherwise.
        """
        try:
            devices = sd.query_devices()
            default_input = sd.query_devices(kind="input")
            if default_input is None:
                self._show_microphone_error()
                return False
            self.logger.debug(f"Using microphone: {default_input['name']}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to query audio devices: {e}")
            self._show_microphone_error()
            return False
    
    def _show_microphone_error(self) -> None:
        """Show error message when no microphone is available."""
        self.logger.error(
            "No microphone available.\n"
            "Please check:\n"
            "  1. A microphone is connected\n"
            "  2. Microphone permission is granted in System Preferences → Privacy & Security → Microphone"
        )
