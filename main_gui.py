import tkinter as tk
import customtkinter as ctk
import os
import json
import threading
import selector
import cv2
import glob
from src.bot_main import ShinyBot
from src.vision import PokéObserver

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Palabras clave de Python para highlighting básico en Brain Viewer
PY_KEYWORDS = [
    "def", "class", "import", "from", "return", "if", "elif", "else",
    "for", "while", "try", "except", "finally", "with", "as", "in",
    "not", "and", "or", "True", "False", "None", "self", "raise", "break",
    "continue", "pass", "yield", "lambda", "global", "nonlocal", "assert",
]


class ShinyHunterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇦🇷 SØREN - Shiny Hunter Bot v7.0")
        self.geometry("720x760")
        self.minsize(680, 600)
        self.attributes("-topmost", True)

        self.bot = None
        self.logger_expanded = True
        self._stats_update_id = None

        # --- MAIN LAYOUT: 5 rows ---
        # Row 0: Start button (fixed)
        # Row 1: Config frame (fixed)
        # Row 2: Tabs (weight 1 - flexible)
        # Row 3: Stats bar (fixed)
        # Row 4: Logger panel (weight 2 - flexible, collapsible)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)   # Solo las tabs crecen con la ventana
        self.grid_rowconfigure(4, weight=0)   # Logger: altura fija, no crece

        # =========================================================
        # 0. START BUTTON
        # =========================================================
        self.start_btn = ctk.CTkButton(
            self, text="START AUTOMATED HUNT", height=60,
            fg_color="#28a745", hover_color="#218838",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.toggle_bot
        )
        self.start_btn.grid(row=0, column=0, padx=15, pady=(15, 8), sticky="ew")

        # =========================================================
        # 1. CONFIG FRAME (Mode + Encounters)
        # =========================================================
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=1, column=0, padx=15, pady=4, sticky="ew")

        ctk.CTkLabel(self.config_frame, text="Mode:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=8, sticky="w")
        self.mode_switch = ctk.CTkSegmentedButton(
            self.config_frame, values=["Horda", "Single", "Ditto"],
            command=self._on_mode_change
        )
        self.mode_switch.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        self.mode_switch.set(self.get_config_val("mode", "horda").capitalize())

        ctk.CTkLabel(self.config_frame, text="Encounters:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=2, padx=10, pady=8, sticky="w")
        self.count_entry = ctk.CTkEntry(self.config_frame, width=70)
        self.count_entry.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        self.count_entry.insert(0, self.get_config_val("total_encounters", "0"))

        # =========================================================
        # 2. TABS (General, Horde, Ditto, Brain, Calibration)
        # =========================================================
        self.tabview = ctk.CTkTabview(self, height=300)
        self.tabview.grid(row=2, column=0, padx=15, pady=4, sticky="nsew")

        self.tab_general = self.tabview.add("⚙️ General")
        self.tab_horde = self.tabview.add("🏹 Horde")
        self.tab_ditto = self.tabview.add("👾 Ditto")
        self.tab_brain = self.tabview.add("🧠 Brain")
        self.tab_calib = self.tabview.add("🔧 Calib")

        self._build_general_tab()
        self._build_horde_tab()
        self._build_ditto_tab()
        self._build_brain_tab()
        self._build_calib_tab()

        # =========================================================
        # 3. STATS BAR (siempre visible)
        # =========================================================
        self.stats_frame = ctk.CTkFrame(self, height=30, fg_color="#1a1a2e")
        self.stats_frame.grid(row=3, column=0, padx=15, pady=2, sticky="ew")
        self.stats_frame.grid_columnconfigure(0, weight=1)

        self.stats_label = ctk.CTkLabel(
            self.stats_frame,
            text="Enc: 0 | Session: 0 | Dittos: 0 | ⏱️ 00:00:00",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#7f8c8d"
        )
        self.stats_label.grid(row=0, column=0, padx=10, pady=3, sticky="w")

        # =========================================================
        # 4. LOGGER PANEL (siempre visible, colapsable)
        # =========================================================
        self.logger_panel = ctk.CTkFrame(self)
        self.logger_panel.grid(row=4, column=0, padx=15, pady=(2, 10), sticky="ew")
        self.logger_panel.grid_columnconfigure(0, weight=1)

        # Logger toolbar
        toolbar = ctk.CTkFrame(self.logger_panel, height=32, fg_color="transparent")
        toolbar.grid(row=0, column=0, padx=5, pady=(4, 0), sticky="ew")
        toolbar.grid_columnconfigure(1, weight=1)

        self.toggle_log_btn = ctk.CTkButton(
            toolbar, text="▼ LOGGER", width=100, height=26,
            fg_color="#2c3e50", hover_color="#34495e",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.toggle_logger
        )
        self.toggle_log_btn.grid(row=0, column=0, padx=2, sticky="w")

        # Verbosity filter
        self.verbosity_switch = ctk.CTkSegmentedButton(
            toolbar, values=["Quiet", "Normal", "Debug"],
            command=self._on_verbosity_change,
            font=ctk.CTkFont(size=10)
        )
        self.verbosity_switch.set("Normal")
        self.verbosity_switch.grid(row=0, column=1, padx=8, sticky="w")

        # Auto-scroll toggle
        self.auto_scroll_var = ctk.BooleanVar(value=True)
        self.auto_scroll_check = ctk.CTkCheckBox(
            toolbar, text="Auto-scroll", variable=self.auto_scroll_var,
            font=ctk.CTkFont(size=10), width=20, height=20,
            checkbox_width=16, checkbox_height=16
        )
        self.auto_scroll_check.grid(row=0, column=2, padx=4)

        # Clear button
        ctk.CTkButton(
            toolbar, text="🗑️", width=30, height=26,
            fg_color="#5a2d2d", hover_color="#7a3d3d",
            command=self.clear_logs
        ).grid(row=0, column=3, padx=2)

        # Copy button
        ctk.CTkButton(
            toolbar, text="📋", width=30, height=26,
            fg_color="#2c3e50", hover_color="#34495e",
            command=self.copy_logs
        ).grid(row=0, column=4, padx=2)

        # Log textbox — altura fija 150px, scroll interno nativo de CTkTextbox
        self.log_box = ctk.CTkTextbox(
            self.logger_panel,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0d1117",
            wrap="word",
            height=150
        )
        self.log_box.grid(row=1, column=0, padx=5, pady=(2, 5), sticky="ew")

        # Collapsed status line (hidden by default)
        self.collapsed_label = ctk.CTkLabel(
            self.logger_panel,
            text="...",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#546E7A",
            anchor="w"
        )

        # Configure color tags on the log_box
        self._setup_log_tags()

        # Insertar mensaje de bienvenida
        self.add_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "PHASE")
        self.add_log("   SØREN v7.0 — Shiny Hunter Bot", "HEADER")
        self.add_log("   Logger con colores • Brain Viewer", "HEADER")
        self.add_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "PHASE")

    # =================================================================
    # TAB BUILDERS
    # =================================================================

    def _build_general_tab(self):
        tab = self.tab_general
        ctk.CTkLabel(tab, text="Webhook URL:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        self.web_entry = ctk.CTkEntry(tab, placeholder_text="Discord URL", width=350)
        self.web_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.web_entry.insert(0, self.get_config_val("discord_webhook"))

        ctk.CTkLabel(tab, text="OCR Retries:", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        self.ocr_entry = ctk.CTkEntry(tab, width=70)
        self.ocr_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ocr_entry.insert(0, self.get_config_val("ocr_retries", "6"))

        ctk.CTkButton(tab, text="SAVE GENERAL CONFIG", fg_color="#1f538d",
                       height=36, command=self.save_all).grid(
            row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def _build_horde_tab(self):
        tab = self.tab_horde
        ctk.CTkLabel(tab, text="Horde Size:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.horde_size_switch = ctk.CTkSegmentedButton(
            tab, values=["3", "5"], command=self.save_all)
        self.horde_size_switch.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.horde_size_switch.set(self.get_config_val("horde_size", "5"))

        # ZORUA CONFIG
        self.mode_zorua_check = ctk.CTkCheckBox(tab, text="Modo Zorua", font=ctk.CTkFont(weight="bold"))
        self.mode_zorua_check.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        if self.get_config_val("mode_zorua", "False") == "True":
            self.mode_zorua_check.select()

        ctk.CTkLabel(tab, text="Zorua Wait (s):", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=1, padx=10, pady=5, sticky="e")
        self.zorua_wait_entry = ctk.CTkEntry(tab, width=60)
        self.zorua_wait_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.zorua_wait_entry.insert(0, self.get_config_val("zorua_wait", "3.0"))

        ctk.CTkButton(tab, text="SAVE HORDE CONFIG", fg_color="#1f538d",
                       height=36, command=self.save_all).grid(
            row=2, column=0, columnspan=3, padx=20, pady=8, sticky="ew")

        ctk.CTkLabel(tab, text="Alarm Testing:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=10, pady=8, sticky="w")
        row_alarm = ctk.CTkFrame(tab, fg_color="transparent")
        row_alarm.grid(row=3, column=1, columnspan=2, padx=10, pady=8, sticky="w")
        ctk.CTkButton(row_alarm, text="TEST ALARM", width=100,
                       fg_color="#d35400", hover_color="#e67e22",
                       command=self.test_alarm).pack(side="left", padx=5)
        ctk.CTkButton(row_alarm, text="STOP ALARM", width=100,
                       fg_color="#7f8c8d",
                       command=self.stop_alarm).pack(side="left", padx=5)

    def _build_ditto_tab(self):
        tab = self.tab_ditto
        # Patrol Time
        ctk.CTkLabel(tab, text="Patrol Time (s):", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=10, pady=4, sticky="w")
        self.ditto_path_entry = ctk.CTkEntry(tab, width=60)
        self.ditto_path_entry.grid(row=0, column=1, padx=10, pady=4, sticky="w")
        self.ditto_path_entry.insert(0, self.get_config_val("ditto_patrol_time", "2.5"))

        # Attack (Swipe)
        ctk.CTkLabel(tab, text="1. Attack (Key/Name):", font=ctk.CTkFont(weight="bold")).grid(
            row=1, column=0, padx=10, pady=4, sticky="w")
        self.ditto_atk_entry = ctk.CTkEntry(tab, width=40)
        self.ditto_atk_entry.grid(row=1, column=1, padx=10, pady=4, sticky="w")
        self.ditto_atk_entry.insert(0, self.get_config_val("ditto_key_attack", "2"))
        self.ditto_atk_name = ctk.CTkEntry(tab, width=120)
        self.ditto_atk_name.grid(row=1, column=2, padx=10, pady=4, sticky="w")
        self.ditto_atk_name.insert(0, self.get_config_val("ditto_name_attack", "False Swipe"))

        # Sleep (Spora)
        ctk.CTkLabel(tab, text="2. Sleep (Key/Name):", font=ctk.CTkFont(weight="bold")).grid(
            row=2, column=0, padx=10, pady=4, sticky="w")
        self.ditto_slp_entry = ctk.CTkEntry(tab, width=40)
        self.ditto_slp_entry.grid(row=2, column=1, padx=10, pady=4, sticky="w")
        self.ditto_slp_entry.insert(0, self.get_config_val("ditto_key_sleep", "1"))
        self.ditto_slp_name = ctk.CTkEntry(tab, width=120)
        self.ditto_slp_name.grid(row=2, column=2, padx=10, pady=4, sticky="w")
        self.ditto_slp_name.insert(0, self.get_config_val("ditto_name_sleep", "Spore"))

        # Balls & Utils
        ctk.CTkLabel(tab, text="3. Ball Hotkey:", font=ctk.CTkFont(weight="bold")).grid(
            row=3, column=0, padx=10, pady=4, sticky="w")
        self.ditto_ball_entry = ctk.CTkEntry(tab, width=50)
        self.ditto_ball_entry.grid(row=3, column=1, padx=10, pady=4, sticky="w")
        self.ditto_ball_entry.insert(0, self.get_config_val("ditto_key_ball", "5"))

        ctk.CTkLabel(tab, text="Potion Key:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=0, padx=10, pady=4, sticky="w")
        self.potion_key_entry = ctk.CTkEntry(tab, width=50)
        self.potion_key_entry.grid(row=4, column=1, padx=10, pady=4, sticky="w")
        self.potion_key_entry.insert(0, self.get_config_val("ditto_key_potion", "6"))

        ctk.CTkLabel(tab, text="Leppa Key:", font=ctk.CTkFont(weight="bold")).grid(
            row=4, column=2, padx=10, pady=4, sticky="w")
        self.leppa_key_entry = ctk.CTkEntry(tab, width=50)
        self.leppa_key_entry.grid(row=4, column=3, padx=10, pady=4, sticky="w")
        self.leppa_key_entry.insert(0, self.get_config_val("ditto_key_leppa", "4"))

        # Checkpoints de Curación
        self.heal_hp_check = ctk.CTkCheckBox(tab, text="Auto-Heal HP", font=ctk.CTkFont(weight="bold"))
        self.heal_hp_check.grid(row=5, column=0, padx=10, pady=4, sticky="w")
        if self.get_config_val("auto_heal_hp", "True") == "True":
            self.heal_hp_check.select()

        self.heal_pp_check = ctk.CTkCheckBox(tab, text="Auto-Restore PP", font=ctk.CTkFont(weight="bold"))
        self.heal_pp_check.grid(row=5, column=2, padx=10, pady=4, sticky="w")
        if self.get_config_val("auto_heal_pp", "True") == "True":
            self.heal_pp_check.select()

        # ── Sección de Timings ──────────────────────────────────────────
        timing_frame = ctk.CTkFrame(tab, fg_color="#1a1a2e")
        timing_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=(8, 4), sticky="ew")

        ctk.CTkLabel(timing_frame, text="⏱️  Timings de Captura",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      text_color="#FFCB6B").grid(
            row=0, column=0, columnspan=4, padx=10, pady=(6, 2), sticky="w")

        # Row 1: Ball Wait | Capture Settle
        ctk.CTkLabel(timing_frame, text="OCR Wait (s):", font=ctk.CTkFont(size=11)).grid(
            row=1, column=0, padx=10, pady=3, sticky="w")
        self.timing_ball_wait_entry = ctk.CTkEntry(timing_frame, width=55)
        self.timing_ball_wait_entry.grid(row=1, column=1, padx=5, pady=3, sticky="w")
        self.timing_ball_wait_entry.insert(0, self.get_config_val("timing_ball_wait", "0.5"))

        ctk.CTkLabel(timing_frame, text="Settle (s):", font=ctk.CTkFont(size=11)).grid(
            row=1, column=2, padx=10, pady=3, sticky="w")
        self.timing_settle_entry = ctk.CTkEntry(timing_frame, width=55)
        self.timing_settle_entry.grid(row=1, column=3, padx=5, pady=3, sticky="w")
        self.timing_settle_entry.insert(0, self.get_config_val("timing_capture_settle", "2.5"))

        # Row 2: Leppa Wait | Ball Press
        ctk.CTkLabel(timing_frame, text="Leppa Pre-Wait (s):", font=ctk.CTkFont(size=11)).grid(
            row=2, column=0, padx=10, pady=3, sticky="w")
        self.timing_leppa_wait_entry = ctk.CTkEntry(timing_frame, width=55)
        self.timing_leppa_wait_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")
        self.timing_leppa_wait_entry.insert(0, self.get_config_val("timing_leppa_wait", "1.5"))

        ctk.CTkLabel(timing_frame, text="Ball Press Delay (s):", font=ctk.CTkFont(size=11)).grid(
            row=2, column=2, padx=10, pady=3, sticky="w")
        self.timing_ball_press_entry = ctk.CTkEntry(timing_frame, width=55)
        self.timing_ball_press_entry.grid(row=2, column=3, padx=5, pady=(3, 6), sticky="w")
        self.timing_ball_press_entry.insert(0, self.get_config_val("timing_ball_press_wait", "0.7"))
        # ────────────────────────────────────────────────────────────────

        ctk.CTkButton(tab, text="SAVE DITTO CONFIG", fg_color="#1f538d",
                       height=36, command=self.save_all).grid(
            row=7, column=0, columnspan=4, padx=20, pady=8, sticky="ew")

    def _build_brain_tab(self):
        """Pestaña Brain Viewer — muestra el código Python del modo activo"""
        tab = self.tab_brain
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Toolbar
        brain_toolbar = ctk.CTkFrame(tab, fg_color="transparent")
        brain_toolbar.grid(row=0, column=0, padx=5, pady=4, sticky="ew")

        ctk.CTkLabel(brain_toolbar, text="Archivo:", font=ctk.CTkFont(weight="bold")).pack(
            side="left", padx=5)

        self.brain_file_var = ctk.StringVar(value="(auto: modo activo)")
        self.brain_dropdown = ctk.CTkOptionMenu(
            brain_toolbar,
            values=self._get_source_files(),
            variable=self.brain_file_var,
            command=self._on_brain_file_change,
            width=250
        )
        self.brain_dropdown.pack(side="left", padx=5)

        ctk.CTkButton(
            brain_toolbar, text="🔄", width=30, height=28,
            fg_color="#2c3e50", hover_color="#34495e",
            command=self._refresh_brain
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            brain_toolbar, text="📋 Copiar", width=70, height=28,
            fg_color="#2c3e50", hover_color="#34495e",
            command=self._copy_brain_code
        ).pack(side="right", padx=5)

        # Code viewer
        self.brain_textbox = ctk.CTkTextbox(
            tab,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#0d1117",
            wrap="none",
            state="disabled"
        )
        self.brain_textbox.grid(row=1, column=0, padx=5, pady=(2, 5), sticky="nsew")

        # Setup syntax highlighting tags
        self.brain_textbox.tag_config("keyword", foreground="#C792EA")
        self.brain_textbox.tag_config("string", foreground="#C3E88D")
        self.brain_textbox.tag_config("comment", foreground="#546E7A")
        self.brain_textbox.tag_config("decorator", foreground="#FFCB6B")
        self.brain_textbox.tag_config("number", foreground="#F78C6C")
        self.brain_textbox.tag_config("lineno", foreground="#3d4f5f")

        # Load initial file
        self._refresh_brain()

    def _build_calib_tab(self):
        """Pestaña de calibración — herramientas de visión"""
        tab = self.tab_calib
        ctk.CTkLabel(tab, text="CALIBRATION TOOLS",
                      font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=0, column=0, columnspan=3, pady=6)

        buttons = [
            ("HUD HORDE", "hud", "#5a5a5a"),
            ("SINGLE SLOT", "single_slot", "#5a5a5a"),
            ("RUN BTN", "combat", "#5a5a5a"),
            ("HP BAR", "hp_bar", "#8d1f1f"),
            ("STATUS", "status_slot", "#1f8d8d"),
            ("SLEEP ICON", "sleep_icon", "#8d8d1f"),
            ("PP SLOTS", "pp_slots", "#5a1f8d"),
            ("BATTLE MSG", "battle_msg", "#1f8d5a"),
            ("MY HP", "hunter_hp", "#8d1f5a"),
        ]
        for i, (text, mode, color) in enumerate(buttons):
            r = 1 + (i // 3)
            c = i % 3
            ctk.CTkButton(
                tab, text=text, width=80, fg_color=color,
                command=lambda m=mode: self.run_calib(m)
            ).grid(row=r, column=c, padx=3, pady=3, sticky="ew")

        # Debug frame button
        ctk.CTkButton(
            tab, text="📸 DEBUG FRAME", width=80, fg_color="#2c3e50",
            command=self.save_debug
        ).grid(row=4, column=0, columnspan=3, padx=20, pady=8, sticky="ew")

    # =================================================================
    # BRAIN VIEWER LOGIC
    # =================================================================

    def _get_source_files(self):
        """Retorna la lista de archivos .py del proyecto"""
        src_files = []
        base = os.path.dirname(os.path.abspath(__file__))
        patterns = [
            os.path.join(base, "src", "*.py"),
            os.path.join(base, "src", "modes", "*.py"),
            os.path.join(base, "*.py"),
        ]
        for pat in patterns:
            for f in sorted(glob.glob(pat)):
                rel = os.path.relpath(f, base)
                src_files.append(rel)
        return src_files if src_files else ["(no files found)"]

    def _get_active_mode_file(self):
        """Retorna el path relativo del archivo del modo activo"""
        mode = self.mode_switch.get().lower()
        mode_map = {
            "horda": os.path.join("src", "modes", "horda.py"),
            "single": os.path.join("src", "modes", "single.py"),
            "ditto": os.path.join("src", "modes", "ditto.py"),
        }
        return mode_map.get(mode, os.path.join("src", "modes", "base.py"))

    def _on_brain_file_change(self, choice):
        self._load_brain_file(choice)

    def _refresh_brain(self):
        """Carga el archivo del modo activo o el seleccionado"""
        current = self.brain_file_var.get()
        if current.startswith("(auto") or current == "(no files found)":
            target = self._get_active_mode_file()
            self.brain_file_var.set(target)
        else:
            target = current
        self._load_brain_file(target)

    def _load_brain_file(self, rel_path):
        """Carga un archivo Python en el Brain Viewer con syntax highlighting"""
        base = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base, rel_path)

        self.brain_textbox.configure(state="normal")
        self.brain_textbox.delete("1.0", "end")

        if not os.path.exists(full_path):
            self.brain_textbox.insert("end", f"# File not found: {rel_path}\n")
            self.brain_textbox.configure(state="disabled")
            return

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                # Line number
                lineno_str = f"{i:4d} │ "
                self.brain_textbox.insert("end", lineno_str, "lineno")

                # Basic syntax highlighting
                stripped = line.rstrip("\r\n")
                self._insert_highlighted_line(stripped)
                self.brain_textbox.insert("end", "\n")

        except Exception as e:
            self.brain_textbox.insert("end", f"# Error reading file: {e}\n")

        self.brain_textbox.configure(state="disabled")

    def _insert_highlighted_line(self, line):
        """Inserta una línea con syntax highlighting básico"""
        stripped = line.lstrip()

        # Comment lines
        if stripped.startswith("#"):
            self.brain_textbox.insert("end", line, "comment")
            return

        # Decorator lines
        if stripped.startswith("@"):
            self.brain_textbox.insert("end", line, "decorator")
            return

        # For lines with content, do word-by-word highlighting
        # Simple approach: just check for keywords at word boundaries
        i = 0
        while i < len(line):
            # Check if we're at the start of a keyword
            found_kw = False
            if line[i].isalpha() or line[i] == '_':
                for kw in PY_KEYWORDS:
                    end = i + len(kw)
                    if line[i:end] == kw:
                        # Check word boundary
                        before_ok = (i == 0 or not (line[i-1].isalnum() or line[i-1] == '_'))
                        after_ok = (end >= len(line) or not (line[end].isalnum() or line[end] == '_'))
                        if before_ok and after_ok:
                            self.brain_textbox.insert("end", kw, "keyword")
                            i = end
                            found_kw = True
                            break

            if not found_kw:
                # Check for strings
                if line[i] in ('"', "'"):
                    quote = line[i]
                    # Check for triple quotes
                    if line[i:i+3] in ('"""', "'''"):
                        end = line.find(line[i:i+3], i+3)
                        if end == -1:
                            self.brain_textbox.insert("end", line[i:], "string")
                            return
                        end += 3
                        self.brain_textbox.insert("end", line[i:end], "string")
                        i = end
                    else:
                        end = line.find(quote, i+1)
                        if end == -1:
                            self.brain_textbox.insert("end", line[i:], "string")
                            return
                        end += 1
                        self.brain_textbox.insert("end", line[i:end], "string")
                        i = end
                # Check for inline comments
                elif line[i] == '#':
                    self.brain_textbox.insert("end", line[i:], "comment")
                    return
                # Check for numbers
                elif line[i].isdigit() and (i == 0 or not (line[i-1].isalnum() or line[i-1] == '_')):
                    j = i
                    while j < len(line) and (line[j].isdigit() or line[j] == '.'):
                        j += 1
                    self.brain_textbox.insert("end", line[i:j], "number")
                    i = j
                else:
                    self.brain_textbox.insert("end", line[i])
                    i += 1

    def _copy_brain_code(self):
        """Copia el código del Brain Viewer al clipboard"""
        try:
            content = self.brain_textbox.get("1.0", "end-1c")
            # Remover los line numbers
            lines = content.split("\n")
            clean = []
            for l in lines:
                if "│" in l:
                    clean.append(l.split("│", 1)[1] if "│" in l else l)
                else:
                    clean.append(l)
            self.clipboard_clear()
            self.clipboard_append("\n".join(clean))
            self.add_log("📋 Código copiado al portapapeles.", "SUCCESS")
        except Exception as e:
            self.add_log(f"❌ Error al copiar: {e}", "FATAL")

    # =================================================================
    # LOGGER METHODS
    # =================================================================

    def _setup_log_tags(self):
        """Configura tags de color para el CTkTextbox del logger"""
        tag_colors = {
            "INFO":    {"foreground": "#82AAFF"},
            "ACTION":  {"foreground": "#89DDFF"},
            "SUCCESS": {"foreground": "#C3E88D"},
            "WARN":    {"foreground": "#FFCB6B"},
            "FATAL":   {"foreground": "#FF5370"},
            "BATTLE":  {"foreground": "#C792EA"},
            "MAP":     {"foreground": "#B2CCD6"},
            "HEAL":    {"foreground": "#A5D6A7"},
            "DEBUG":   {"foreground": "#546E7A"},
            "HEADER":  {"foreground": "#F78C6C"},
            "PHASE":   {"foreground": "#FFCB6B"},
            "BRAIN":   {"foreground": "#82AAFF"},
        }
        for tag, config in tag_colors.items():
            try:
                self.log_box.tag_config(tag, **config)
            except Exception:
                pass  # Some tag_config params may not apply

    def add_log(self, msg, category="INFO"):
        """Agrega un mensaje al logger con color por categoría"""
        # Verbosity filtering
        verbosity = self.verbosity_switch.get() if hasattr(self, 'verbosity_switch') else "Normal"
        if verbosity == "Quiet" and category not in ("SUCCESS", "FATAL", "PHASE", "HEADER"):
            return
        if verbosity == "Normal" and category == "DEBUG":
            return

        self.log_box.insert("end", f"{msg}\n", category)

        # Auto-scroll
        if hasattr(self, 'auto_scroll_var') and self.auto_scroll_var.get():
            self.log_box.see("end")

        # Buffer circular: máximo 2000 líneas
        self._trim_log_buffer()

        # Actualizar collapsed label
        if hasattr(self, 'collapsed_label'):
            short = msg[:80] + "..." if len(msg) > 80 else msg
            self.collapsed_label.configure(text=short)

    def _trim_log_buffer(self, max_lines=2000):
        """Elimina líneas viejas si excede el máximo"""
        try:
            content = self.log_box.get("1.0", "end-1c")
            lines = content.split("\n")
            if len(lines) > max_lines:
                excess = len(lines) - max_lines
                self.log_box.delete("1.0", f"{excess + 1}.0")
        except Exception:
            pass

    def toggle_logger(self):
        """Colapsa o expande el panel del logger"""
        if self.logger_expanded:
            # Colapsar: ocultar textbox, mostrar label de 1 línea
            self.log_box.grid_remove()
            self.collapsed_label.grid(row=1, column=0, padx=10, pady=2, sticky="ew")
            self.toggle_log_btn.configure(text="▶ LOGGER")
            self.grid_rowconfigure(4, weight=0)
            self.logger_expanded = False
        else:
            # Expandir: mostrar textbox, ocultar label
            self.collapsed_label.grid_remove()
            self.log_box.grid(row=1, column=0, padx=5, pady=(2, 5), sticky="nsew")
            self.toggle_log_btn.configure(text="▼ LOGGER")
            self.grid_rowconfigure(4, weight=2)
            self.logger_expanded = True

    def clear_logs(self):
        """Limpia todo el contenido del logger"""
        self.log_box.delete("1.0", "end")
        self.add_log("🗑️ Logs limpiados.", "INFO")

    def copy_logs(self):
        """Copia las últimas 10 líneas del log"""
        try:
            content = self.log_box.get("1.0", "end-1c")
            lines = [l for l in content.split("\n") if l.strip()]
            last_10 = "\n".join(lines[-10:])
            if last_10:
                self.clipboard_clear()
                self.clipboard_append(last_10)
                self.add_log("📋 Últimas 10 líneas copiadas.", "SUCCESS")
            else:
                self.add_log("⚠️ No hay logs para copiar.", "WARN")
        except Exception:
            self.add_log("⚠️ Error al copiar logs.", "WARN")

    # =================================================================
    # STATS BAR
    # =================================================================

    def _update_stats(self):
        """Actualiza la barra de stats cada segundo"""
        try:
            if self.bot and self.bot.running:
                enc = self.bot.encounters
                sess = self.bot.session_encounters
                dittos = self.bot.session_dittos
                elapsed = self.bot.get_elapsed_time()

                # Calculate rate
                elapsed_obj = self.bot.logger.start_time
                from datetime import datetime
                seconds = (datetime.now() - elapsed_obj).total_seconds()
                rate = (sess / (seconds / 60)) if seconds > 60 else 0

                mode = self.mode_switch.get()
                self.stats_label.configure(
                    text=f"🎯 {mode} | Enc: {enc} | Sess: {sess} | "
                         f"Dittos: {dittos} | Rate: {rate:.1f}/min | ⏱️ {elapsed}",
                    text_color="#C3E88D" if self.bot.running else "#7f8c8d"
                )
        except Exception:
            pass

        self._stats_update_id = self.after(1000, self._update_stats)

    # =================================================================
    # CONFIG / STATE
    # =================================================================

    def get_config_val(self, key, default=""):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    val = json.load(f).get(key, default)
                    return str(val)
        except Exception:
            pass
        return str(default)

    def save_all(self, _=None):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)
            else:
                config = {}

            config["mode"] = self.mode_switch.get().lower()
            config["total_encounters"] = int(self.count_entry.get())
            config["discord_webhook"] = self.web_entry.get()
            config["ocr_retries"] = int(self.ocr_entry.get())
            config["horde_size"] = int(self.horde_size_switch.get())

            # Guardar Zorua Settings
            if hasattr(self, 'mode_zorua_check'):
                config["mode_zorua"] = bool(self.mode_zorua_check.get())
                config["zorua_wait"] = float(self.zorua_wait_entry.get())

            # Ditto Settings
            config["ditto_patrol_time"] = float(self.ditto_path_entry.get())
            config["ditto_key_attack"] = self.ditto_atk_entry.get()
            config["ditto_name_attack"] = self.ditto_atk_name.get()
            config["ditto_key_sleep"] = self.ditto_slp_entry.get()
            config["ditto_name_sleep"] = self.ditto_slp_name.get()
            config["ditto_key_ball"] = self.ditto_ball_entry.get()
            config["ditto_key_potion"] = self.potion_key_entry.get()
            config["ditto_key_leppa"] = self.leppa_key_entry.get()
            config["auto_heal_hp"] = bool(self.heal_hp_check.get())
            config["auto_heal_pp"] = bool(self.heal_pp_check.get())

            # Timings de captura
            config["timing_ball_wait"]       = float(self.timing_ball_wait_entry.get())
            config["timing_capture_settle"]  = float(self.timing_settle_entry.get())
            config["timing_leppa_wait"]      = float(self.timing_leppa_wait_entry.get())
            config["timing_ball_press_wait"] = float(self.timing_ball_press_entry.get())

            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            self.add_log("✅ Configuration saved.", "SUCCESS")
        except Exception as e:
            self.add_log(f"❌ Error saving: {e}", "FATAL")

    def _on_mode_change(self, value):
        """Callback cuando cambia el modo — guarda y actualiza Brain"""
        self.save_all()
        # Actualizar Brain Viewer si está en auto
        if hasattr(self, 'brain_file_var'):
            current = self.brain_file_var.get()
            # Si el usuario no seleccionó un archivo específico, auto-cambiar
            mode_files = [
                os.path.join("src", "modes", "horda.py"),
                os.path.join("src", "modes", "single.py"),
                os.path.join("src", "modes", "ditto.py"),
                os.path.join("src", "modes", "base.py"),
            ]
            if current in mode_files or current.startswith("("):
                self._refresh_brain()

    def _on_verbosity_change(self, value):
        """Callback cuando cambia la verbosidad"""
        if self.bot and self.bot.logger:
            level_map = {"Quiet": "QUIET", "Normal": "NORMAL", "Debug": "DEBUG"}
            self.bot.logger.verbosity = level_map.get(value, "NORMAL")
        self.add_log(f"📊 Verbosity: {value}", "INFO")

    # =================================================================
    # BOT ACTIONS
    # =================================================================

    def run_calib(self, mode):
        threading.Thread(target=selector.run_calibration, args=(mode, self.add_log), daemon=True).start()

    def test_alarm(self):
        if not self.bot:
            self.bot = ShinyBot(log_widget=self.log_box)
        self.bot.play_shiny_alarm()
        self.add_log("🎵 Testing alarm... Check assets/shiny_alarm.wav", "ACTION")

    def stop_alarm(self):
        if self.bot:
            self.bot.stop_shiny_alarm()

    def save_debug(self):
        try:
            obs = PokéObserver()
            frame = obs.capture_frame()
            if frame is None:
                return
            cv2.imwrite("debug_view.png", frame)
            self.add_log("📸 Debug frame saved → debug_view.png", "SUCCESS")
        except Exception as e:
            self.add_log(f"❌ Debug Error: {e}", "FATAL")

    def toggle_bot(self):
        if not self.bot or not self.bot.running:
            self.save_all()
            self.bot = ShinyBot(log_widget=self.log_box)
            self.bot.start()
            self.start_btn.configure(text="⏹ STOP AUTOMATION", fg_color="#dc3545", hover_color="#c82333")
            self._update_stats()  # Arranca el loop de stats
        else:
            self.bot.stop()
            self.bot = None
            self.start_btn.configure(text="START AUTOMATED HUNT", fg_color="#28a745", hover_color="#218838")
            if self._stats_update_id:
                self.after_cancel(self._stats_update_id)
                self._stats_update_id = None
            self.stats_label.configure(
                text="Enc: 0 | Session: 0 | Dittos: 0 | ⏱️ 00:00:00",
                text_color="#7f8c8d"
            )

    def destroy(self):
        """Cleanup al cerrar la ventana"""
        if self._stats_update_id:
            self.after_cancel(self._stats_update_id)
        if self.bot:
            self.bot.stop()
        super().destroy()


if __name__ == "__main__":
    app = ShinyHunterGUI()
    app.mainloop()
