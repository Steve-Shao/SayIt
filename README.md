# SayIt

Local, privacy-focused voice-to-text for macOS.

Hold a hotkey to record, release to transcribe locally, text appears at cursor.

## Features

- System-wide hotkey activation (Right Option by default)
- Local transcription using MLX Whisper (no cloud, no data sent anywhere)
- Audio recording with sound feedback (start/stop sounds)
- Visual status indicator (red → orange during transcription)
- Automatic text injection at cursor position
- Unicode support (Chinese, Japanese, etc.)

## Requirements

- macOS 12+ (Monterey or later)
- Apple Silicon Mac (M1/M2/M3)
- Python 3.12+
- ffmpeg (`brew install ffmpeg`)

## Installation

```bash
pip install sayit
```

Or from source:

```bash
git clone https://github.com/steve-shao/sayit.git
cd sayit
pip install -e .
```

## Quick Start

```bash
# Start the daemon
sayit start

# Hold Right Option key, speak, release
# Text appears at your cursor!

# Stop when done
sayit stop
```

## Usage

```bash
sayit start      # Start background daemon
sayit stop       # Stop daemon
sayit status     # Check if running
sayit config     # View configuration
sayit config set hotkey cmd_r    # Change hotkey
sayit config set model mlx-community/whisper-large-v3-turbo
```

## Configuration

Stored in `~/.config/sayit/config.json`.

| Setting | Default | Description |
|---------|---------|-------------|
| hotkey | alt_r | Trigger key (Right Option) |
| engine | mlx-whisper | Transcription engine |
| model | mlx-community/whisper-large-v3-turbo | Whisper model |
| language | auto | Language (auto, zh, en, ja) |
| sounds_enabled | true | Audio feedback |

### Supported Hotkeys

`alt_r`, `alt_l`, `ctrl_r`, `ctrl_l`, `cmd_r`, `cmd_l`, `shift_r`, `shift_l`, `f1`-`f12`

## Permissions

Grant these in System Settings → Privacy & Security:

- **Accessibility**: Required for hotkey detection and text injection
- **Microphone**: Required for audio recording

## Development

```bash
conda create -n sayit python=3.12
conda activate sayit
pip install -e ".[dev]"
pytest -v -m "not hardware"
```

## Project Status

- [x] Phase 1: CLI + Config
- [x] Phase 2: Hotkey + Recording + Feedback
- [x] Phase 3: Transcription + Text Injection
- [ ] Phase 4: Additional Engines (faster-whisper, SenseVoice)
- [ ] Phase 5: Linux Support

## License

MIT
