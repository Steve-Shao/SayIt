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

# SayIt

Local voice-to-text for macOS. Hold a key, speak, release—text appears at cursor. No cloud. No subscription.

## Why SayIt

Voice is faster than typing. Modern laptops can run speech recognition locally. Your voice data should stay on your machine. SayIt makes this possible: a simple, open-source keyboard replacement that transcribes exactly what you say.

See [VISION.md](VISION.md) for the full rationale.

---

## Installation

**Requirements:** macOS 12+, Apple Silicon, Python 3.12+, ffmpeg

```bash
# Install ffmpeg (if not already)
brew install ffmpeg

# Install SayIt
pip install sayit
```

Or from source:

```bash
git clone https://github.com/steve-shao/sayit.git
cd sayit
pip install -e .
```

---

## Usage

```bash
sayit start    # Start daemon
sayit stop     # Stop daemon
sayit status   # Check status
sayit config   # View/edit settings
```

Hold Right Option (default), speak, release. Text appears at cursor.

### Permissions

Grant in System Settings → Privacy & Security:

| Permission | Purpose |
|------------|---------|
| Accessibility | Hotkey detection, text injection |
| Microphone | Audio recording |

---

## Documentation

| Document | Purpose |
|----------|---------|
| [VISION.md](VISION.md) | Product philosophy and goals |
| [ROADMAP.md](ROADMAP.md) | Development phases and status |
| [DEVELOPER.md](DEVELOPER.md) | Architecture, components, technical details |
| [ISSUES.md](ISSUES.md) | Known bugs and improvements |

---

## Development Workflow

SayIt uses a spec-driven development process:

1. **Plan:** Create a feature spec in `.kiro/specs/` with requirements and tasks
2. **Build:** Implement the feature following the spec
3. **Test:** Use daily, document issues in ISSUES.md
4. **Update:** Merge learnings into project docs, archive the spec
5. **Repeat:** Move to next phase in ROADMAP.md

To contribute or extend SayIt, start with [DEVELOPER.md](DEVELOPER.md) for architecture overview, then check [ROADMAP.md](ROADMAP.md) for current priorities.

---

## License

MIT
