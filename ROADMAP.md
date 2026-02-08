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

**Current Status:** Phase 4 (Local Testing and FunASR Integration)

---

## Phase 7: Initial Publication

**Goal:** Make SayIt publicly available and discoverable.

- [ ] Build project website (GitHub Pages or simple landing page)
- [ ] Write announcement post
- [ ] Push to GitHub (public repository)
- [ ] Submit to relevant communities (Hacker News, Reddit, etc.)

---

## Phase 6: macOS App Packaging

**Goal:** Package SayIt as a native macOS application.

- [ ] PyInstaller setup for .app bundle
- [ ] Settings UI (hotkey, language selection)
- [ ] Test on clean macOS system
- [ ] Code signing and notarization
- [ ] DMG installer

---

## Phase 5: Additional Models via FunASR

**Goal:** Support alternative speech recognition models through FunASR.

- [ ] Test Paraformer (Chinese-optimized)
- [ ] Test Whisper via FunASR
- [ ] Test Qwen-Audio
- [ ] Model switching via config
- [ ] Document model comparison (accuracy, speed, languages)

---

## Phase 4: Local Testing and FunASR Integration ← Current

**Goal:** Refine user experience and establish FunASR as the unified framework.

- [x] FunASR as unified inference framework
- [x] SenseVoice as default model (excellent Chinese-English mixed recognition)
- [x] Simplified codebase (removed multi-engine abstraction)
- [ ] Use SayIt daily as primary voice input tool
- [ ] Document bugs and friction points
- [ ] Fix critical issues
- [ ] Optimize transcription latency

---

## Phase 3: Transcription + Text Injection ✓

**Completed:** End-to-end voice input working.

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
