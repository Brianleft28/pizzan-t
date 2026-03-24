# SØREN - Technical System Prompt & Project Map

This document is the **Source of Truth** for any AI agent interacting with this codebase. It contains the architectural DNA and behavioral mandates of the SØREN Shiny Hunter Bot.

## 🤖 AI AGENT MANDATES (Read Before Coding)
1.  **Self-Documentation**: After any significant logic change or feature addition, you **MUST** update both `README.md` (for users) and `GEMINI.md` (for future agents).
2.  **Human-Likeness First**: Never implement perfectly timed loops. All keyboard interactions and movements must use `random.uniform` and randomized patterns. Avoid short, rhythmic "robo-steps".
3.  **No Reversions**: Do not remove the hybrid detection, the gapless patrol, or the maintenance logic unless explicitly asked.
4.  **Logging Standard**: Maintain the English logging format: `[CATEGORY] Message`.
5.  **Bilingual Support**: All OCR keyword checks must include both English and Spanish terms (e.g., `Caught` / `Atrapado`).

## 🏗️ Core Architecture & Logic

### 1. Fluid Movement: "Gapless Patrol" (`src/controller.py`)
- **Logic**: Instead of steps, the bot uses continuous key holding (`key_down`) for a randomized duration (1.5s - 3.5s).
- **Scanning**: While moving, the bot performs high-speed HUD scanning (every 0.05s).
- **Reaction**: Keys are released (`key_up`) immediately upon battle detection, ensuring zero-pause fluid traversal.

### 2. HUD-Centric Detection (`src/bot_main.py`)
- **Battle Confirmation**: To avoid map false positives (flowers, arena), the bot uses three anchors:
    1. **Menu Anchor**: High-threshold check (180 gray) for the "Run/Fight" button.
    2. **PP Anchor**: Check for bright numbers in calibrated PP slots.
    3. **Slot Anchor**: Pure white threshold (230 gray) for Pokémon name/level boxes.
- **OCR Stability**: Uses a `time.sleep(1.0)` delay after menu detection to wait for animations to settle before Phase 1 analysis.

### 3. Auto-Capture Protocol (Universal 1v1)
- **Priority**: Used for Ditto and Single Shiny encounters.
- **Sequence**: 
    1. **False Swipe**: Priority 1 to prevent Substitute (costing HP) and set logical `has_swiped` flag.
    2. **Soak**: Priority 2 to ensure transformation and remove type immunities.
    3. **Sleep**: Priority 3 only after health is low.
    4. **Balls**: Spammed while target is asleep.
- **Logical HP**: Once a move is executed, the bot logically assumes 1 HP, overriding potentially noisy pixel detection.

### 4. Maintenance & Auto-Sustain
- **Leppa Berry**: Proactive restoration if a PP "gap" of 10 or more is detected. Navigates submenus to select "MAX" quantity.
- **Potions**: Triggered if the hunter is missing 60 HP or more.
- **Safety**: Maintenance only occurs out of combat after verifying map stability for 2.5 seconds.

### 5. Post-Capture Cleanup
- **X-Spam**: Pressing 'X' six times (0.6s intervals) after battle to clear nicknames, summaries, and "Sent to PC" popups.

## ⚙️ Configuration Schema (`config.json`)
- `mode`: "horda", "single", or "ditto".
- `ocr_retries`: OCR attempts for general battle.
- `ditto_ocr_retries`: Fast-check attempts for Ditto mode.
- `ditto_patrol_time`: Base duration for one direction.
- `hunter_pokemon_name`: Target name for transformation confirmation.
- `ditto_key_attack/sleep/soak/ball/leppa/potion`: Hotkeys and slots (1-4).
- `hp_bar_region`, `status_slot_region`, `pp_slots`, `battle_msg_region`, `hunter_hp_region`: Calibrated areas.

## 🛠️ Common Maintenance Tasks

### Adjusting Vision Sensitivity
- For map noise: Increase threshold in `is_ui_present` (>230).
- For menu misses: Decrease threshold in `is_menu_present` (<160).

### Refining OCR
- Check `src/recognizer.py` for image preprocessing (currently uses 3x upscaling for PP slots).
