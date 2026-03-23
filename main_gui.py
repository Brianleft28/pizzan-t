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
        self.geometry("600x750")
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
        
        self.mode_switch = ctk.CTkSegmentedButton(self.config_frame, values=["Horda", "Single"], 
                                                 command=self.save_all)
        self.mode_switch.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        initial_mode = self.get_config_val("mode", "horda").capitalize()
        self.mode_switch.set(initial_mode)

        self.count_label = ctk.CTkLabel(self.config_frame, text="Encounters:", font=ctk.CTkFont(weight="bold"))
        self.count_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.count_entry = ctk.CTkEntry(self.config_frame, width=70)
        self.count_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        self.count_entry.insert(0, self.get_config_val("total_encounters", "0"))

        # Row 1: Discord Webhook
        self.web_label = ctk.CTkLabel(self.config_frame, text="Discord Webhook URL:", font=ctk.CTkFont(weight="bold"))
        self.web_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.web_entry = ctk.CTkEntry(self.config_frame, placeholder_text="https://discord.com/api/webhooks/...", width=400)
        self.web_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        self.web_entry.insert(0, self.get_config_val("discord_webhook"))

        # Row 2: Advanced Settings (OCR Retries)
        self.adv_label = ctk.CTkLabel(self.config_frame, text="OCR Retries:", font=ctk.CTkFont(weight="bold"))
        self.adv_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.ocr_entry = ctk.CTkEntry(self.config_frame, width=70)
        self.ocr_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.ocr_entry.insert(0, self.get_config_val("ocr_retries", "6"))
        
        self.save_btn = ctk.CTkButton(self.config_frame, text="SAVE CONFIG", fg_color="#1f538d", command=self.save_all)
        self.save_btn.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

        # 3. Calibration Frame
        self.calib_frame = ctk.CTkFrame(self)
        self.calib_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.calib_title = ctk.CTkLabel(self.calib_frame, text="SCREENS CALIBRATION", font=ctk.CTkFont(size=14, weight="bold"))
        self.calib_title.pack(pady=5)
        
        self.btns_row1 = ctk.CTkFrame(self.calib_frame, fg_color="transparent")
        self.btns_row1.pack(fill="x", padx=10, pady=5)
        
        self.btn_hud = ctk.CTkButton(self.btns_row1, text="CALIB. HORDE SLOTS", fg_color="#5a5a5a", command=lambda: self.run_calib("hud"))
        self.btn_hud.pack(side="left", padx=5, expand=True, fill="x")

        self.btn_single = ctk.CTkButton(self.btns_row1, text="CALIB. SINGLE SLOT", fg_color="#5a5a5a", command=lambda: self.run_calib("single_slot"))
        self.btn_single.pack(side="left", padx=5, expand=True, fill="x")
        
        self.btn_combat = ctk.CTkButton(self.calib_frame, text="CALIBRATE RUN BUTTON AREA", fg_color="#5a5a5a", command=lambda: self.run_calib("combat"))
        self.btn_combat.pack(fill="x", padx=15, pady=5)

        # 4. Logger Frame
        self.log_box = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_box.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
        self.log_box.insert("0.0", "--- SYSTEM INITIALIZED ---\n")

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
            config["discord_webhook"] = self.web_entry.get()
            config["total_encounters"] = int(self.count_entry.get())
            config["mode"] = self.mode_switch.get().lower()
            config["ocr_retries"] = int(self.ocr_entry.get())
            with open("config.json", "w") as f: json.dump(config, f, indent=4)
            self.add_log(f"✅ Configuration saved. (Mode: {config['mode']}, Retries: {config['ocr_retries']})")
        except: self.add_log("❌ Error saving configuration. Check inputs.")

    def add_log(self, msg):
        self.log_box.insert("end", f"{msg}\n")
        self.log_box.see("end")

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
