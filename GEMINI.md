# SØREN - Technical System Prompt & Project Map

This document is the **Source of Truth** for any AI agent interacting with this codebase. It contains the architectural DNA and behavioral mandates of the SØREN Shiny Hunter Bot.

## 🤖 AI AGENT MANDATES (Read Before Coding)
1.  **Self-Documentation**: After any significant logic change, update `README.md` and `GEMINI.md`.
2.  **Human-Likeness**: Movements must use randomized bursts (0.6s - 1.2s) and high-frequency direction changes (50% flip rate) to simulate human searching.
3.  **Data-Driven Decision**: NEVER attempt actions based on map details. Confirmation MUST come from OCR (Name Slot) or HUD Anchors (Run Button).
4.  **Logging Standard**: Maintain the Cyberpunk ASCII terminal style with [HH:MM:SS] session timers.

## 🏗️ Core Architecture (v2.2 Data Driven)

### 1. Battle Entry: "Target-First" Logic
- **Trigger**: The bot monitors the `slot_single` region for any non-zero pixels (text) using a 180-threshold binary mask.
- **Verification**: Once triggered, it enters a `Verification State`. It performs up to 10 OCR scans to identify the target name or Shiny status *before* looking for the menu.
- **Action Gate**: Decisions (Capture or Escape) are queued but **NEVER** executed until `is_menu_present` returns `True`. This eliminates errors during battle entry animations.

### 2. Patch-Stay Patrol
- **Burst Pattern**: Movement is performed in short bursts (0.6s - 1.2s) to stay within small grass patches.
- **Directional Flip**: After each burst, there is a 50% chance to reverse direction, ensuring the bot stays localized and doesn't run into distant walls.

### 3. Combat & Maintenance
- **Universal Capture**: Applies to Dittos or any Shiny. Sequence: Swipe -> Soak -> Sleep -> Balls.
- **PP/HP Logic**: Every turn, the bot reads Hunter HP and Target Status. PP restoration uses the "MAX" navigation protocol (Up, Right, Z, Down, Z) if the gap is >= 10.
- **X-Spam Cleanup**: 3 rapid 'X' presses (0.5s interval) after battle to clear post-capture screens.

### 4. Vision System
- **Thread-Safety**: `PokéObserver` creates a new `mss` instance per thread to avoid `srcdc` attribute errors.
- **Thresholds**: 
    - Slots: 180 (for light text on dark/minimalist backgrounds).
    - Menu: 160 (for the "Run" button anchor).

## ⚙️ Configuration Schema (`config.json`)
- `mode`: "horda", "single", or "ditto".
- `ditto_patrol_time`: Not used in v2.2 (replaced by random bursts).
- `hunter_pokemon_name`: String used to confirm successful Ditto transformation.
- `slots/pp_slots/battle_msg_region`: All regions are mandatory for full automation.

## 🛠️ Diagnostics
- **Debug Frame**: Use the `save_debug_frame` method to generate `debug_view.png` (binary threshold) to verify what the bot sees.
