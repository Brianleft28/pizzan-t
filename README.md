# SØREN - Automated Pokémon Shiny & Ditto Hunter (v2.2)

SØREN is a high-performance, data-driven automated bot for Pokémon shiny hunting and mass Ditto catching. Version 2.2 introduces a fundamental shift in vision logic, prioritizing target identification over map environment details.

## 🌟 What's New in v2.2?
- **Data-Driven Logic**: The bot no longer "looks" at the map. It monitors the Pokémon Name Slot directly. If text appears, it enters Analysis Mode.
- **Verification State**: Identifies "Ditto" or "Shiny" *before* the battle menu even appears, preparing its next move instantly.
- **Cyberpunk ASCII Terminal**: Redesigned logging interface with a session timer, turn-by-turn health monitoring, and ASCII art notifications.
- **Patch-Stay Patrol**: Human-like movement bursts (0.6s-1.2s) with frequent direction changes to keep the character inside small grass patches.
- **Thread-Safe Vision**: Robust screen capture system designed for multi-threaded performance on notebooks and high-end PCs.

## 🚀 Key Features
- **Ditto Specialist**: Automated identification, transformation waiting, weakening (Swipe), soaking, sleeping, and catching.
- **Universal Shiny Capture**: Automatically enters high-priority capture mode if a shiny is detected in any 1v1 encounter.
- **Auto-Sustain**: 
    - **Leppa Berry**: Intelligent PP restoration with "MAX" quantity navigation.
    - **Potions**: Automatic hunter healing out of combat.
- **Bilingual OCR**: Seamlessly understands English and Spanish game clients.
- **Discord Alerts**: Real-time screenshots sent to your private webhook.

## 🛠️ Installation

1. **Clone & Enter**:
   ```bash
   git clone https://github.com/Brianleft28/pizzan-t
   cd pizzan-t
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Configuration & Calibration
Open the GUI (`python main_gui.py`) and use the **SCREENS CALIBRATION** panel:
1. **HORDE/SINGLE SLOTS**: Mark the areas where Pokémon names appear.
2. **RUN BUTTON**: Mark the "Run/Fight" button in the menu.
3. **HP/STATUS/PP**: Mark these essential combat areas for full automation.
4. **DEBUG FRAME**: Use this button to see a binary view of what the bot sees (helps with dark/light themes).

## 🏗️ Project Architecture
- `src/bot_main.py`: The data-driven state machine (Logic Engine).
- `src/vision.py`: Robust, thread-safe screen capture.
- `src/controller.py`: Human-like input simulation.
- `src/recognizer.py`: OCR and Template Matching engine.

## ⚠️ Disclaimer
This software is for educational purposes. Use it at your own risk. The developers are not responsible for any in-game sanctions or account actions.
