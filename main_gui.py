import tkinter as tk
import customtkinter as ctk
import os
import json
import threading
import selector
from src.bot_main import ShinyBot

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ShinyHunterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🇦🇷 SØREN - Shiny Hunter Bot")
        self.geometry("600x850")
        self.attributes("-topmost", True)

        self.bot = None
        self.settings_visible = True

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1) # Logger Row

        # 0. Toggle Button (Top)
        self.toggle_btn = ctk.CTkButton(self, text="VIEW FULL LOGGER", height=35, fg_color="#5a5a5a", 
                                         font=ctk.CTkFont(weight="bold"), command=self.toggle_settings)
        self.toggle_btn.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")

        # 1. Main Configuration Frame
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.mode_label = ctk.CTkLabel(self.config_frame, text="Hunting Mode:", font=ctk.CTkFont(weight="bold"))
        self.mode_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.mode_switch = ctk.CTkSegmentedButton(self.config_frame, values=["Horda", "Single", "Ditto"], 
                                                 command=self.save_all)
        self.mode_switch.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        initial_mode = self.get_config_val("mode", "horda").capitalize()
        self.mode_switch.set(initial_mode)

        self.count_label = ctk.CTkLabel(self.config_frame, text="Encounters:", font=ctk.CTkFont(weight="bold"))
        self.count_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.count_entry = ctk.CTkEntry(self.config_frame, width=70)
        self.count_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.count_entry.insert(0, self.get_config_val("total_encounters", "0"))

        # 2. Tabs
        self.tabview = ctk.CTkTabview(self, height=350)
        self.tabview.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.tab_general = self.tabview.add("General / Horde Settings")
        self.tab_ditto = self.tabview.add("Ditto Mode Settings")

        # General Tab
        self.web_label = ctk.CTkLabel(self.tab_general, text="Discord Webhook URL:", font=ctk.CTkFont(weight="bold"))
        self.web_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.web_entry = ctk.CTkEntry(self.tab_general, placeholder_text="https://discord.com/api/webhooks/...", width=350)
        self.web_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.web_entry.insert(0, self.get_config_val("discord_webhook"))

        self.adv_label = ctk.CTkLabel(self.tab_general, text="OCR Retries (General):", font=ctk.CTkFont(weight="bold"))
        self.adv_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ocr_entry = ctk.CTkEntry(self.tab_general, width=70)
        self.ocr_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ocr_entry.insert(0, self.get_config_val("ocr_retries", "6"))

        # Ditto Tab
        self.ditto_path_label = ctk.CTkLabel(self.tab_ditto, text="Patrol Time (Sec):", font=ctk.CTkFont(weight="bold"))
        self.ditto_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ditto_path_entry = ctk.CTkEntry(self.tab_ditto, width=70)
        self.ditto_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.ditto_path_entry.insert(0, self.get_config_val("ditto_patrol_time", "2.5"))

        self.ditto_hunter_label = ctk.CTkLabel(self.tab_ditto, text="Hunter Name:", font=ctk.CTkFont(weight="bold"))
        self.ditto_hunter_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.ditto_hunter_entry = ctk.CTkEntry(self.tab_ditto, width=120)
        self.ditto_hunter_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.ditto_hunter_entry.insert(0, self.get_config_val("hunter_pokemon_name", "Magikarp"))

        # Row 1: Attack and Sleep
        self.ditto_atk_label = ctk.CTkLabel(self.tab_ditto, text="Attack Slot:", font=ctk.CTkFont(weight="bold"))
        self.ditto_atk_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ditto_atk_entry = ctk.CTkEntry(self.tab_ditto, width=40); self.ditto_atk_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ditto_atk_entry.insert(0, self.get_config_val("ditto_key_attack", "2"))
        self.ditto_atk_name = ctk.CTkEntry(self.tab_ditto, width=90, placeholder_text="Name"); self.ditto_atk_name.grid(row=1, column=1, padx=(55, 0), pady=5, sticky="w")
        self.ditto_atk_name.insert(0, self.get_config_val("ditto_name_attack", "False Swipe"))

        self.ditto_slp_label = ctk.CTkLabel(self.tab_ditto, text="Sleep Slot:", font=ctk.CTkFont(weight="bold"))
        self.ditto_slp_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.ditto_slp_entry = ctk.CTkEntry(self.tab_ditto, width=40); self.ditto_slp_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.ditto_slp_entry.insert(0, self.get_config_val("ditto_key_sleep", "1"))
        self.ditto_slp_name = ctk.CTkEntry(self.tab_ditto, width=90, placeholder_text="Name"); self.ditto_slp_name.grid(row=1, column=3, padx=(55, 0), pady=5, sticky="w")
        self.ditto_slp_name.insert(0, self.get_config_val("ditto_name_sleep", "Spore"))

        # Row 2: Soak and Ball
        self.ditto_soak_label = ctk.CTkLabel(self.tab_ditto, text="Soak Slot:", font=ctk.CTkFont(weight="bold"))
        self.ditto_soak_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ditto_soak_entry = ctk.CTkEntry(self.tab_ditto, width=40); self.ditto_soak_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.ditto_soak_entry.insert(0, self.get_config_val("ditto_key_soak", "4"))
        self.ditto_soak_name = ctk.CTkEntry(self.tab_ditto, width=90, placeholder_text="Name"); self.ditto_soak_name.grid(row=2, column=1, padx=(55, 0), pady=5, sticky="w")
        self.ditto_soak_name.insert(0, self.get_config_val("ditto_name_soak", "Soak"))

        self.ditto_ball_label = ctk.CTkLabel(self.tab_ditto, text="Ball Hotkey:", font=ctk.CTkFont(weight="bold"))
        self.ditto_ball_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.ditto_ball_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.ditto_ball_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.ditto_ball_entry.insert(0, self.get_config_val("ditto_key_ball", "5"))

        # Row 3: OCR and Utility
        self.ditto_ocr_label = ctk.CTkLabel(self.tab_ditto, text="OCR Retries:", font=ctk.CTkFont(weight="bold"))
        self.ditto_ocr_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ditto_ocr_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.ditto_ocr_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.ditto_ocr_entry.insert(0, self.get_config_val("ditto_ocr_retries", "1"))

        self.leppa_key_label = ctk.CTkLabel(self.tab_ditto, text="Hotkey Leppa:", font=ctk.CTkFont(weight="bold"))
        self.leppa_key_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.leppa_key_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.leppa_key_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")
        self.leppa_key_entry.insert(0, self.get_config_val("ditto_key_leppa", "4"))

        self.potion_key_label = ctk.CTkLabel(self.tab_ditto, text="Hotkey Potion:", font=ctk.CTkFont(weight="bold"))
        self.potion_key_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.potion_key_entry = ctk.CTkEntry(self.tab_ditto, width=50); self.potion_key_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.potion_key_entry.insert(0, self.get_config_val("ditto_key_potion", "6"))

        self.save_btn_tab = ctk.CTkButton(self.tab_ditto, text="SAVE DITTO CONFIGURATION", fg_color="#1f538d", height=40, command=self.save_all)
        self.save_btn_tab.grid(row=5, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        # 3. Calibration Frame
        self.calib_frame = ctk.CTkFrame(self)
        self.calib_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.calib_title = ctk.CTkLabel(self.calib_frame, text="SCREENS CALIBRATION", font=ctk.CTkFont(size=14, weight="bold"))
        self.calib_title.pack(pady=5)
        
        # Row 1: Main Zones
        self.btns_row1 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row1.pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(self.btns_row1, text="CALIBRATE HORDE SLOTS", fg_color="#5a5a5a", command=lambda: self.run_calib("hud")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.btns_row1, text="CALIBRATE SINGLE SLOT", fg_color="#5a5a5a", command=lambda: self.run_calib("single_slot")).pack(side="left", padx=2, expand=True, fill="x")
        
        # Row 2: Combat UI
        self.btns_row2 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row2.pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(self.btns_row2, text="CALIBRATE RUN BUTTON", fg_color="#5a5a5a", command=lambda: self.run_calib("combat")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.btns_row2, text="CALIBRATE HP BAR", fg_color="#8d1f1f", command=lambda: self.run_calib("hp_bar")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.btns_row2, text="CALIBRATE STATUS", fg_color="#1f8d8d", command=lambda: self.run_calib("status_slot")).pack(side="left", padx=2, expand=True, fill="x")

        # Row 3: Advanced
        self.btns_row3 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row3.pack(fill="x", padx=10, pady=2)
        ctk.CTkButton(self.btns_row3, text="SLEEP ASSET", fg_color="#8d8d1f", width=100, command=lambda: self.run_calib("sleep_icon")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.btns_row3, text="PP SLOTS (4)", fg_color="#5a1f8d", width=100, command=lambda: self.run_calib("pp_slots")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.btns_row3, text="BATTLE MSG", fg_color="#1f8d5a", width=100, command=lambda: self.run_calib("battle_msg")).pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkButton(self.btns_row3, text="HUNTER HP", fg_color="#8d1f5a", width=100, command=lambda: self.run_calib("hunter_hp")).pack(side="left", padx=2, expand=True, fill="x")

        # 4. Logger Frame (Hidden when Settings visible)
        self.log_container = ctk.CTkFrame(self)
        self.log_container.grid(row=1, column=0, rowspan=3, padx=20, pady=10, sticky="nsew")
        self.log_container.grid_columnconfigure(0, weight=1); self.log_container.grid_rowconfigure(0, weight=1)
        self.log_box = ctk.CTkTextbox(self.log_container, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.log_container.grid_remove() # Default: hide logger

        # 5. Start Button
        self.start_btn = ctk.CTkButton(self, text="START AUTOMATED HUNT", height=70, 
                                     fg_color="#28a745", hover_color="#218838",
                                     font=ctk.CTkFont(size=20, weight="bold"),
                                     command=self.toggle_bot)
        self.start_btn.grid(row=5, column=0, padx=20, pady=20, sticky="ew")

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
            
            # General
            config["discord_webhook"] = self.web_entry.get(); config["total_encounters"] = int(self.count_entry.get())
            config["mode"] = self.mode_switch.get().lower(); config["ocr_retries"] = int(self.ocr_entry.get())
            
            # Ditto
            config["ditto_patrol_time"] = float(self.ditto_path_entry.get()); config["hunter_pokemon_name"] = self.ditto_hunter_entry.get()
            config["ditto_key_attack"] = self.ditto_atk_entry.get(); config["ditto_name_attack"] = self.ditto_atk_name.get()
            config["ditto_key_sleep"] = self.ditto_slp_entry.get(); config["ditto_name_sleep"] = self.ditto_slp_name.get()
            config["ditto_key_soak"] = self.ditto_soak_entry.get(); config["ditto_name_soak"] = self.ditto_soak_name.get()
            config["ditto_key_ball"] = self.ditto_ball_entry.get(); config["ditto_ocr_retries"] = int(self.ditto_ocr_entry.get())
            config["ditto_key_leppa"] = self.leppa_key_entry.get(); config["ditto_key_potion"] = self.potion_key_entry.get()

            with open("config.json", "w") as f: json.dump(config, f, indent=4)
            self.add_log(f"✅ Configuration saved. (Mode: {config['mode']})")
        except Exception as e: self.add_log(f"❌ Error saving: {e}")

    def add_log(self, msg):
        self.log_box.insert("end", f"{msg}\n"); self.log_box.see("end")

    def run_calib(self, mode):
        threading.Thread(target=selector.run_calibration, args=(mode, self.add_log), daemon=True).start()

    def toggle_settings(self):
        if self.settings_visible:
            self.config_frame.grid_remove(); self.tabview.grid_remove(); self.calib_frame.grid_remove()
            self.log_container.grid(); self.toggle_btn.configure(text="SHOW CONFIGURATION")
            self.settings_visible = False
        else:
            self.log_container.grid_remove()
            self.config_frame.grid(); self.tabview.grid(); self.calib_frame.grid()
            self.toggle_btn.configure(text="VIEW FULL LOGGER")
            self.settings_visible = True

    def toggle_bot(self):
        if not self.bot or not self.bot.running:
            self.save_all(); self.bot = ShinyBot(log_callback=self.add_log); self.bot.start()
            self.start_btn.configure(text="STOP AUTOMATION", fg_color="#dc3545")
        else:
            self.bot.stop(); self.bot = None; self.start_btn.configure(text="START AUTOMATED HUNT", fg_color="#28a745")

if __name__ == "__main__":
    app = ShinyHunterGUI(); app.mainloop()
