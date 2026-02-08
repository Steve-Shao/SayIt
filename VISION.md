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

# Vision: SayIt

## The Thesis

Voice is the ultimate input method. In the AI era, speaking is faster, more natural, and more expressive than typing. The keyboard—a 150-year-old technology—should no longer be the primary way humans communicate with machines.

## Why SayIt Exists

Three observations led to this project:

**1. Local compute is enough.**
Modern laptops (especially Apple Silicon) can run Whisper-class speech recognition in real-time. Cloud dependency is no longer a technical necessity—it's a business choice.

**2. Privacy matters.**
Voice input captures everything: passwords, private thoughts, sensitive conversations. Sending this data to remote servers creates unnecessary risk. A tool this fundamental should run entirely on your machine.

**3. This should be free.**
Speech-to-text is now a commodity capability. Charging $12/month for what your laptop can do locally feels like rent-seeking. Basic infrastructure should be accessible to everyone.

## What SayIt Is

A local, open-source voice input app for macOS. Hold a key, speak, release—text appears at your cursor. No cloud. No subscription. No data leaves your machine.

Packaged as a native macOS application for end users, with an optional CLI for developers.

## What SayIt Is Not

- Not an AI assistant or chatbot
- Not a meeting transcription tool
- Not a voice command system
- Not trying to "polish" or rewrite your words

SayIt is a keyboard replacement. It transcribes exactly what you say, nothing more.

## Design Philosophy

**Invisible when working.** The best tool is one you forget exists. SayIt should feel like a natural extension of typing—press, speak, done.

**Local-first, always.** No network requests. No telemetry. No accounts. Your voice stays on your device.

**Simple over clever.** One hotkey. One function. No modes, no menus, no learning curve.
