import re
import random

with open('src/controller.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Leppa timings
# Hotkey press up delay (wait for Party UI to open)
content = content.replace("time.sleep(random.uniform(0.3, 0.8))\n        \n        # 2. Select first Pokemon", "time.sleep(random.uniform(0.6, 0.9))\n        \n        # 2. Select first Pokemon")

# Z press delay (wait for Move list to open)
content = content.replace("self._press('z')\n        time.sleep(random.uniform(0.3, 0.8))\n        \n        # 3. Navigate to Move Slot", "self._press('z')\n        time.sleep(random.uniform(0.6, 1.0))\n        \n        # 3. Navigate to Move Slot")

# Z press delay (wait for Quantity submenu to open)
content = content.replace("self._press('z')\n        time.sleep(random.uniform(0.2, 0.6))\n\n        # 5. Handle Quantity Submenu", "self._press('z')\n        time.sleep(random.uniform(0.5, 0.8))\n\n        # 5. Handle Quantity Submenu")

with open('src/controller.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('src/bot_main.py', 'r', encoding='utf-8') as f:
    content_main = f.read()

content_main = content_main.replace("v6.9", "v7.0")

with open('src/bot_main.py', 'w', encoding='utf-8') as f:
    f.write(content_main)

print("Fixes applied.")
