# SØREN - Automated Pokémon Shiny Hunter Bot

SØREN is a high-performance automated bot for Pokémon shiny hunting. It specializes in **Horde Encounters** and **Single Combat**, using computer vision and OCR to identify shiny Pokémon with human-like precision.

## Key Features
- **Dual Hunting Modes**: 
    - **Horde Mode**: Uses "Sweet Scent" to encounter 5 Pokémon at once.
    - **Single Mode**: Moves your character (Left/Right) to trigger wild encounters.
- **Smart Analysis**: Powered by **EasyOCR** and **OpenCV**.
- **Human Simulation**: Randomized delays and non-deterministic navigation paths.
- **Discord Integration**: Real-time alerts with screenshots.
- **Independent Calibration**: Separate coordinate settings for Horde and Single modes.

## Requirements
- Python 3.10+
- Game settings:
    - **UI Scale**: 1x (Recommended)
    - **Language**: English or Spanish (EasyOCR supports both).
    - **Keybinds**: Sweet Scent Ocarina must be assigned to a hotkey (default: `3`).

## Installation

1. **Clone & Enter**:
   ```bash
   git clone https://github.com/Brianleft28/pizzan-t
   cd pizzan-t
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use (Step-by-Step)

### 1. Game Preparation
- **Horde Mode**: 
    - Have a Pokémon with "Sweet Scent" or the Ocarina item.
    - Place the Ocarina/Move in your hotbar (default is key `3`).
    - Carry **Leppa Berries** (Zanamas) if you are using the horde mode. 
- **Single Mode**: 
    - Stand in a patch of grass or a cave where wild encounters occur.
    - The bot will move your character left and right automatically.

### 2. Calibration (CRITICAL)
Open the GUI (`python main_gui.py`) and perform the following calibrations:
1. **CALIB. HORDE SLOTS**: Draw 5 rectangles over the areas where Pokémon names appear during a horde.
2. **CALIB. SINGLE SLOT**: Draw 1 rectangle over the area where the wild Pokémon's name appears in a 1-on-1 battle.
3. **CALIB. RUN BUTTON**: Draw 1 rectangle over the "RUN" (Huir) button in the battle menu.

### 3. Start Hunting
1. Select your **Mode** (Horda or Single).
2. Paste your **Discord Webhook URL** if you want notifications.
3. Click **START HUNT**. 
4. Switch to the game window immediately.

## Project Structure
- `main_gui.py`: Main controller and user interface.
- `selector.py`: Visual calibration tool.
- `src/bot_main.py`: Logic engine and state machine.
- `src/controller.py`: Human-like input simulation (movement & keys).
- `src/recognizer.py`: OCR and image analysis.

## Disclaimer
This software is for educational purposes. Use it at your own risk. The developers are not responsible for any in-game sanctions.
