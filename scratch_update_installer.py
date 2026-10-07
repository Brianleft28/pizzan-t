import sys
import re

with open("scripts/installer.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace theme_source and theme_dest
content = content.replace(
    "theme_source = os.path.join(os.path.dirname(__file__), \"..\", \"pizzatheme\")",
    "theme_source = os.path.join(os.path.dirname(__file__), \"..\", \"moontheme\")"
)
content = content.replace(
    "theme_dest = os.path.join(pokemmo_dir, \"data\", \"themes\", \"PizzantTheme\")",
    "theme_dest = os.path.join(pokemmo_dir, \"data\", \"themes\", \"MoonTheme\")"
)
content = content.replace(
    "pizzant_info_path = os.path.join(theme_dest, \"info.xml\")",
    "moon_info_path = os.path.join(theme_dest, \"info.xml\")"
)
content = content.replace("pizzant_info_path", "moon_info_path")
content = content.replace("tree_pizzant", "tree_moon")
content = content.replace("root_pizzant", "root_moon")
content = content.replace("Pizzant", "Moon")

# Add mod copying logic inside auto_sync_theme
mod_logic = """
    # Copiar Mods
    mods_source = os.path.join(os.path.dirname(__file__), "..", "mods")
    mods_dest = os.path.join(pokemmo_dir, "data", "mods")
    try:
        if os.path.exists(mods_source) and os.path.isdir(mods_source):
            if not os.path.exists(mods_dest):
                os.makedirs(mods_dest)
            for item in os.listdir(mods_source):
                s = os.path.join(mods_source, item)
                d = os.path.join(mods_dest, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
    except Exception as e:
        logger.warning(f"Error copiando mods: {e}")
"""

# Insert mod_logic before patching XML
content = content.replace("    # Parchear XML con la versi?n correcta en el destino", mod_logic + "\n    # Parchear XML con la versi?n correcta en el destino")

with open("scripts/installer.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Done")
