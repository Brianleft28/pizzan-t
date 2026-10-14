import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QDoubleSpinBox, QSpinBox, QCheckBox, QPushButton, QLabel, QGroupBox, QScrollArea
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
        self.edit_atk_key.setMaximumWidth(35)
        self.edit_atk_name = QLineEdit("False Swipe")
        self.edit_atk_pp = QLineEdit("40")
        self.edit_atk_pp.setMaximumWidth(40)
        self.spin_thresh_swipe = QSpinBox()
        self.spin_thresh_swipe.setRange(1, 40)
        self.spin_thresh_swipe.setValue(20)
        self.spin_thresh_swipe.setMaximumWidth(50)

        row_atk.addWidget(QLabel("Tecla:"))
        row_atk.addWidget(self.edit_atk_key)
        row_atk.addWidget(QLabel("Nombre:"))
        row_atk.addWidget(self.edit_atk_name)
        row_atk.addWidget(QLabel("Tope:"))
        row_atk.addWidget(self.edit_atk_pp)
        row_atk.addWidget(QLabel("Curar en ≤:"))
        row_atk.addWidget(self.spin_thresh_swipe)
        row_atk.addWidget(QLabel("(MAX)"))
        form_moves.addRow(QLabel("1. Ataque Principal:"), row_atk)

        # Dormir
        row_slp = QHBoxLayout()
        self.edit_slp_key = QLineEdit("1")
        self.edit_slp_key.setMaximumWidth(35)
        self.edit_slp_name = QLineEdit("Spore")
        self.edit_slp_pp = QLineEdit("15")
        self.edit_slp_pp.setMaximumWidth(40)
        self.spin_thresh_spore = QSpinBox()
        self.spin_thresh_spore.setRange(1, 20)
        self.spin_thresh_spore.setValue(5)
        self.spin_thresh_spore.setMaximumWidth(50)

        row_slp.addWidget(QLabel("Tecla:"))
        row_slp.addWidget(self.edit_slp_key)
        row_slp.addWidget(QLabel("Nombre:"))
        row_slp.addWidget(self.edit_slp_name)
        row_slp.addWidget(QLabel("Tope:"))
        row_slp.addWidget(self.edit_slp_pp)
        row_slp.addWidget(QLabel("Curar en ≤:"))
        row_slp.addWidget(self.spin_thresh_spore)
        row_slp.addWidget(QLabel("(1 Baya)"))
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

        # 2. Control de PP en Vivo (Sincronización)
        grp_pp_live = QGroupBox("🔋 Estado y Sincronización de PP (En Vivo)")
        form_pp_live = QFormLayout(grp_pp_live)

        row_live = QHBoxLayout()
        self.spin_curr_swipe = QSpinBox()
        self.spin_curr_swipe.setRange(0, 50)
        self.spin_curr_swipe.setValue(40)
        self.spin_curr_swipe.setMaximumWidth(60)

        self.spin_curr_spore = QSpinBox()
        self.spin_curr_spore.setRange(0, 30)
        self.spin_curr_spore.setValue(15)
        self.spin_curr_spore.setMaximumWidth(60)

        self.btn_reset_pp = QPushButton("🔄 Restablecer PP al Máximo")
        self.btn_reset_pp.setStyleSheet("background-color: #238636; color: white; font-weight: bold;")
        self.btn_reset_pp.clicked.connect(self._reset_pp_to_max)

        row_live.addWidget(QLabel("Falso Tortazo actual:"))
        row_live.addWidget(self.spin_curr_swipe)
        row_live.addWidget(QLabel("Espora actual:"))
        row_live.addWidget(self.spin_curr_spore)
        row_live.addWidget(self.btn_reset_pp)
        form_pp_live.addRow(QLabel("Sincronización:"), row_live)

        layout.addWidget(grp_pp_live)

        # 3. Timings de Captura
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

        # 4. Acciones
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

    def _load_live_pp(self):
        try:
            if os.path.exists("pp_state.json"):
                with open("pp_state.json", "r") as f:
                    data = json.load(f)
                    self.spin_curr_swipe.setValue(int(data.get("swipe", 40)))
                    self.spin_curr_spore.setValue(int(data.get("spore", 15)))
        except Exception:
            pass

    def _save_live_pp(self):
        try:
            state = {}
            if os.path.exists("pp_state.json"):
                with open("pp_state.json", "r") as f:
                    state = json.load(f)
            state["swipe"] = self.spin_curr_swipe.value()
            state["spore"] = self.spin_curr_spore.value()
            with open("pp_state.json", "w") as f:
                json.dump(state, f, indent=4)
        except Exception:
            pass

    def _reset_pp_to_max(self):
        try:
            max_swipe = int(self.edit_atk_pp.text().strip() or 40)
            max_spore = int(self.edit_slp_pp.text().strip() or 15)
            self.spin_curr_swipe.setValue(max_swipe)
            self.spin_curr_spore.setValue(max_spore)
            self._save_live_pp()
        except Exception:
            pass

    def load_from_config(self, config):
        self.spin_patrol.setValue(config.ditto_patrol_time)
        self.edit_atk_key.setText(config.ditto_key_attack)
        self.edit_atk_name.setText(config.ditto_name_attack)
        self.edit_atk_pp.setText(config.pp_max_swipe)
        self.spin_thresh_swipe.setValue(getattr(config, "pp_threshold_swipe", 20))
        self.edit_slp_key.setText(config.ditto_key_sleep)
        self.edit_slp_name.setText(config.ditto_name_sleep)
        self.edit_slp_pp.setText(config.pp_max_spore)
        self.spin_thresh_spore.setValue(getattr(config, "pp_threshold_spore", 5))
        self.edit_ball.setText(config.ditto_key_ball)
        self.edit_potion.setText(config.ditto_key_potion)
        self.edit_leppa.setText(config.ditto_key_leppa)
        self.chk_heal_hp.setChecked(config.auto_heal_hp)
        self.chk_heal_pp.setChecked(config.auto_heal_pp)
        self.spin_ball_wait.setValue(config.timing_ball_wait)
        self.spin_settle.setValue(config.timing_capture_settle)
        self.spin_leppa_wait.setValue(config.timing_leppa_wait)
        self.spin_ball_press.setValue(config.timing_ball_press_wait)
        self._load_live_pp()

    def apply_to_config(self, config):
        config.ditto_patrol_time = self.spin_patrol.value()
        config.ditto_key_attack = self.edit_atk_key.text().strip()
        config.ditto_name_attack = self.edit_atk_name.text().strip()
        config.pp_max_swipe = self.edit_atk_pp.text().strip()
        config.pp_threshold_swipe = self.spin_thresh_swipe.value()
        config.ditto_key_sleep = self.edit_slp_key.text().strip()
        config.ditto_name_sleep = self.edit_slp_name.text().strip()
        config.pp_max_spore = self.edit_slp_pp.text().strip()
        config.pp_threshold_spore = self.spin_thresh_spore.value()
        config.ditto_key_ball = self.edit_ball.text().strip()
        config.ditto_key_potion = self.edit_potion.text().strip()
        config.ditto_key_leppa = self.edit_leppa.text().strip()
        config.auto_heal_hp = self.chk_heal_hp.isChecked()
        config.auto_heal_pp = self.chk_heal_pp.isChecked()
        config.timing_ball_wait = self.spin_ball_wait.value()
        config.timing_capture_settle = self.spin_settle.value()
        config.timing_leppa_wait = self.spin_leppa_wait.value()
        config.timing_ball_press_wait = self.spin_ball_press.value()
        self._save_live_pp()
