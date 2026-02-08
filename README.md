# SayIt

Local, privacy-focused voice-to-text for macOS (and Linux).

Hold a hotkey to record, release to transcribe locally, text appears at cursor.

## Features

- System-wide hotkey activation
- Local transcription (no cloud)
- Multiple engine support (MLX Whisper, faster-whisper, SenseVoice)
- Cross-platform (macOS primary, Linux planned)

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

## Usage

```bash
# Start the daemon
sayit start

# Check status
sayit status

# Stop the daemon
sayit stop

# View/modify configuration
sayit config
sayit config set hotkey ctrl_r
sayit config reset
```

## Configuration

Configuration is stored in `~/.config/sayit/config.json`.

| Setting | Default | Description |
|---------|---------|-------------|
| hotkey | alt_r | Trigger key (Right Option). See supported keys below. |
| engine | mlx-whisper | Transcription engine |
| model | distil-large-v3 | Model variant |
| language | auto | Language preference |
| sounds_enabled | true | Audio feedback |
| min_recording_duration | 0.3 | Minimum recording length (seconds) |

### Supported Hotkeys

`alt_r`, `alt_l`, `ctrl_r`, `ctrl_l`, `cmd_r`, `cmd_l`, `shift_r`, `shift_l`, `f1`-`f12`

Note: The Fn key is not supported (cannot be detected by pynput on macOS).

## Development

```bash
# Create conda environment
conda create -n sayit python=3.12
conda activate sayit

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest -v
```

## Project Status

- [x] Phase 1: CLI Shell + Config
- [ ] Phase 2: Hotkey + Recording + Feedback
- [ ] Phase 3: Transcription + Text Injection
- [ ] Phase 4: Additional Engines
- [ ] Phase 5: Cross-Platform Support

## License

MIT
