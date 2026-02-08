"""Tests for the AudioRecorder class."""

import os
import tempfile
import time
import wave
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from sayit.recorder import AudioRecorder


class TestAudioRecorder:
    """Unit tests for AudioRecorder."""
    
    def test_init_default_values(self):
        """Test default initialization values."""
        recorder = AudioRecorder()
        assert recorder.sample_rate == 16000
        assert recorder.min_duration == 0.3
        assert not recorder.is_recording()
    
    def test_init_custom_values(self):
        """Test custom initialization values."""
        recorder = AudioRecorder(sample_rate=44100, min_duration=0.5)
        assert recorder.sample_rate == 44100
        assert recorder.min_duration == 0.5
    
    def test_is_recording_initially_false(self):
        """Test that is_recording returns False initially."""
        recorder = AudioRecorder()
        assert not recorder.is_recording()
    
    def test_stop_recording_when_not_recording(self):
        """Test stop_recording returns None when not recording."""
        recorder = AudioRecorder()
        result = recorder.stop_recording()
        assert result is None
    
    @patch('sayit.recorder.sd.query_devices')
    def test_check_microphone_no_device(self, mock_query):
        """Test microphone check when no device available."""
        mock_query.side_effect = Exception("No device")
        recorder = AudioRecorder()
        assert not recorder._check_microphone()
    
    @patch('sayit.recorder.sd.query_devices')
    def test_check_microphone_with_device(self, mock_query):
        """Test microphone check when device is available."""
        mock_query.return_value = [{"name": "Test Mic", "max_input_channels": 1}]
        with patch('sayit.recorder.sd.query_devices', return_value={"name": "Test Mic"}):
            recorder = AudioRecorder()
            assert recorder._check_microphone()
    
    def test_save_wav_creates_file(self):
        """Test that _save_wav creates a valid WAV file."""
        recorder = AudioRecorder()
        
        # Create test audio data (1 second of silence)
        audio_data = np.zeros(16000, dtype=np.float32)
        
        path = recorder._save_wav(audio_data)
        
        try:
            assert os.path.exists(path)
            assert path.endswith(".wav")
            
            # Verify WAV file properties
            with wave.open(path, "rb") as wf:
                assert wf.getnchannels() == 1
                assert wf.getsampwidth() == 2  # 16-bit
                assert wf.getframerate() == 16000
                assert wf.getnframes() == 16000
        finally:
            os.unlink(path)
    
    def test_save_wav_audio_content(self):
        """Test that _save_wav preserves audio content."""
        recorder = AudioRecorder()
        
        # Create test audio data (sine wave)
        t = np.linspace(0, 1, 16000, dtype=np.float32)
        audio_data = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
        
        path = recorder._save_wav(audio_data)
        
        try:
            with wave.open(path, "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                loaded_data = np.frombuffer(frames, dtype=np.int16)
                
                # Convert back to float and check correlation
                loaded_float = loaded_data.astype(np.float32) / 32767
                correlation = np.corrcoef(audio_data, loaded_float)[0, 1]
                assert correlation > 0.99  # High correlation
        finally:
            os.unlink(path)


class TestAudioRecorderIntegration:
    """Integration tests that require actual audio hardware.
    
    These tests are marked with pytest.mark.hardware and skipped by default.
    Run with: pytest -m hardware
    """
    
    @pytest.mark.hardware
    def test_start_and_stop_recording(self):
        """Test actual recording start and stop."""
        recorder = AudioRecorder(min_duration=0.1)
        
        assert recorder.start_recording()
        assert recorder.is_recording()
        
        # Record for a short time
        time.sleep(0.5)
        
        path = recorder.stop_recording()
        assert not recorder.is_recording()
        
        if path:
            assert os.path.exists(path)
            os.unlink(path)
    
    @pytest.mark.hardware
    def test_short_recording_discarded(self):
        """Test that recordings shorter than min_duration are discarded."""
        recorder = AudioRecorder(min_duration=1.0)  # 1 second minimum
        
        recorder.start_recording()
        time.sleep(0.2)  # Record only 0.2 seconds
        
        path = recorder.stop_recording()
        assert path is None  # Should be discarded
