"""SenseVoice transcription for SayIt.

SenseVoice is developed by Alibaba FunAudioLLM. It excels at Chinese recognition
and supports Chinese, Cantonese, English, Japanese, and Korean with excellent
mixed-language performance.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

MODEL_ID = "iic/SenseVoiceSmall"


def _is_model_cached() -> bool:
    """Check if model is already downloaded."""
    cache_dir = Path.home() / ".cache" / "modelscope" / "hub" / "models" / "iic" / "SenseVoiceSmall"
    return cache_dir.exists()


class Transcriber:
    """Speech-to-text transcription using SenseVoice."""

    def __init__(self):
        self._model = None
        self._first_run_logged = False

    def transcribe(self, audio_path: str, language: str = "auto") -> str:
        """Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file (any format supported).
            language: Language code ("auto", "zh", "en", "yue", "ja", "ko").
            
        Returns:
            Transcribed text.
        """
        from funasr import AutoModel
        from funasr.utils.postprocess_utils import rich_transcription_postprocess

        # Log first-run download notice
        if not self._first_run_logged and not _is_model_cached():
            logger.info(
                f"First run: downloading SenseVoice model (~900MB). "
                "This may take a few minutes..."
            )
            self._first_run_logged = True

        # Lazy load model
        if self._model is None:
            logger.debug(f"Loading SenseVoice model: {MODEL_ID}")
            self._model = AutoModel(
                model=MODEL_ID,
                trust_remote_code=True,
                device="cpu",
                disable_update=True,
            )

        logger.debug(f"Transcribing: {audio_path}")
        
        # SenseVoice language codes
        lang_map = {
            "auto": "auto",
            "zh": "zh",
            "en": "en",
            "yue": "yue",
            "ja": "ja",
            "ko": "ko",
        }
        lang = lang_map.get(language, "auto")

        result = self._model.generate(
            input=audio_path,
            cache={},
            language=lang,
            use_itn=True,
            batch_size_s=60,
        )
        
        text = rich_transcription_postprocess(result[0]["text"])
        logger.debug(f"Result: {text[:50]}..." if len(text) > 50 else f"Result: {text}")
        return text
