"""SayIt configuration management."""

import json
from dataclasses import dataclass, asdict
from pathlib import Path


CONFIG_DIR = Path.home() / ".config" / "sayit"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    """SayIt configuration."""
    
    hotkey: str = "alt_r"  # Default: Right Option key
    language: str = "auto"  # "auto", "zh", "en", "ja", "ko", "yue"
    sounds_enabled: bool = True
    min_recording_duration: float = 0.3
    
    @staticmethod
    def is_valid_hotkey(key: str) -> bool:
        """Check if hotkey is supported."""
        from sayit.hotkey import HotkeyListener
        return HotkeyListener.is_valid_key(key)
    
    @classmethod
    def load(cls) -> "Config":
        """Load config from file. Create default if not exists."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                # Filter out old config keys that no longer exist
                valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
                filtered = {k: v for k, v in data.items() if k in valid_keys}
                return cls(**filtered)
            except (json.JSONDecodeError, TypeError):
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
