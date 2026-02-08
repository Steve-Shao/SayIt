<!--
WRITING_PREFERENCES:
  principles:
    - Beautiful is better than ugly
    - Simple is better than complex
    - Readability counts
    - Polish relentlessly
  style:
    - Clear and precise
    - Bottom line up front (BLUF)
    - Plain words, short sentences
    - Concise and compact
    - Factual and specific
    - Active voice
  format:
    - Use tables for structured comparisons
    - Use bullet points sparingly
    - Prefer prose over lists when explaining ideas
    - Keep sections short and focused
-->

# Developer Notes: SayIt

Technical decisions, architecture notes, and implementation details.

---

## Glossary

| Term | Definition |
|------|------------|
| SayItCore | Main application class. Manages event loop and coordinates all components. |
| HotkeyListener | Monitors global keyboard events for the configured trigger key. |
| AudioRecorder | Captures microphone input during recording sessions. |
| Transcriber | Converts audio to text using FunASR framework with SenseVoice model. |
| TextInjector | Simulates keyboard input to insert text at cursor position. |
| StatusIndicator | Floating window showing recording/processing state. |
| SoundPlayer | Plays audio feedback for state transitions. |
| Config | Dataclass holding user preferences. Persisted as JSON. |

---

## Architecture

SayIt uses an inverted threading model to satisfy macOS GUI requirements:

| Thread | Responsibility |
|--------|----------------|
| Main | tkinter mainloop, StatusIndicator |
| Background | HotkeyListener (pynput) |

The `root.after()` mechanism schedules GUI operations from background threads safely.

### Data Flow

```
1. User holds hotkey
2. HotkeyListener.on_press() → start recording, show indicator, play sound
3. User releases hotkey
4. HotkeyListener.on_release() → stop recording, hide indicator, play sound
5. Transcriber.transcribe(audio_path)
6. TextInjector.inject(text)
```

### Source Structure

```
src/sayit/
├── cli.py           # CLI entry point (click)
├── daemon.py        # Process management
├── daemon_runner.py # Standalone daemon entry
├── core.py          # Main event loop
├── hotkey.py        # Hotkey listener
├── recorder.py      # Audio capture
├── injector.py      # Text injection
├── indicator.py     # Status window
├── config.py        # Configuration
├── sounds.py        # Audio feedback
├── transcriber.py   # Speech-to-text (FunASR/SenseVoice)
└── logging.py       # Logging setup
```

---

## Key Implementation Decisions

**Text Injection:** Uses clipboard + Cmd+V paste instead of AppleScript `keystroke`. The latter fails for non-ASCII characters and certain input method states.

**Daemon Process:** Uses `subprocess.Popen` instead of `os.fork()`. Fork causes tkinter to fail on macOS because GUI must initialize in the main process.

**FunASR Framework:** Unified inference framework supporting multiple models. Currently uses SenseVoice for excellent Chinese-English mixed recognition.

---

## File Locations

| Item | Path |
|------|------|
| Config | `~/.config/sayit/config.json` |
| Logs | `~/.config/sayit/logs/sayit.log` |
| PID | `~/.config/sayit/sayit.pid` |
| Models | `~/.cache/modelscope/hub/` (managed by FunASR) |

---

## Development Commands

```bash
# Activate environment
conda activate sayit

# Run tests
python -m pytest tests/ -v -m "not hardware"

# View logs
tail -f ~/.config/sayit/logs/sayit.log

# Manual test
sayit start
# ... use voice input ...
sayit stop
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| click | CLI framework |
| rich | CLI formatting |
| pynput | Global hotkey |
| sounddevice | Audio recording |
| funasr | Speech recognition framework |
| torch | PyTorch backend for FunASR |
| tkinter | Status indicator (built-in) |

---

## Supported Hotkeys

| Key | Name | Notes |
|-----|------|-------|
| Right Option | `alt_r` | Default. Rarely conflicts. |
| Left Option | `alt_l` | Alternative. |
| Right/Left Command | `cmd_r`, `cmd_l` | May conflict with system shortcuts. |
| Right/Left Control | `ctrl_r`, `ctrl_l` | Available. |
| Right/Left Shift | `shift_r`, `shift_l` | Available. |
| F1-F12 | `f1` to `f12` | May require disabling system shortcuts. |

The Fn key cannot be detected by pynput on macOS.

---

## Configuration Schema

```json
{
  "hotkey": "alt_r",
  "language": "auto",
  "sounds_enabled": true,
  "min_recording_duration": 0.3
}
```

Supported languages: `auto`, `zh`, `en`, `ja`, `ko`, `yue` (Cantonese).

---

## Permissions (macOS)

| Permission | Purpose | Location |
|------------|---------|----------|
| Accessibility | Hotkey detection, text injection | System Settings → Privacy → Accessibility |
| Microphone | Audio recording | System Settings → Privacy → Microphone |

SayIt prompts for permissions on first use. If denied, it provides instructions to grant manually.
