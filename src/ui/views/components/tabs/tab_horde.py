from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QDoubleSpinBox, QCheckBox, QPushButton, QLabel, QComboBox, QGroupBox
)
from PyQt6.QtCore import pyqtSignal

class TabHorde(QWidget):
    save_requested = pyqtSignal()
    test_alarm_clicked = pyqtSignal()
    stop_alarm_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # 1. Config Hordas
        grp_horde = QGroupBox("Configuración de Hordas")
        form_horde = QFormLayout(grp_horde)

        self.combo_size = QComboBox()
        self.combo_size.addItems(["3", "5"])
        form_horde.addRow(QLabel("👥 Tamaño de Horda:"), self.combo_size)

        self.chk_zorua = QCheckBox("Habilitar Modo Zorua")
        form_horde.addRow(QLabel("🦊 Modo Zorua:"), self.chk_zorua)

        self.spin_zorua_wait = QDoubleSpinBox()
        self.spin_zorua_wait.setRange(0.5, 10.0)
        self.spin_zorua_wait.setSingleStep(0.5)
        self.spin_zorua_wait.setValue(3.0)
        form_horde.addRow(QLabel("⏳ Espera Zorua (s):"), self.spin_zorua_wait)

        layout.addWidget(grp_horde)

        # 2. Hotkeys & PP
        grp_keys = QGroupBox("Atajos y Dulce Aroma")
        form_keys = QFormLayout(grp_keys)

        self.edit_sweet_key = QLineEdit("5")
        self.edit_sweet_key.setMaximumWidth(60)
        form_keys.addRow(QLabel("🌸 Tecla Dulce Aroma:"), self.edit_sweet_key)

        self.edit_sweet_slot = QLineEdit("1")
        self.edit_sweet_slot.setMaximumWidth(60)
        form_keys.addRow(QLabel("🔢 Slot Pokémon (1-6):"), self.edit_sweet_slot)

        self.edit_sweet_pp = QLineEdit("32")
        self.edit_sweet_pp.setMaximumWidth(60)
        form_keys.addRow(QLabel("⚡ PP Máximos:"), self.edit_sweet_pp)

        self.edit_leppa_key = QLineEdit("4")
        self.edit_leppa_key.setMaximumWidth(60)
        form_keys.addRow(QLabel("🍒 Tecla Baya Zanama (Leppa):"), self.edit_leppa_key)

        layout.addWidget(grp_keys)

        # 3. Alarma & Guardar
        alarm_layout = QHBoxLayout()
        btn_test = QPushButton("🎵 Probar Alarma")
        btn_test.clicked.connect(self.test_alarm_clicked.emit)
        btn_stop = QPushButton("⏹ Detener Alarma")
        btn_stop.clicked.connect(self.stop_alarm_clicked.emit)
        alarm_layout.addWidget(btn_test)
        alarm_layout.addWidget(btn_stop)
        layout.addLayout(alarm_layout)

        self.btn_save = QPushButton("💾 GUARDAR CONFIGURACIÓN DE HORDA")
        self.btn_save.setFixedHeight(36)
        self.btn_save.setStyleSheet("background-color: #1f6feb; color: white;")
        self.btn_save.clicked.connect(self.save_requested.emit)
        layout.addWidget(self.btn_save)

        layout.addStretch()

    def load_from_config(self, config):
        idx = self.combo_size.findText(str(config.horde_size))
        if idx >= 0:
            self.combo_size.setCurrentIndex(idx)
        self.chk_zorua.setChecked(config.mode_zorua)
        self.spin_zorua_wait.setValue(config.zorua_wait)
        self.edit_sweet_key.setText(config.horde_key_sweet_scent)
        self.edit_sweet_slot.setText(config.horde_slot_sweet_scent)
        self.edit_sweet_pp.setText(config.pp_max_sweet_scent)
        self.edit_leppa_key.setText(config.horde_key_leppa)

    def apply_to_config(self, config):
        config.horde_size = int(self.combo_size.currentText())
        config.mode_zorua = self.chk_zorua.isChecked()
        config.zorua_wait = self.spin_zorua_wait.value()
        config.horde_key_sweet_scent = self.edit_sweet_key.text().strip()
        config.horde_slot_sweet_scent = self.edit_sweet_slot.text().strip()
        config.pp_max_sweet_scent = self.edit_sweet_pp.text().strip()
        config.horde_key_leppa = self.edit_leppa_key.text().strip()
