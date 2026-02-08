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

# Issues: SayIt

Tracking bugs, friction points, and improvements discovered during daily use.

---

## Open

### 1. Silent failure when model unavailable

**Problem:** When the model fails to download or load, transcription silently fails. The status indicator keeps spinning with no error feedback.

**Root cause:** Transcription runs in a background thread. Failures are logged but not surfaced to the user.

**Suggested fix:**
- Show error indicator when transcription fails
- Add startup check for model availability
- Add timeout mechanism (e.g., 30s) with user notification

---

## Resolved

### ~~2. Chinese text uses English punctuation~~ ✓

**Resolved:** Switched to SenseVoice engine which handles Chinese punctuation correctly.

---

### ~~3. Mixed Chinese-English transcription quality~~ ✓

**Resolved:** SenseVoice provides excellent mixed Chinese-English recognition out of the box. No special configuration needed.
