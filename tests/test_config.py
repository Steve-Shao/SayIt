"""Tests for configuration management."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from sayit.config import Config, CONFIG_FILE


class TestConfig:
    """Test Config class."""
    
    def test_default_values(self):
        """Test default config values."""
        config = Config()
        assert config.hotkey == "fn"
        assert config.engine == "mlx-whisper"
        assert config.model == "distil-large-v3"
        assert config.language == "auto"
        assert config.sounds_enabled is True
        assert config.min_recording_duration == 0.3
    
    def test_save_and_load(self, tmp_path):
        """Test saving and loading config."""
        config_file = tmp_path / "config.json"
        config_dir = tmp_path
        
        with patch("sayit.config.CONFIG_FILE", config_file), \
             patch("sayit.config.CONFIG_DIR", config_dir):
            # Save config
            config = Config(hotkey="ctrl", engine="faster-whisper")
            config.save()
            
            # Verify file exists
            assert config_file.exists()
            
            # Load and verify
            loaded = Config.load()
            assert loaded.hotkey == "ctrl"
            assert loaded.engine == "faster-whisper"
    
    def test_load_missing_file(self, tmp_path):
        """Test loading when config file doesn't exist."""
        config_file = tmp_path / "nonexistent" / "config.json"
        
        with patch("sayit.config.CONFIG_FILE", config_file):
            config = Config.load()
            # Should return default config
            assert config.hotkey == "fn"
    
    def test_load_invalid_json(self, tmp_path):
        """Test loading invalid JSON file."""
        config_file = tmp_path / "config.json"
        config_file.write_text("invalid json {{{")
        
        with patch("sayit.config.CONFIG_FILE", config_file):
            config = Config.load()
            # Should return default config
            assert config.hotkey == "fn"
    
    def test_reset(self, tmp_path):
        """Test resetting config to defaults."""
        config_file = tmp_path / "config.json"
        config_dir = tmp_path
        
        with patch("sayit.config.CONFIG_FILE", config_file), \
             patch("sayit.config.CONFIG_DIR", config_dir):
            # Save custom config
            config = Config(hotkey="ctrl")
            config.save()
            
            # Reset
            reset_config = Config.reset()
            assert reset_config.hotkey == "fn"
            
            # Verify file was updated
            loaded = Config.load()
            assert loaded.hotkey == "fn"
