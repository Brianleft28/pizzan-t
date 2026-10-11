from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QFrame
from PyQt6.QtCore import pyqtSignal

class HeaderBar(QWidget):
    start_toggle_clicked = pyqtSignal()
    mode_changed = pyqtSignal(str)
    encounters_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 5)
        layout.setSpacing(8)

        # 1. Main Action Button
        self.btn_toggle = QPushButton("▶ START AUTOMATED HUNT")
        self.btn_toggle.setObjectName("startStopButton")
        self.btn_toggle.setFixedHeight(50)
        self.btn_toggle.clicked.connect(self.start_toggle_clicked.emit)
        layout.addWidget(self.btn_toggle)

        # 2. Sub-bar for Mode and Encounters
        bar_frame = QFrame()
        bar_frame.setObjectName("cardFrame")
        bar_layout = QHBoxLayout(bar_frame)
        bar_layout.setContentsMargins(12, 6, 12, 6)

        lbl_mode = QLabel("🎯 Modo:")
        lbl_mode.setStyleSheet("font-weight: bold; color: #58a6ff;")
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Horda", "Single", "Ditto"])
        self.combo_mode.currentTextChanged.connect(self.mode_changed.emit)

        lbl_enc = QLabel("🔢 Encounters:")
        lbl_enc.setStyleSheet("font-weight: bold; color: #58a6ff;")
        self.spin_enc = QSpinBox()
        self.spin_enc.setRange(0, 9999999)
        self.spin_enc.valueChanged.connect(self.encounters_changed.emit)

        bar_layout.addWidget(lbl_mode)
        bar_layout.addWidget(self.combo_mode)
        bar_layout.addSpacing(20)
        bar_layout.addWidget(lbl_enc)
        bar_layout.addWidget(self.spin_enc)
        bar_layout.addStretch()

        layout.addWidget(bar_frame)

    def set_running_state(self, is_running: bool):
        if is_running:
            self.btn_toggle.setText("⏹ STOP AUTOMATION")
            self.btn_toggle.setProperty("running", "true")
            self.btn_toggle.setStyle(self.btn_toggle.style())
        else:
            self.btn_toggle.setText("▶ START AUTOMATED HUNT")
            self.btn_toggle.setProperty("running", "false")
            self.btn_toggle.setStyle(self.btn_toggle.style())

    def set_mode(self, mode: str):
        idx = self.combo_mode.findText(mode.capitalize())
        if idx >= 0:
            self.combo_mode.setCurrentIndex(idx)

    def set_encounters(self, count: int):
        self.spin_enc.setValue(count)
