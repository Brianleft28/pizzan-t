import os
import threading
import cv2
import winsound
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox
)
from PyQt6.QtCore import pyqtSlot

from src.ui.views.styles import APP_STYLESHEET
from src.ui.views.components.header_bar import HeaderBar
from src.ui.views.components.stats_bar import StatsBar
from src.ui.views.components.logger_widget import LoggerWidget
from src.ui.views.components.brain_viewer import BrainViewerWidget
from src.ui.views.components.tabs.tab_general import TabGeneral
from src.ui.views.components.tabs.tab_horde import TabHorde
from src.ui.views.components.tabs.tab_ditto import TabDitto
from src.ui.views.components.tabs.tab_calib import TabCalib

from src.ui.controllers.config_controller import ConfigController
from src.ui.controllers.bot_controller import BotController
from src.vision import PokéObserver
import selector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🍕 PizzaHunter — Shiny & Ditto Hunter v8.0 [PyQt6 MVC]")
        self.resize(740, 780)
        self.setMinimumSize(700, 620)

        self.config_ctrl = ConfigController("config.json")
        self.bot_ctrl = BotController()

        self._init_ui()
        self._load_all_configs()
        self._wire_signals()

    def _init_ui(self):
        self.setStyleSheet(APP_STYLESHEET)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 0)
        main_layout.setSpacing(6)

        # 1. Header
        self.header = HeaderBar()
        main_layout.addWidget(self.header)

        # 2. Tabs
        self.tabs = QTabWidget()
        self.tab_general = TabGeneral()
        self.tab_horde = TabHorde()
        self.tab_ditto = TabDitto()
        self.tab_brain = BrainViewerWidget()
        self.tab_calib = TabCalib()

        self.tabs.addTab(self.tab_general, "⚙️ General")
        self.tabs.addTab(self.tab_horde, "🏹 Horde")
        self.tabs.addTab(self.tab_ditto, "👾 Ditto")
        self.tabs.addTab(self.tab_brain, "🧠 Brain")
        self.tabs.addTab(self.tab_calib, "🔧 Calib")
        main_layout.addWidget(self.tabs, stretch=1)

        # 3. Logger Panel
        self.logger = LoggerWidget()
        main_layout.addWidget(self.logger)

        # 4. Bottom Stats Bar
        self.stats_bar = StatsBar()
        main_layout.addWidget(self.stats_bar)

    def _wire_signals(self):
        # Header controls
        self.header.start_toggle_clicked.connect(self.toggle_bot)
        self.header.mode_changed.connect(self._on_mode_changed)
        self.header.encounters_changed.connect(self._on_encounters_changed)

        # Tabs Save signals
        self.tab_general.save_requested.connect(self.save_all)
        self.tab_general.install_roms_clicked.connect(self._install_roms_wip)
        self.tab_horde.save_requested.connect(self.save_all)
        self.tab_horde.test_alarm_clicked.connect(self.test_alarm)
        self.tab_horde.stop_alarm_clicked.connect(self.stop_alarm)
        self.tab_ditto.save_requested.connect(self.save_all)
        self.tab_ditto.optimize_ui_clicked.connect(self.optimize_pokemmo_ui)
        self.tab_calib.calib_requested.connect(self.run_calibration)
        self.tab_calib.debug_frame_requested.connect(self.save_debug)

        # Bot Controller Signals
        self.bot_ctrl.log_signal.connect(self.logger.append_log)
        self.bot_ctrl.stats_signal.connect(self.stats_bar.update_stats)
        self.bot_ctrl.bot_stopped.connect(self._on_bot_stopped)

    def _load_all_configs(self):
        cfg = self.config_ctrl.config
        self.header.set_mode(cfg.mode)
        self.header.set_encounters(cfg.total_encounters)
        self.tab_general.load_from_config(cfg)
        self.tab_horde.load_from_config(cfg)
        self.tab_ditto.load_from_config(cfg)

        self.logger.append_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "PHASE")
        self.logger.append_log("  🍕 PizzaHunter v8.0 — PyQt6 Edition", "HEADER")
        self.logger.append_log("  Arquitectura MVC desacoplada • Hilos seguros", "HEADER")
        self.logger.append_log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "PHASE")

    def save_all(self):
        cfg = self.config_ctrl.config
        cfg.mode = self.header.combo_mode.currentText().lower()
        cfg.total_encounters = self.header.spin_enc.value()
        self.tab_general.apply_to_config(cfg)
        self.tab_horde.apply_to_config(cfg)
        self.tab_ditto.apply_to_config(cfg)

        if self.config_ctrl.save(cfg):
            self.logger.append_log("✅ Configuración guardada en config.json.", "SUCCESS")
        else:
            self.logger.append_log("❌ Error guardando config.json.", "FATAL")

    def _on_mode_changed(self, mode_name: str):
        self.save_all()
        # Actualizar archivo en Brain Viewer si corresponde
        mode_map = {
            "horda": os.path.join("src", "modes", "horda.py"),
            "single": os.path.join("src", "modes", "single.py"),
            "ditto": os.path.join("src", "modes", "ditto.py"),
        }
        target = mode_map.get(mode_name.lower())
        if target:
            self.tab_brain.combo_files.setCurrentText(target)

    def _on_encounters_changed(self, count: int):
        self.save_all()

    def toggle_bot(self):
        if not self.bot_ctrl.is_running():
            self.save_all()
            self.header.set_running_state(True)
            self.bot_ctrl.start()
        else:
            self.bot_ctrl.stop()

    def _on_bot_stopped(self):
        self.header.set_running_state(False)
        self.stats_bar.reset()

    def test_alarm(self):
        def _play():
            path = os.path.join("assets", "shiny_alarm.wav")
            if os.path.exists(path):
                winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                winsound.Beep(1000, 500)
        threading.Thread(target=_play, daemon=True).start()
        self.logger.append_log("🎵 Reproduciendo alarma de prueba...", "ACTION")

    def stop_alarm(self):
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.logger.append_log("⏹ Alarma silenciada.", "INFO")

    def _install_roms_wip(self):
        self.logger.append_log("📦 [WIP] Utilizá 'manage.py' desde la terminal para instalar ROMs.", "ACTION")

    def optimize_pokemmo_ui(self):
        paths = [
            r"C:\Program Files\PokeMMO\config\main.properties",
            r"C:\PokeMMO\config\main.properties",
            r"D:\PokeMMO\config\main.properties",
            os.path.expanduser(r"~\Desktop\PokeMMO\config\main.properties")
        ]
        found = next((p for p in paths if os.path.exists(p)), None)
        if not found:
            self.logger.append_log("⚠️ No se encontró main.properties de PokeMMO.", "WARN")
            return

        try:
            with open(found, "r", encoding="utf-8") as f:
                lines = f.readlines()

            modified = False
            new_lines = []
            for line in lines:
                if line.startswith("client.ui.nameplate.") and "true" in line:
                    line = line.replace("true", "false")
                    modified = True
                elif line.startswith("client.gui.showchatbubbles") and "true" in line:
                    line = line.replace("true", "false")
                    modified = True
                new_lines.append(line)

            if modified:
                with open(found, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                self.logger.append_log("✅ PokeMMO UI optimizada (Nombres y Chats desactivados).", "SUCCESS")
            else:
                self.logger.append_log("✅ PokeMMO ya estaba optimizado.", "SUCCESS")
        except Exception as e:
            self.logger.append_log(f"❌ Error al optimizar PokeMMO: {e}", "FATAL")

    def run_calibration(self, mode: str):
        def _target():
            selector.run_calibration(mode, lambda msg, cat="INFO": self.bot_ctrl.log_signal.emit(msg, cat))
        threading.Thread(target=_target, daemon=True).start()

    def save_debug(self):
        try:
            obs = PokéObserver()
            frame = obs.capture_frame()
            if frame is not None:
                cv2.imwrite("debug_view.png", frame)
                self.logger.append_log("📸 Debug frame guardado en debug_view.png.", "SUCCESS")
            else:
                self.logger.append_log("⚠️ No se pudo capturar la ventana de PokeMMO.", "WARN")
        except Exception as e:
            self.logger.append_log(f"❌ Error al guardar debug frame: {e}", "FATAL")

    def closeEvent(self, event):
        if self.bot_ctrl.is_running():
            self.bot_ctrl.stop()
        event.accept()
