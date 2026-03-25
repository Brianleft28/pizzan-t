import tkinter as tk
import customtkinter as ctk
import os
import json
import threading
import selector
import cv2
from src.bot_main import ShinyBot
from src.vision import PokéObserver

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ShinyHunterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇦🇷 SØREN - Shiny Hunter Bot")
        self.geometry("700x950")
        self.attributes("-topmost", True)

        self.bot = None
        self.settings_visible = True

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # 0. Start Button
        self.start_btn = ctk.CTkButton(self, text="START AUTOMATED HUNT", height=70, 
                                     fg_color="#28a745", hover_color="#218838",
                                     font=ctk.CTkFont(size=20, weight="bold"),
                                     command=self.toggle_bot)
        self.start_btn.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # 1. Main Configuration Frame (Mode & Counter)
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.config_frame, text="Hunting Mode:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.mode_switch = ctk.CTkSegmentedButton(self.config_frame, values=["Horda", "Single", "Ditto"], command=self.save_all)
        self.mode_switch.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.mode_switch.set(self.get_config_val("mode", "horda").capitalize())

        ctk.CTkLabel(self.config_frame, text="Encounters:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.count_entry = ctk.CTkEntry(self.config_frame, width=70)
        self.count_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.count_entry.insert(0, self.get_config_val("total_encounters", "0"))

        # 2. Tabs
        self.tabview = ctk.CTkTabview(self, height=450)
        self.tabview.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.tab_general = self.tabview.add("General / Stats")
        self.tab_ditto = self.tabview.add("Ditto Settings")

        # --- General Tab ---
        ctk.CTkLabel(self.tab_general, text="Webhook URL:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.web_entry = ctk.CTkEntry(self.tab_general, placeholder_text="Discord URL", width=350)
        self.web_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.web_entry.insert(0, self.get_config_val("discord_webhook"))

        ctk.CTkLabel(self.tab_general, text="OCR Retries:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ocr_entry = ctk.CTkEntry(self.tab_general, width=70)
        self.ocr_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ocr_entry.insert(0, self.get_config_val("ocr_retries", "6"))

        # --- Ditto Tab (TODOS LOS PARÁMETROS) ---
        # Patrol Time
        ctk.CTkLabel(self.tab_ditto, text="Patrol Time (s):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ditto_path_entry = ctk.CTkEntry(self.tab_ditto, width=60); self.ditto_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.ditto_path_entry.insert(0, self.get_config_val("ditto_patrol_time", "2.5"))

        # Attack (Swipe)
        ctk.CTkLabel(self.tab_ditto, text="1. Attack (Key/Name):", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ditto_atk_entry = ctk.CTkEntry(self.tab_ditto, width=40); self.ditto_atk_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ditto_atk_entry.insert(0, self.get_config_val("ditto_key_attack", "2"))
        self.ditto_atk_name = ctk.CTkEntry(self.tab_ditto, width=120); self.ditto_atk_name.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.ditto_atk_name.insert(0, self.get_config_val("ditto_name_attack", "False Swipe"))

        # Soak (Anegar)
        ctk.CTkLabel(self.tab_ditto, text="2. Soak (Key/Name):", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ditto_soak_entry = ctk.CTkEntry(self.tab_ditto, width=40); self.ditto_soak_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.ditto_soak_entry.insert(0, self.get_config_val("ditto_key_soak", "4"))
        self.ditto_soak_name = ctk.CTkEntry(self.tab_ditto, width=120); self.ditto_soak_name.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.ditto_soak_name.insert(0, self.get_config_val("ditto_name_soak", "Soak"))

        # Sleep (Spora)
        ctk.CTkLabel(self.tab_ditto, text="3. Sleep (Key/Name):", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ditto_slp_entry = ctk.CTkEntry(self.tab_ditto, width=40); self.ditto_slp_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.ditto_slp_entry.insert(0, self.get_config_val("ditto_key_sleep", "1"))
        self.ditto_slp_name = ctk.CTkEntry(self.tab_ditto, width=120); self.ditto_slp_name.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.ditto_slp_name.insert(0, self.get_config_val("ditto_name_sleep", "Spore"))

        # Balls & Utils
        ctk.CTkLabel(self.tab_ditto, text="4. Ball Hotkey:", font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.ditto_ball_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.ditto_ball_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.ditto_ball_entry.insert(0, self.get_config_val("ditto_key_ball", "5"))

        ctk.CTkLabel(self.tab_ditto, text="Potion Key:", font=ctk.CTkFont(weight="bold")).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.potion_key_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.potion_key_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.potion_key_entry.insert(0, self.get_config_val("ditto_key_potion", "6"))

        ctk.CTkLabel(self.tab_ditto, text="Leppa Key:", font=ctk.CTkFont(weight="bold")).grid(row=5, column=2, padx=10, pady=5, sticky="w")
        self.leppa_key_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.leppa_key_entry.grid(row=5, column=3, padx=10, pady=5, sticky="w")
        self.leppa_key_entry.insert(0, self.get_config_val("ditto_key_leppa", "4"))

        # Checkpoints de Curación (DENTRO DE DITTO TAB)
        self.heal_hp_check = ctk.CTkCheckBox(self.tab_ditto, text="Auto-Heal HP", font=ctk.CTkFont(weight="bold"))
        self.heal_hp_check.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        if self.get_config_val("auto_heal_hp", "True") == "True": self.heal_hp_check.select()

        self.heal_pp_check = ctk.CTkCheckBox(self.tab_ditto, text="Auto-Restore PP", font=ctk.CTkFont(weight="bold"))
        self.heal_pp_check.grid(row=6, column=2, padx=10, pady=5, sticky="w")
        if self.get_config_val("auto_heal_pp", "True") == "True": self.heal_pp_check.select()

        self.save_btn_tab = ctk.CTkButton(self.tab_ditto, text="SAVE DITTO CONFIG", fg_color="#1f538d", height=40, command=self.save_all)
        self.save_btn_tab.grid(row=7, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        # 3. Calibration Frame (TODOS LOS BOTONES RESTAURADOS)
        self.calib_frame = ctk.CTkFrame(self)
        self.calib_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(self.calib_frame, text="CALIBRATION TOOLS", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        row1 = ctk.CTkFrame(self.calib_frame, fg_color="transparent"); row1.pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(row1, text="HUD HORDE", width=80, fg_color="#5a5a5a", command=lambda: self.run_calib("hud")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row1, text="SINGLE SLOT", width=80, fg_color="#5a5a5a", command=lambda: self.run_calib("single_slot")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row1, text="RUN BTN", width=80, fg_color="#5a5a5a", command=lambda: self.run_calib("combat")).pack(side="left", padx=2, expand=True, fill="x")

        row2 = ctk.CTkFrame(self.calib_frame, fg_color="transparent"); row2.pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(row2, text="HP BAR", width=80, fg_color="#8d1f1f", command=lambda: self.run_calib("hp_bar")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row2, text="STATUS", width=80, fg_color="#1f8d8d", command=lambda: self.run_calib("status_slot")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row2, text="SLEEP ICON", width=80, fg_color="#8d8d1f", command=lambda: self.run_calib("sleep_icon")).pack(side="left", padx=2, expand=True, fill="x")

        row3 = ctk.CTkFrame(self.calib_frame, fg_color="transparent"); row3.pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(row3, text="PP SLOTS", width=80, fg_color="#5a1f8d", command=lambda: self.run_calib("pp_slots")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row3, text="BATTLE MSG", width=80, fg_color="#1f8d5a", command=lambda: self.run_calib("battle_msg")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row3, text="MY HP", width=80, fg_color="#8d1f5a", command=lambda: self.run_calib("hunter_hp")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(row3, text="DEBUG FRAME", width=80, fg_color="#2c3e50", command=self.save_debug).pack(side="left", padx=2, expand=True, fill="x")

        # 4. Logger Frame
        self.log_container = ctk.CTkFrame(self)
        self.log_container.grid(row=1, column=0, rowspan=3, padx=20, pady=10, sticky="nsew")
        self.log_container.grid_columnconfigure(0, weight=1); self.log_container.grid_rowconfigure(0, weight=1)
        self.log_box = ctk.CTkTextbox(self.log_container, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.log_container.grid_remove()

        # 5. View Toggle
        self.toggle_btn = ctk.CTkButton(self, text="VIEW FULL LOGGER", height=35, fg_color="#5a5a5a", command=self.toggle_settings)
        self.toggle_btn.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

    def get_config_val(self, key, default=""):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f: return str(json.load(f).get(key, default))
        except: pass
        return default

    def save_all(self, _=None):
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f: config = json.load(f)
            else: config = {}
            config["mode"] = self.mode_switch.get().lower()
            config["total_encounters"] = int(self.count_entry.get())
            config["discord_webhook"] = self.web_entry.get()
            config["ocr_retries"] = int(self.ocr_entry.get())
            
            # Ditto Settings
            config["ditto_patrol_time"] = float(self.ditto_path_entry.get())
            config["ditto_key_attack"] = self.ditto_atk_entry.get()
            config["ditto_name_attack"] = self.ditto_atk_name.get()
            config["ditto_key_soak"] = self.ditto_soak_entry.get()
            config["ditto_name_soak"] = self.ditto_soak_name.get()
            config["ditto_key_sleep"] = self.ditto_slp_entry.get()
            config["ditto_name_sleep"] = self.ditto_slp_name.get()
            config["ditto_key_ball"] = self.ditto_ball_entry.get()
            config["ditto_key_potion"] = self.potion_key_entry.get()
            config["ditto_key_leppa"] = self.leppa_key_entry.get()
            config["auto_heal_hp"] = self.heal_hp_check.get()
            config["auto_heal_pp"] = self.heal_pp_check.get()

            with open("config.json", "w") as f: json.dump(config, f, indent=4)
            self.add_log(f"✅ Configuration saved successfully.")
        except Exception as e: self.add_log(f"❌ Error saving config: {e}")

    def add_log(self, msg):
        self.log_box.insert("end", f"{msg}\n"); self.log_box.see("end")

    def run_calib(self, mode):
        threading.Thread(target=selector.run_calibration, args=(mode, self.add_log), daemon=True).start()

    def save_debug(self):
        try:
            obs = PokéObserver(); frame = obs.capture_frame()
            if frame is not None: cv2.imwrite("debug_view.png", frame); self.add_log("📸 Debug frame saved.")
        except Exception as e: self.add_log(f"❌ Debug Error: {e}")

    def toggle_settings(self):
        if self.settings_visible:
            self.config_frame.grid_remove(); self.tabview.grid_remove(); self.calib_frame.grid_remove(); self.log_container.grid()
            self.toggle_btn.configure(text="SHOW CONFIGURATION"); self.settings_visible = False
        else:
            self.log_container.grid_remove(); self.config_frame.grid(); self.tabview.grid(); self.calib_frame.grid()
            self.toggle_btn.configure(text="VIEW FULL LOGGER"); self.settings_visible = True

    def toggle_bot(self):
        if not self.bot or not self.bot.running:
            self.save_all(); self.bot = ShinyBot(log_widget=self.log_box); self.bot.start()
            self.start_btn.configure(text="STOP AUTOMATION", fg_color="#dc3545")
        else:
            self.bot.stop(); self.bot = None; self.start_btn.configure(text="START AUTOMATED HUNT", fg_color="#28a745")

if __name__ == "__main__":
    app = ShinyHunterGUI(); app.mainloop()
