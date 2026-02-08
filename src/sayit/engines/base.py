"""Abstract base class for transcription engines."""

from abc import ABC, abstractmethod


class TranscriptionEngine(ABC):
    """Base class for all transcription engines."""

    @abstractmethod
    def load_model(self, model_name: str) -> None:
        """Load the specified model.
        
        Args:
            model_name: Model identifier (e.g., "distil-large-v3", "base").
        """

    @abstractmethod
    def transcribe(self, audio_path: str, language: str = "auto") -> str:
        """Transcribe audio file to text.
        
        Args:
            audio_path: Path to WAV file.
            language: Language code ("auto", "zh", "en", "ja").
            
        Returns:
            Transcribed text.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """Check if engine dependencies are installed.
        
        Returns:
            True if engine can be used.
        """


# Engine registry
_ENGINES: dict[str, type[TranscriptionEngine]] = {}


def register_engine(name: str):
    """Decorator to register an engine class."""
    def decorator(cls: type[TranscriptionEngine]):
        _ENGINES[name] = cls
        return cls
    return decorator


def get_engine(name: str) -> TranscriptionEngine:
    """Create engine instance by name.
    
    Args:
        name: Engine name ("mlx-whisper", "faster-whisper", "sensevoice").
        
    Returns:
        Engine instance.
        
    Raises:
        ValueError: If engine not found.
    """
    if name not in _ENGINES:
        available = ", ".join(_ENGINES.keys()) or "none"
        raise ValueError(f"Unknown engine '{name}'. Available: {available}")
    return _ENGINES[name]()


def get_available_engines() -> list[str]:
    """Return list of registered engine names."""
    return list(_ENGINES.keys())
