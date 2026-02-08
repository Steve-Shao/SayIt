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

# Roadmap: SayIt

**Current Status:** Phase 4 (Local Testing and Polishing)

---

## Phase 8: Cross-Platform Support

**Goal:** Extend SayIt beyond macOS.

- [ ] Linux support (xdotool for text injection)
- [ ] Platform detection and conditional loading
- [ ] faster-whisper as default engine for Linux
- [ ] Test on Ubuntu/Debian

---

## Phase 7: Additional Engines

**Goal:** Support alternative transcription backends.

- [ ] faster-whisper engine (cross-platform, CPU)
- [ ] SenseVoice engine (Chinese-optimized)
- [ ] Engine switching via config (`sayit config set engine <name>`)
- [ ] `sayit engines` command to list available engines

---

## Phase 6: Initial Publication

**Goal:** Make SayIt publicly available and discoverable.

- [ ] Build project website (GitHub Pages or simple landing page)
- [ ] Write announcement post
- [ ] Push to GitHub (public repository)
- [ ] Submit to relevant communities (Hacker News, Reddit, etc.)

---

## Phase 5: Packaging and Installation Testing

**Goal:** Make installation simple and reliable for end users.

- [ ] Simplify dependency installation
- [ ] Test fresh install on clean macOS system
- [ ] Write clear installation guide
- [ ] Consider PyPI publication (`pip install sayit`)
- [ ] Test installation from PyPI

---

## Phase 4: Local Testing and Polishing ← Current

**Goal:** Refine the user experience through daily use.

- [ ] Use SayIt daily as primary voice input tool
- [ ] Document bugs and friction points
- [ ] Fix critical issues
- [ ] Optimize transcription latency
- [ ] Improve error handling and user feedback

---

## Phase 3: Transcription + Text Injection ✓

**Completed:** End-to-end voice input working.

- [x] MLX Whisper engine integration
- [x] Text injection via clipboard + paste
- [x] Focus restoration after indicator shows
- [x] Support for Chinese, English, Japanese

---

## Phase 2: Hotkey + Recording + Feedback ✓

**Completed:** Audio recording with visual and audio feedback.

- [x] Global hotkey listener (pynput)
- [x] Audio recording (16kHz WAV)
- [x] Sound feedback (Tink/Pop)
- [x] Floating status indicator (tkinter)

---

## Phase 1: CLI Shell + Config ✓

**Completed:** Basic infrastructure.

- [x] CLI commands (`sayit start/stop/status/config`)
- [x] Configuration management
- [x] Logging system
- [x] Daemon process management
