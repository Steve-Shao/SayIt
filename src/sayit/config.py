"""SayIt configuration management."""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


CONFIG_DIR = Path.home() / ".config" / "sayit"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    """SayIt configuration."""
    
    hotkey: str = "fn"
    engine: str = "mlx-whisper"
    model: str = "distil-large-v3"
    language: str = "auto"
    sounds_enabled: bool = True
    min_recording_duration: float = 0.3
    
    @classmethod
    def load(cls) -> "Config":
        """Load config from file. Create default if not exists."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                return cls(**data)
            except (json.JSONDecodeError, TypeError):
                # Invalid config, return default
                return cls()
        return cls()
    
    def save(self) -> None:
        """Save config to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def reset(cls) -> "Config":
        """Reset to default config and save."""
        config = cls()
        config.save()
        return config
