from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QGroupBox
)
from PyQt6.QtCore import pyqtSignal

class TabCalib(QWidget):
    calib_requested = pyqtSignal(str)
    debug_frame_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        grp_tools = QGroupBox("Herramientas de Visión / Calibración")
        grid = QGridLayout(grp_tools)
        grid.setSpacing(8)

        buttons = [
            ("HUD HORDE", "hud", "#21262d"),
            ("SINGLE SLOT", "single_slot", "#21262d"),
            ("RUN BTN", "combat", "#21262d"),
            ("HP BAR", "hp_bar", "#8d1f1f"),
            ("STATUS", "status_slot", "#1f8d8d"),
            ("SLEEP ICON", "sleep_icon", "#8d8d1f"),
            ("PP SLOTS", "pp_slots", "#5a1f8d"),
            ("BATTLE MSG", "battle_msg", "#1f8d5a"),
            ("MY HP", "hunter_hp", "#8d1f5a"),
        ]

        for i, (text, mode, color) in enumerate(buttons):
            r = i // 3
            c = i % 3
            btn = QPushButton(text)
            btn.setFixedHeight(36)
            btn.setStyleSheet(f"background-color: {color}; color: white; font-weight: bold;")
            btn.clicked.connect(lambda checked, m=mode: self.calib_requested.emit(m))
            grid.addWidget(btn, r, c)

        layout.addWidget(grp_tools)

        btn_debug = QPushButton("📸 CAPTURAR DEBUG FRAME (debug_view.png)")
        btn_debug.setFixedHeight(38)
        btn_debug.setStyleSheet("background-color: #30363d; color: #58a6ff; font-weight: bold;")
        btn_debug.clicked.connect(self.debug_frame_requested.emit)
        layout.addWidget(btn_debug)

        layout.addStretch()
