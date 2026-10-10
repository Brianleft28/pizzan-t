"""
config_gui.py - GUI editor for patcher_config.json.

Opens a tkinter window to configure all patcher settings visually,
then saves the result back to patcher_config.json.
"""

from __future__ import annotations

import io
import json
import re
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path

from config import (
    PATCH_TARGETS, load_config, save_config, DEFAULT_CONFIG, CONFIG_FILE,
    DEFAULT_THEME_REL, MODS_BASE_REL,
)
from main import run_patch, run_restore

# ---------------------------------------------------------------------------
# Label mapping: target key -> English display name
# ---------------------------------------------------------------------------

TARGET_LABELS = {
    "inventory": "Inventory",
    "mods_panel": "Mods Panel",
    "encounter_frame": "Encounter Counter Frame",
    "encounter_history_scroll": "Shiny History Scrollpane",
    "encounter_summary_scroll": "Encounter Summary Scrollpane",
}

PARAM_LABELS = {
    "minWidth": "Min Width",
    "minHeight": "Min Height",
    "maxHeight": "Max Height",
}


class ConfigEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PokeMMO UI Patcher - Configuration")
        self.resizable(False, False)

        if getattr(sys, 'frozen', False):
            self.config_path = Path(sys.executable).parent / CONFIG_FILE
        else:
            self.config_path = Path(__file__).parent / CONFIG_FILE
        self.config_data = load_config(self.config_path)

        self._build_ui()
        self._center_window()

    # -------------------------------------------------------------------
    # UI construction
    # -------------------------------------------------------------------

    def _build_ui(self):
        main = ttk.Frame(self, padding=15)
        main.pack(fill="both", expand=True)

        # --- Game path ---
        path_frame = ttk.LabelFrame(main, text="Game Path", padding=8)
        path_frame.pack(fill="x", pady=(0, 10))

        self.game_path_var = tk.StringVar(value=self.config_data.get("game_path", ""))
        entry = ttk.Entry(path_frame, textvariable=self.game_path_var, width=55)
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        ttk.Button(path_frame, text="Browse...", command=self._browse_path).pack(side="left")

        # --- Themes ---
        self.themes_frame = ttk.LabelFrame(main, text="Themes", padding=8)
        self.themes_frame.pack(fill="x", pady=(0, 10))

        self.theme_vars: dict[str, tk.BooleanVar] = {}
        self._build_theme_checkboxes()

        # --- Patches ---
        patches_frame = ttk.LabelFrame(main, text="Patches", padding=8)
        patches_frame.pack(fill="x", pady=(0, 10))

        self.patch_widgets: dict[str, dict] = {}
        patches_cfg = self.config_data.get("patches", {})

        for target_key, target in PATCH_TARGETS.items():
            patch_cfg = patches_cfg.get(target_key, {})
            display_name = TARGET_LABELS.get(target_key, target.label)

            row_frame = ttk.Frame(patches_frame)
            row_frame.pack(fill="x", pady=3)

            enabled_var = tk.BooleanVar(value=patch_cfg.get("enabled", True))
            cb = ttk.Checkbutton(row_frame, text=display_name, variable=enabled_var, width=30)
            cb.pack(side="left")

            param_vars: dict[str, tk.StringVar] = {}
            for param in target.params:
                plabel = PARAM_LABELS.get(param.name, param.name)
                ttk.Label(row_frame, text=f"{plabel}:").pack(side="left", padx=(10, 2))
                val = str(patch_cfg.get(param.name, param.default))
                var = tk.StringVar(value=val)
                sp = ttk.Spinbox(row_frame, textvariable=var, from_=0, to=9999, width=6)
                sp.pack(side="left")
                param_vars[param.name] = var

            self.patch_widgets[target_key] = {
                "enabled": enabled_var,
                "params": param_vars,
            }

        # --- Actions ---
        actions_frame = ttk.LabelFrame(main, text="Actions", padding=8)
        actions_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(actions_frame, text="\u25b6  Apply Patches", command=self._run_patcher).pack(
            side="left", padx=(0, 10))
        ttk.Button(actions_frame, text="\u21a9  Restore Game Defaults", command=self._run_restore).pack(
            side="left")

        # --- Buttons ---
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x", pady=(5, 0))

        ttk.Button(btn_frame, text="Reset Form", command=self._reset_defaults).pack(side="left")
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(side="right", padx=(5, 0))
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side="right")

    # -------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------

    def _center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _browse_path(self):
        folder = filedialog.askdirectory(title="Select PokeMMO installation folder")
        if folder:
            self.game_path_var.set(folder)
            self._build_theme_checkboxes()

    # -------------------------------------------------------------------
    # Theme detection
    # -------------------------------------------------------------------

    def _detect_themes(self) -> list[str]:
        """Scan the game directory for available themes."""
        game_path = Path(self.game_path_var.get().strip())
        themes = []

        # "default" always available if the base theme dir exists
        default_dir = game_path / DEFAULT_THEME_REL
        if default_dir.is_dir():
            themes.append("default")

        # Scan data/mods/ for custom themes (folders containing a subfolder with theme.xml)
        mods_dir = game_path / MODS_BASE_REL
        if mods_dir.is_dir():
            for mod in sorted(mods_dir.iterdir()):
                if not mod.is_dir():
                    continue
                for sub in mod.iterdir():
                    if sub.is_dir() and (sub / "theme.xml").exists():
                        themes.append(mod.name)
                        break

        return themes

    def _build_theme_checkboxes(self):
        """Rebuild theme checkboxes based on detected themes."""
        for widget in self.themes_frame.winfo_children():
            widget.destroy()

        selected = set(self.config_data.get("themes", ["default"]))
        detected = self._detect_themes()

        # Merge: show detected themes + any previously selected that weren't detected
        all_themes = list(dict.fromkeys(detected + sorted(selected)))

        if not all_themes:
            ttk.Label(self.themes_frame, text="No themes found. Set the correct game path above.").pack(anchor="w")
            self.theme_vars = {}
            return

        self.theme_vars = {}
        row = ttk.Frame(self.themes_frame)
        row.pack(fill="x")

        for i, name in enumerate(all_themes):
            var = tk.BooleanVar(value=(name in selected))
            label = name
            if name not in detected:
                label = f"{name} (not found)"
            cb = ttk.Checkbutton(row, text=label, variable=var)
            cb.grid(row=i // 3, column=i % 3, sticky="w", padx=(0, 15), pady=1)
            self.theme_vars[name] = var

        btn_row = ttk.Frame(self.themes_frame)
        btn_row.pack(fill="x", pady=(5, 0))
        ttk.Button(btn_row, text="Refresh", command=self._build_theme_checkboxes).pack(side="left")

    def _reset_defaults(self):
        if not messagebox.askyesno("Reset", "Reset all values to defaults?"):
            return

        self.game_path_var.set(DEFAULT_CONFIG["game_path"])
        self.config_data["themes"] = DEFAULT_CONFIG["themes"]
        self._build_theme_checkboxes()

        for target_key, widgets in self.patch_widgets.items():
            default_patch = DEFAULT_CONFIG["patches"].get(target_key, {})
            widgets["enabled"].set(default_patch.get("enabled", True))
            target = PATCH_TARGETS[target_key]
            for param in target.params:
                val = str(default_patch.get(param.name, param.default))
                widgets["params"][param.name].set(val)

    def _save(self):
        config = {
            "game_path": self.game_path_var.get().strip(),
            "themes": [name for name, var in self.theme_vars.items() if var.get()],
            "patches": {},
        }

        for target_key, widgets in self.patch_widgets.items():
            patch = {"enabled": widgets["enabled"].get()}
            for pname, var in widgets["params"].items():
                raw = var.get().strip()
                try:
                    patch[pname] = int(raw)
                except ValueError:
                    messagebox.showerror(
                        "Invalid value",
                        f"'{raw}' is not a valid integer for {pname} in {TARGET_LABELS.get(target_key, target_key)}.",
                    )
                    return
            config["patches"][target_key] = patch

        save_config(config, self.config_path)
        self.config_data = config
        messagebox.showinfo("Saved", "Configuration saved successfully.")


    # -------------------------------------------------------------------
    # Patcher actions
    # -------------------------------------------------------------------

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Remove ANSI escape sequences from text."""
        return re.sub(r'\033\[[0-9;]*m', '', text)

    def _collect_config(self) -> dict | None:
        """Build config dict from current form values; returns None on error."""
        config = {
            "game_path": self.game_path_var.get().strip(),
            "themes": [name for name, var in self.theme_vars.items() if var.get()],
            "patches": {},
        }
        for target_key, widgets in self.patch_widgets.items():
            patch = {"enabled": widgets["enabled"].get()}
            for pname, var in widgets["params"].items():
                raw = var.get().strip()
                try:
                    patch[pname] = int(raw)
                except ValueError:
                    messagebox.showerror(
                        "Invalid value",
                        f"'{raw}' is not a valid integer for {pname} "
                        f"in {TARGET_LABELS.get(target_key, target_key)}.",
                    )
                    return None
            config["patches"][target_key] = patch
        return config

    def _run_operation(self, title: str, func):
        """Save config, run func(config), and display captured output."""
        config = self._collect_config()
        if config is None:
            return

        # Save config to disk first
        save_config(config, self.config_path)
        self.config_data = config

        # Capture stdout
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        try:
            func(config)
        finally:
            sys.stdout = old_stdout

        output = self._strip_ansi(buf.getvalue())
        self._show_output(title, output)

    def _run_patcher(self):
        self._run_operation("Apply Patches", run_patch)

    def _run_restore(self):
        if not messagebox.askyesno("Confirm", "Restore all patched values to the game's original defaults?"):
            return
        self._run_operation("Restore Defaults", run_restore)

    def _show_output(self, title: str, text: str):
        """Show operation output in a popup window."""
        win = tk.Toplevel(self)
        win.title(title)
        win.resizable(True, True)
        win.geometry("620x400")

        st = scrolledtext.ScrolledText(win, wrap="word", font=("Consolas", 10))
        st.pack(fill="both", expand=True, padx=8, pady=8)
        st.insert("1.0", text)
        st.configure(state="disabled")

        ttk.Button(win, text="Close", command=win.destroy).pack(pady=(0, 8))

        # Center on parent
        win.transient(self)
        win.grab_set()
        win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - win.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")


def main():
    app = ConfigEditor()
    app.mainloop()


if __name__ == "__main__":
    main()
