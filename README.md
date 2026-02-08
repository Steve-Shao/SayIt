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

## Usage

```bash
sayit start    # Start daemon
sayit stop     # Stop daemon
sayit status   # Check status
sayit config   # Configure settings
```

## Development

```bash
# Create conda environment
conda create -n sayit python=3.12
conda activate sayit

# Install in editable mode
pip install -e ".[dev]"
```

## License

MIT
