"""MLX Whisper engine for Apple Silicon Macs."""

import logging
import shutil
from pathlib import Path

from sayit.engines.base import TranscriptionEngine, register_engine

logger = logging.getLogger(__name__)

# Default model: fast and accurate
DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"


def _check_ffmpeg() -> None:
    """Check if ffmpeg is installed."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "ffmpeg not found. Install with: brew install ffmpeg"
        )


def _is_model_cached(model_name: str) -> bool:
    """Check if model is already downloaded."""
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
    # HuggingFace cache uses model name with -- separator
    model_dir_name = "models--" + model_name.replace("/", "--")
    return (cache_dir / model_dir_name).exists()


@register_engine("mlx-whisper")
class MLXWhisperEngine(TranscriptionEngine):
    """Transcription engine using mlx-whisper.
    
    Optimized for Apple Silicon.
    """

    def __init__(self):
        self._model_name: str | None = None
        self._first_run_logged = False

    def load_model(self, model_name: str = DEFAULT_MODEL) -> None:
        """Set model to use for transcription.
        
        Args:
            model_name: HuggingFace model path. Options include:
                - "mlx-community/whisper-large-v3-turbo" (default, fast)
                - "mlx-community/whisper-large-v3"
                - "mlx-community/whisper-small"
                - "mlx-community/whisper-base"
        """
        self._model_name = model_name
        logger.info(f"Model set: {model_name}")

    def transcribe(self, audio_path: str, language: str = "auto") -> str:
        """Transcribe audio file.
        
        Args:
            audio_path: Path to WAV file (16kHz recommended).
            language: Language hint. "auto" for auto-detect.
            
        Returns:
            Transcribed text.
        """
        _check_ffmpeg()
        
        import mlx_whisper

        if self._model_name is None:
            self._model_name = DEFAULT_MODEL

        # Log first-run model download notice
        if not self._first_run_logged and not _is_model_cached(self._model_name):
            logger.info(
                f"First run: downloading model '{self._model_name}' (~1.5GB). "
                "This may take a few minutes..."
            )
            self._first_run_logged = True

        logger.debug(f"Transcribing: {audio_path}")
        result = mlx_whisper.transcribe(
            audio_path,
            path_or_hf_repo=self._model_name,
        )
        text = result.get("text", "").strip()
        logger.debug(f"Result: {text[:50]}..." if len(text) > 50 else f"Result: {text}")
        return text

    def is_available(self) -> bool:
        """Check if mlx-whisper is installed."""
        try:
            import mlx_whisper  # noqa: F401
            return True
        except ImportError:
            return False
