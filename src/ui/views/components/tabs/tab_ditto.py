from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QDoubleSpinBox, QCheckBox, QPushButton, QLabel, QGroupBox, QScrollArea
)
from PyQt6.QtCore import pyqtSignal

class TabDitto(QWidget):
    save_requested = pyqtSignal()
    optimize_ui_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # 1. Movimientos y Captura
        grp_moves = QGroupBox("Ataques y Utilitarios")
        form_moves = QFormLayout(grp_moves)

        self.spin_patrol = QDoubleSpinBox()
        self.spin_patrol.setRange(0.5, 10.0)
        self.spin_patrol.setValue(2.5)
        form_moves.addRow(QLabel("⏱️ Tiempo Patrulla (s):"), self.spin_patrol)

        # Ataque
        row_atk = QHBoxLayout()
        self.edit_atk_key = QLineEdit("2")
        self.edit_atk_key.setMaximumWidth(40)
        self.edit_atk_name = QLineEdit("False Swipe")
        self.edit_atk_pp = QLineEdit("40")
        self.edit_atk_pp.setMaximumWidth(40)
        row_atk.addWidget(QLabel("Tecla:"))
        row_atk.addWidget(self.edit_atk_key)
        row_atk.addWidget(QLabel("Nombre:"))
        row_atk.addWidget(self.edit_atk_name)
        row_atk.addWidget(QLabel("PP:"))
        row_atk.addWidget(self.edit_atk_pp)
        form_moves.addRow(QLabel("1. Ataque Principal:"), row_atk)

        # Dormir
        row_slp = QHBoxLayout()
        self.edit_slp_key = QLineEdit("1")
        self.edit_slp_key.setMaximumWidth(40)
        self.edit_slp_name = QLineEdit("Spore")
        self.edit_slp_pp = QLineEdit("15")
        self.edit_slp_pp.setMaximumWidth(40)
        row_slp.addWidget(QLabel("Tecla:"))
        row_slp.addWidget(self.edit_slp_key)
        row_slp.addWidget(QLabel("Nombre:"))
        row_slp.addWidget(self.edit_slp_name)
        row_slp.addWidget(QLabel("PP:"))
        row_slp.addWidget(self.edit_slp_pp)
        form_moves.addRow(QLabel("2. Estado Sueño:"), row_slp)

        # Hotkeys extra
        row_extra = QHBoxLayout()
        self.edit_ball = QLineEdit("5")
        self.edit_ball.setMaximumWidth(40)
        self.edit_potion = QLineEdit("6")
        self.edit_potion.setMaximumWidth(40)
        self.edit_leppa = QLineEdit("4")
        self.edit_leppa.setMaximumWidth(40)
        row_extra.addWidget(QLabel("Pokéball:"))
        row_extra.addWidget(self.edit_ball)
        row_extra.addWidget(QLabel("Poción:"))
        row_extra.addWidget(self.edit_potion)
        row_extra.addWidget(QLabel("Leppa:"))
        row_extra.addWidget(self.edit_leppa)
        form_moves.addRow(QLabel("3. Objetos:"), row_extra)

        # Curación
        row_heal = QHBoxLayout()
        self.chk_heal_hp = QCheckBox("Auto-Curar HP")
        self.chk_heal_hp.setChecked(True)
        self.chk_heal_pp = QCheckBox("Auto-Restaurar PP")
        self.chk_heal_pp.setChecked(True)
        row_heal.addWidget(self.chk_heal_hp)
        row_heal.addWidget(self.chk_heal_pp)
        form_moves.addRow(QLabel("4. Mantenimiento:"), row_heal)

        layout.addWidget(grp_moves)

        # 2. Timings de Captura
        grp_timings = QGroupBox("⏱️ Timings de Captura (Segundos)")
        form_timings = QFormLayout(grp_timings)

        self.spin_ball_wait = QDoubleSpinBox()
        self.spin_ball_wait.setRange(0.1, 5.0)
        self.spin_ball_wait.setValue(0.5)
        form_timings.addRow(QLabel("Espera OCR Pre-Ball:"), self.spin_ball_wait)

        self.spin_settle = QDoubleSpinBox()
        self.spin_settle.setRange(0.5, 10.0)
        self.spin_settle.setValue(2.5)
        form_timings.addRow(QLabel("Espera Animación Captura:"), self.spin_settle)

        self.spin_leppa_wait = QDoubleSpinBox()
        self.spin_leppa_wait.setRange(0.1, 5.0)
        self.spin_leppa_wait.setValue(1.5)
        form_timings.addRow(QLabel("Espera Pre-Leppa:"), self.spin_leppa_wait)

        self.spin_ball_press = QDoubleSpinBox()
        self.spin_ball_press.setRange(0.1, 5.0)
        self.spin_ball_press.setValue(0.7)
        form_timings.addRow(QLabel("Retraso Presión Pokéball:"), self.spin_ball_press)

        layout.addWidget(grp_timings)

        # 3. Acciones
        self.btn_opt = QPushButton("⚡ Optimizar PokeMMO UI (Ocultar Nombres/Chats)")
        self.btn_opt.setStyleSheet("background-color: #8957e5; color: white;")
        self.btn_opt.clicked.connect(self.optimize_ui_clicked.emit)
        layout.addWidget(self.btn_opt)

        self.btn_save = QPushButton("💾 GUARDAR CONFIGURACIÓN DITTO")
        self.btn_save.setFixedHeight(36)
        self.btn_save.setStyleSheet("background-color: #1f6feb; color: white;")
        self.btn_save.clicked.connect(self.save_requested.emit)
        layout.addWidget(self.btn_save)

        layout.addStretch()

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def load_from_config(self, config):
        self.spin_patrol.setValue(config.ditto_patrol_time)
        self.edit_atk_key.setText(config.ditto_key_attack)
        self.edit_atk_name.setText(config.ditto_name_attack)
        self.edit_atk_pp.setText(config.pp_max_swipe)
        self.edit_slp_key.setText(config.ditto_key_sleep)
        self.edit_slp_name.setText(config.ditto_name_sleep)
        self.edit_slp_pp.setText(config.pp_max_spore)
        self.edit_ball.setText(config.ditto_key_ball)
        self.edit_potion.setText(config.ditto_key_potion)
        self.edit_leppa.setText(config.ditto_key_leppa)
        self.chk_heal_hp.setChecked(config.auto_heal_hp)
        self.chk_heal_pp.setChecked(config.auto_heal_pp)
        self.spin_ball_wait.setValue(config.timing_ball_wait)
        self.spin_settle.setValue(config.timing_capture_settle)
        self.spin_leppa_wait.setValue(config.timing_leppa_wait)
        self.spin_ball_press.setValue(config.timing_ball_press_wait)

    def apply_to_config(self, config):
        config.ditto_patrol_time = self.spin_patrol.value()
        config.ditto_key_attack = self.edit_atk_key.text().strip()
        config.ditto_name_attack = self.edit_atk_name.text().strip()
        config.pp_max_swipe = self.edit_atk_pp.text().strip()
        config.ditto_key_sleep = self.edit_slp_key.text().strip()
        config.ditto_name_sleep = self.edit_slp_name.text().strip()
        config.pp_max_spore = self.edit_slp_pp.text().strip()
        config.ditto_key_ball = self.edit_ball.text().strip()
        config.ditto_key_potion = self.edit_potion.text().strip()
        config.ditto_key_leppa = self.edit_leppa.text().strip()
        config.auto_heal_hp = self.chk_heal_hp.isChecked()
        config.auto_heal_pp = self.chk_heal_pp.isChecked()
        config.timing_ball_wait = self.spin_ball_wait.value()
        config.timing_capture_settle = self.spin_settle.value()
        config.timing_leppa_wait = self.spin_leppa_wait.value()
        config.timing_ball_press_wait = self.spin_ball_press.value()
