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
        self.geometry("600x800")
        self.attributes("-topmost", True)

        self.bot = None

        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # 1. Main Configuration Frame
        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # Row 0: Mode and Encounters
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

        # 2. Tabs for specific configurations
        self.tabview = ctk.CTkTabview(self, height=250)
        self.tabview.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        self.tab_general = self.tabview.add("General / Horde")
        self.tab_ditto = self.tabview.add("Ditto Mode")

        # General Tab Content
        self.web_label = ctk.CTkLabel(self.tab_general, text="Discord Webhook URL:", font=ctk.CTkFont(weight="bold"))
        self.web_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.web_entry = ctk.CTkEntry(self.tab_general, placeholder_text="https://discord.com/api/webhooks/...", width=350)
        self.web_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.web_entry.insert(0, self.get_config_val("discord_webhook"))

        self.adv_label = ctk.CTkLabel(self.tab_general, text="OCR Retries:", font=ctk.CTkFont(weight="bold"))
        self.adv_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ocr_entry = ctk.CTkEntry(self.tab_general, width=70)
        self.ocr_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ocr_entry.insert(0, self.get_config_val("ocr_retries", "6"))

        # Ditto Tab Content
        self.ditto_path_label = ctk.CTkLabel(self.tab_ditto, text="Patrol Time (Seconds):", font=ctk.CTkFont(weight="bold"))
        self.ditto_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ditto_path_entry = ctk.CTkEntry(self.tab_ditto, width=70)
        self.ditto_path_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.ditto_path_entry.insert(0, self.get_config_val("ditto_patrol_time", "2.5"))

        self.ditto_hunter_label = ctk.CTkLabel(self.tab_ditto, text="Hunter Poke Name:", font=ctk.CTkFont(weight="bold"))
        self.ditto_hunter_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.ditto_hunter_entry = ctk.CTkEntry(self.tab_ditto, width=120)
        self.ditto_hunter_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        self.ditto_hunter_entry.insert(0, self.get_config_val("hunter_pokemon_name", "Magikarp"))

        self.ditto_atk_label = ctk.CTkLabel(self.tab_ditto, text="Key Attack:", font=ctk.CTkFont(weight="bold"))
        self.ditto_atk_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ditto_atk_entry = ctk.CTkEntry(self.tab_ditto, width=40)
        self.ditto_atk_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.ditto_atk_entry.insert(0, self.get_config_val("ditto_key_attack", "2"))
        self.ditto_atk_name = ctk.CTkEntry(self.tab_ditto, width=100, placeholder_text="Move Name")
        self.ditto_atk_name.grid(row=1, column=1, padx=(55, 0), pady=5, sticky="w")
        self.ditto_atk_name.insert(0, self.get_config_val("ditto_name_attack", "False Swipe"))

        self.ditto_slp_label = ctk.CTkLabel(self.tab_ditto, text="Key Sleep:", font=ctk.CTkFont(weight="bold"))
        self.ditto_slp_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.ditto_slp_entry = ctk.CTkEntry(self.tab_ditto, width=40)
        self.ditto_slp_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.ditto_slp_entry.insert(0, self.get_config_val("ditto_key_sleep", "1"))
        self.ditto_slp_name = ctk.CTkEntry(self.tab_ditto, width=100, placeholder_text="Move Name")
        self.ditto_slp_name.grid(row=1, column=3, padx=(55, 0), pady=5, sticky="w")
        self.ditto_slp_name.insert(0, self.get_config_val("ditto_name_sleep", "Spore"))

        self.ditto_soak_label = ctk.CTkLabel(self.tab_ditto, text="Hotkey Soak (Anegar):", font=ctk.CTkFont(weight="bold"))
        self.ditto_soak_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ditto_soak_entry = ctk.CTkEntry(self.tab_ditto, width=40)
        self.ditto_soak_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.ditto_soak_entry.insert(0, self.get_config_val("ditto_key_soak", "4"))
        self.ditto_soak_name = ctk.CTkEntry(self.tab_ditto, width=100, placeholder_text="Move Name")
        self.ditto_soak_name.grid(row=2, column=1, padx=(55, 0), pady=5, sticky="w")
        self.ditto_soak_name.insert(0, self.get_config_val("ditto_name_soak", "Soak"))

        self.ditto_ball_label = ctk.CTkLabel(self.tab_ditto, text="Hotkey Ball (5th slot):", font=ctk.CTkFont(weight="bold"))
        self.ditto_ball_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.ditto_ball_entry = ctk.CTkEntry(self.tab_ditto, width=50)
        self.ditto_ball_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")
        self.ditto_ball_entry.insert(0, self.get_config_val("ditto_key_ball", "5"))

        self.ditto_ocr_label = ctk.CTkLabel(self.tab_ditto, text="Ditto OCR Retries:", font=ctk.CTkFont(weight="bold"))
        self.ditto_ocr_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.ditto_ocr_entry = ctk.CTkEntry(self.tab_ditto, width=50)
        self.ditto_ocr_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.ditto_ocr_entry.insert(0, self.get_config_val("ditto_ocr_retries", "1"))

        self.leppa_key_label = ctk.CTkLabel(self.tab_ditto, text="Hotkey Leppa:", font=ctk.CTkFont(weight="bold"))
        self.leppa_key_label.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.leppa_key_entry = ctk.CTkEntry(self.tab_ditto, width=50)
        self.leppa_key_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")
        self.leppa_key_entry.insert(0, self.get_config_val("ditto_key_leppa", "4"))

        self.leppa_count_label = ctk.CTkLabel(self.tab_ditto, text="Leppa every X Dittos:", font=ctk.CTkFont(weight="bold"))
        self.leppa_count_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.leppa_count_entry = ctk.CTkEntry(self.tab_ditto, width=50)
        self.leppa_count_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.leppa_count_entry.insert(0, self.get_config_val("ditto_leppa_count", "10"))

        self.potion_key_label = ctk.CTkLabel(self.tab_ditto, text="Hotkey Potion:", font=ctk.CTkFont(weight="bold"))
        self.potion_key_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.potion_key_entry = ctk.CTkEntry(self.tab_ditto, width=50)
        self.potion_key_entry.grid(row=4, column=3, padx=10, pady=5, sticky="w")
        self.potion_key_entry.insert(0, self.get_config_val("ditto_key_potion", "6"))

        self.save_btn = ctk.CTkButton(self, text="SAVE CONFIGURATION", fg_color="#1f538d", height=40, command=self.save_all)
        self.save_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # 3. Calibration Frame
        self.calib_frame = ctk.CTkFrame(self)
        self.calib_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.calib_title = ctk.CTkLabel(self.calib_frame, text="SCREENS CALIBRATION", font=ctk.CTkFont(size=14, weight="bold"))
        self.calib_title.pack(pady=5)
        
        self.btns_row1 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row1.pack(fill="x", padx=10, pady=2)
        
        self.btn_hud = ctk.CTkButton(self.btns_row1, text="HORDE SLOTS", fg_color="#5a5a5a", command=lambda: self.run_calib("hud"))
        self.btn_hud.pack(side="left", padx=2, expand=True, fill="x")

        self.btn_single = ctk.CTkButton(self.btns_row1, text="SINGLE SLOT", fg_color="#5a5a5a", command=lambda: self.run_calib("single_slot"))
        self.btn_single.pack(side="left", padx=2, expand=True, fill="x")
        
        self.btns_row2 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row2.pack(fill="x", padx=10, pady=2)

        self.btn_combat = ctk.CTkButton(self.btns_row2, text="RUN BUTTON", fg_color="#5a5a5a", command=lambda: self.run_calib("combat"))
        self.btn_combat.pack(side="left", padx=2, expand=True, fill="x")

        self.btn_hp = ctk.CTkButton(self.btns_row2, text="HP BAR AREA", fg_color="#8d1f1f", command=lambda: self.run_calib("hp_bar"))
        self.btn_hp.pack(side="left", padx=2, expand=True, fill="x")

        self.btn_status = ctk.CTkButton(self.btns_row2, text="STATUS SLOT", fg_color="#1f8d8d", command=lambda: self.run_calib("status_slot"))
        self.btn_status.pack(side="left", padx=2, expand=True, fill="x")

        self.btn_icon = ctk.CTkButton(self.btns_row2, text="SLEEP ICON", fg_color="#8d8d1f", command=lambda: self.run_calib("sleep_icon"))
        self.btn_icon.pack(side="left", padx=2, expand=True, fill="x")

        self.btns_row3 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row3.pack(fill="x", padx=10, pady=2)

        self.btn_pp = ctk.CTkButton(self.btns_row3, text="PP SLOTS (4 RECTS)", fg_color="#5a1f8d", command=lambda: self.run_calib("pp_slots"))
        self.btn_pp.pack(side="left", padx=2, expand=True, fill="x")

        self.btn_msg = ctk.CTkButton(self.btns_row3, text="BATTLE MSG", fg_color="#1f8d5a", command=lambda: self.run_calib("battle_msg"))
        self.btn_msg.pack(side="left", padx=2, expand=True, fill="x")

        # 4. Logger Frame
        self.log_container = ctk.CTkFrame(self)
        self.log_container.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.log_container.grid_columnconfigure(0, weight=1)
        self.log_container.grid_rowconfigure(0, weight=1)

        self.log_box = ctk.CTkTextbox(self.log_container, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.log_box.insert("0.0", "--- SYSTEM INITIALIZED ---\n")
        
        self.clear_log_btn = ctk.CTkButton(self.log_container, text="CLEAR LOGS", fg_color="#5a5a5a", height=25, command=self.clear_logs)
        self.clear_log_btn.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

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
            config["discord_webhook"] = self.web_entry.get()
            config["total_encounters"] = int(self.count_entry.get())
            config["mode"] = self.mode_switch.get().lower()
            config["ocr_retries"] = int(self.ocr_entry.get())
            
            # Ditto
            config["ditto_patrol_time"] = float(self.ditto_path_entry.get())
            config["hunter_pokemon_name"] = self.ditto_hunter_entry.get()
            config["ditto_key_attack"] = self.ditto_atk_entry.get()
            config["ditto_name_attack"] = self.ditto_atk_name.get()
            config["ditto_key_sleep"] = self.ditto_slp_entry.get()
            config["ditto_name_sleep"] = self.ditto_slp_name.get()
            config["ditto_key_soak"] = self.ditto_soak_entry.get()
            config["ditto_name_soak"] = self.ditto_soak_name.get()
            config["ditto_key_ball"] = self.ditto_ball_entry.get()
            config["ditto_ocr_retries"] = int(self.ditto_ocr_entry.get())
            config["ditto_key_leppa"] = self.leppa_key_entry.get()
            config["ditto_leppa_count"] = int(self.leppa_count_entry.get())
            config["ditto_key_potion"] = self.potion_key_entry.get()

            with open("config.json", "w") as f: json.dump(config, f, indent=4)
            self.add_log(f"✅ Configuration saved. (Mode: {config['mode']})")
        except: self.add_log("❌ Error saving configuration. Check inputs.")

    def add_log(self, msg):
        self.log_box.insert("end", f"{msg}\n")
        self.log_box.see("end")

    def clear_logs(self):
        self.log_box.delete("0.0", "end")
        self.add_log("--- LOGS CLEARED ---")

    def run_calib(self, mode):
        threading.Thread(target=selector.run_calibration, args=(mode, self.add_log), daemon=True).start()

    def toggle_bot(self):
        if not self.bot or not self.bot.running:
            self.save_all()
            self.bot = ShinyBot(log_callback=self.add_log)
            self.bot.start()
            self.start_btn.configure(text="STOP AUTOMATION", fg_color="#dc3545")
        else:
            self.bot.stop()
            self.bot = None 
            self.start_btn.configure(text="START AUTOMATED HUNT", fg_color="#28a745")

if __name__ == "__main__":
    app = ShinyHunterGUI()
    app.mainloop()
