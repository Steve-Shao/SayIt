"""Tests for MLX Whisper engine."""

import pytest

from sayit.engines.base import get_engine, get_available_engines


class TestMLXWhisperEngine:
    """Unit tests for MLXWhisperEngine."""

    def test_engine_registered(self):
        """Engine should be registered after import."""
        import sayit.engines.mlx_whisper  # noqa: F401
        
        assert "mlx-whisper" in get_available_engines()

    def test_get_engine(self):
        """Factory should return MLXWhisperEngine instance."""
        import sayit.engines.mlx_whisper  # noqa: F401
        
        engine = get_engine("mlx-whisper")
        assert engine.__class__.__name__ == "MLXWhisperEngine"

    def test_is_available(self):
        """is_available should return bool based on package presence."""
        import sayit.engines.mlx_whisper  # noqa: F401
        
        engine = get_engine("mlx-whisper")
        result = engine.is_available()
        assert isinstance(result, bool)

    def test_load_model_sets_name(self):
        """load_model should set the model name."""
        import sayit.engines.mlx_whisper  # noqa: F401
        
        engine = get_engine("mlx-whisper")
        engine.load_model("mlx-community/whisper-small")
        assert engine._model_name == "mlx-community/whisper-small"


@pytest.mark.hardware
class TestMLXWhisperTranscription:
    """Integration tests requiring actual transcription."""

    def test_transcribe_audio(self, tmp_path):
        """Transcribe a test audio file."""
        import sayit.engines.mlx_whisper  # noqa: F401
        
        engine = get_engine("mlx-whisper")
        if not engine.is_available():
            pytest.skip("mlx-whisper not installed")

        # Create a simple test WAV (silence)
        import numpy as np
        import wave

        wav_path = tmp_path / "test.wav"
        sample_rate = 16000
        duration = 1.0
        samples = np.zeros(int(sample_rate * duration), dtype=np.int16)

        with wave.open(str(wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(samples.tobytes())

        # Transcribe (silence should return empty or minimal text)
        result = engine.transcribe(str(wav_path))
        assert isinstance(result, str)


if __name__ == "__main__":
    import sayit.engines.mlx_whisper  # noqa: F401
    
    engine = get_engine("mlx-whisper")
    print(f"Available: {engine.is_available()}")
    print(f"Registered engines: {get_available_engines()}")
