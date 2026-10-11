from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import pyqtSignal

class TabGeneral(QWidget):
    save_requested = pyqtSignal()
    install_roms_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        form = QFormLayout()
        form.setSpacing(10)

        self.edit_webhook = QLineEdit()
        self.edit_webhook.setPlaceholderText("https://discord.com/api/webhooks/...")
        form.addRow(QLabel("🔗 Discord Webhook:"), self.edit_webhook)

        self.edit_jwt = QLineEdit()
        self.edit_jwt.setPlaceholderText("NestJS JWT Token")
        self.edit_jwt.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow(QLabel("🔑 Webhook JWT:"), self.edit_jwt)

        self.spin_ocr = QSpinBox()
        self.spin_ocr.setRange(1, 20)
        self.spin_ocr.setValue(6)
        form.addRow(QLabel("🔍 OCR Retries:"), self.spin_ocr)

        layout.addLayout(form)
        layout.addSpacing(10)

        self.btn_save = QPushButton("💾 GUARDAR CONFIGURACIÓN GENERAL")
        self.btn_save.setFixedHeight(36)
        self.btn_save.setStyleSheet("background-color: #1f6feb; color: white;")
        self.btn_save.clicked.connect(self.save_requested.emit)
        layout.addWidget(self.btn_save)

        self.btn_roms = QPushButton("📦 INSTALAR ROMS (WIP)")
        self.btn_roms.setFixedHeight(36)
        self.btn_roms.setStyleSheet("background-color: #d29922; color: black; font-weight: bold;")
        self.btn_roms.clicked.connect(self.install_roms_clicked.emit)
        layout.addWidget(self.btn_roms)

        layout.addStretch()

    def load_from_config(self, config):
        self.edit_webhook.setText(config.discord_webhook)
        self.edit_jwt.setText(config.webhook_jwt)
        self.spin_ocr.setValue(config.ocr_retries)

    def apply_to_config(self, config):
        config.discord_webhook = self.edit_webhook.text().strip()
        config.webhook_jwt = self.edit_jwt.text().strip()
        config.ocr_retries = self.spin_ocr.value()
