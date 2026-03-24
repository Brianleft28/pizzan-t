# SØREN - Automated Pokémon Shiny & Ditto Hunter

SØREN is a high-performance automated bot for Pokémon shiny hunting and mass Ditto catching. It uses computer vision, OCR, and human-like input simulation to provide a safe and efficient hunting experience.

## 🌟 Key Features
- **Hunting Modes**: 
    - **Horde Mode**: Uses "Sweet Scent" to encounter 5 Pokémon at once.
    - **Single Mode**: Fluid "Gapless Patrol" movement to trigger wild encounters.
    - **Ditto Mode**: Advanced AI to identify, wait for transformation, weaken, sleep, and capture Dittos automatically.
- **Auto-Capture Protocol**: Automatically catches any 1v1 Shiny or Ditto using a configurable sequence (Swipe -> Soak -> Sleep -> Ball).
- **Auto-Sustain System**: 
    - **Leppa Berry**: Automatically restores PP for specific moves (Slots 1, 2, 4) using "MAX" quantity navigation.
    - **Potions**: Automatically heals the hunter Pokémon if health drops below a threshold.
- **Smart Vision**: HUD-centric detection anchors (Menu, PP, Slots) to prevent map false positives.
- **Bilingual Support**: OCR understands English and Spanish game clients (Caught/Atrapado, Run/Huir, etc.).
- **Human Simulation**: Long key presses for fluid traversal and randomized delay patterns.
- **Discord Integration**: Real-time alerts with screenshots of your findings.

## 📋 Requirements
- Python 3.10+
- Game settings:
    - **Language**: English or Spanish.
    - **Hotkeys**: Assign Potion, Leppa, and Quick Ball to hotkeys (e.g., 4, 5, 6).
    - **Quick Access**: Moves should be assigned to slots 1-4 in the battle menu.

## 🚀 Installation

1. **Clone & Enter**:
   ```bash
   git clone https://github.com/Brianleft28/pizzan-t
   cd pizzan-t
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ How to Use

### 1. Game Preparation
- **Ditto Mode**: Stand in a Ditto area (e.g., Desert Underpass). Ensure your lead Pokémon has False Swipe, Soak, and a Sleep move in the configured slots.
- **Patrol**: The character will move continuously based on "Patrol Time" (seconds).

### 2. Calibration (Essential)
Open the GUI (`python main_gui.py`) and perform the following calibrations:
1. **HORDE SLOTS**: Mark the 5 name areas for hordes.
2. **SINGLE SLOT**: Mark the name area for 1v1.
3. **RUN BUTTON**: Mark the "Run/Fight" area.
4. **HP BAR & STATUS**: Mark the enemy's health bar and status icon areas.
5. **SLEEP ASSET**: Mark the "ZZZ" icon while a Pokémon is asleep.
6. **PP SLOTS**: Mark the 4 PP count areas in the fight menu.
7. **BATTLE MSG**: Mark the bottom text area where "Caught!" appears.
8. **HUNTER HP**: Mark your own Pokémon's HP numbers (e.g., 100/100).

### 3. Start Hunting
1. Configure your move slots and hotkeys in the **Ditto Mode Settings** tab.
2. Use **VIEW FULL LOGGER** to monitor the bot's logic in real-time.
3. Click **START AUTOMATED HUNT**.

## 🏗️ Project Structure
- `main_gui.py`: Modern UI with toggleable settings/logger.
- `selector.py`: Precise visual calibration tool.
- `src/bot_main.py`: The "Brain" - handles state machine and vision logic.
- `src/controller.py`: Human-like keyboard simulation.
- `src/recognizer.py`: OCR engine and image template matching.

## ⚠️ Disclaimer
This software is for educational purposes. Use it at your own risk. The developers are not responsible for any in-game sanctions or account actions.
