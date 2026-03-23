# SØREN - Technical System Prompt & Project Map

This document is the **Source of Truth** for any AI agent interacting with this codebase. It contains the architectural DNA and behavioral mandates of the SØREN Shiny Hunter Bot.

## 🤖 AI AGENT MANDATES (Read Before Coding)
1.  **Self-Documentation**: After any significant logic change or feature addition, you **MUST** update both `README.md` (for users) and `GEMINI.md` (for future agents).
2.  **Human-Likeness First**: Never implement perfectly timed loops. All keyboard interactions and movements must use `random.uniform` and randomized patterns.
3.  **No Reversions**: Do not remove the hybrid detection or the randomized escape paths unless explicitly asked.
4.  **Logging Standard**: Maintain the English logging format: `[CATEGORY] Message`.

## 🏗️ Core Architecture & Logic

### 1. Advanced Movement: "Humanoid Zig-Zag" (`src/controller.py`)
- **Logic**: Instead of simple turns, the bot performs rapid bursts of movement (0.18s - 0.28s) to ensure tile-stepping.
- **Pattern**: Alternates directions (Left/Right) in random clusters (2-4 steps).
- **Goal**: Trigger encounters while staying within the same grass patch and avoiding "robotic" linear paths.

### 2. Hybrid Detection Engine (`src/bot_main.py`)
- **Battle Confirmation**: The bot checks for HUD presence using high-threshold pixel counting in calibrated slots.
- **Single Mode Fallback**: Even in "Single" mode, the bot checks Horde slots first. If a random horde appears during a single encounter search, the bot will identify all 5 slots.
- **OCR Stability**: Uses a `time.sleep(0.5)` delay before analysis to wait for UI animations. It performs up to `ocr_retries` (default 6) to account for slow ability animations (e.g., Intimidate).

### 3. Notification System
- **Discord Webhook**: Captures a frame *after* shiny confirmation, saves it as `shiny_detected.png`, and sends it via POST request.
- **Error Handling**: Log status codes (200/204) to the GUI for user troubleshooting.

## ⚙️ Configuration Schema (`config.json`)
- `mode`: "horda" or "single".
- `ocr_retries`: Number of attempts before skipping/escaping.
- `total_encounters`: Global counter.
- `discord_webhook`: Target URL.
- `slots`: Dict of 5 regions for horde detection.
- `slot_single`: Specific region for 1v1 encounters.
- `button_run`: Region for the "Run/Huir" button.

## 🛠️ Common Maintenance Tasks

### Fixing OCR Misses
- Check `ocr_retries` in the GUI.
- Verify `is_ui_present` threshold (currently 150 non-zero pixels).
- Check `src/recognizer.py` for EasyOCR language settings.

### Adjusting Movement Speed
- Modify `duration` in `controller.search_movement`. 
- **Caution**: Durations below 0.1s may only rotate the character without taking a step.

### Webhook Failures
- Verify the bot has write permissions to save `shiny_detected.png`.
- Check if the URL is valid in `config.json`.
