from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QPlainTextEdit, QComboBox, QCheckBox, QApplication
)
from PyQt6.QtGui import QTextCharFormat, QColor, QFont
from PyQt6.QtCore import pyqtSlot

CATEGORY_COLORS = {
    "INFO":    "#82aaff",
    "ACTION":  "#89ddff",
    "SUCCESS": "#c3e88d",
    "WARN":    "#ffcb6b",
    "FATAL":   "#ff5370",
    "BATTLE":  "#c792ea",
    "MAP":     "#b2ccd6",
    "HEAL":    "#a5d6a7",
    "DEBUG":   "#546e7a",
    "HEADER":  "#f78c6c",
    "PHASE":   "#ffcb6b",
    "BRAIN":   "#82aaff",
}

class LoggerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_expanded = True
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(4)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        self.btn_toggle = QPushButton("▼ LOGGER")
        self.btn_toggle.setFixedHeight(26)
        self.btn_toggle.clicked.connect(self.toggle_collapse)

        self.combo_verb = QComboBox()
        self.combo_verb.addItems(["Normal", "Quiet", "Debug"])
        self.combo_verb.setFixedHeight(26)

        self.chk_autoscroll = QCheckBox("Auto-scroll")
        self.chk_autoscroll.setChecked(True)

        self.btn_clear = QPushButton("🗑️")
        self.btn_clear.setFixedSize(30, 26)
        self.btn_clear.setToolTip("Limpiar logs")
        self.btn_clear.clicked.connect(self.clear_logs)

        self.btn_copy = QPushButton("📋")
        self.btn_copy.setFixedSize(30, 26)
        self.btn_copy.setToolTip("Copiar últimas líneas")
        self.btn_copy.clicked.connect(self.copy_logs)

        toolbar.addWidget(self.btn_toggle)
        toolbar.addWidget(self.combo_verb)
        toolbar.addWidget(self.chk_autoscroll)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_clear)
        toolbar.addWidget(self.btn_copy)

        layout.addLayout(toolbar)

        # Log Text Box
        self.text_box = QPlainTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setFont(QFont("Consolas", 10))
        self.text_box.setStyleSheet(
            "background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px;"
        )
        self.text_box.setMaximumBlockCount(2000)
        self.text_box.setFixedHeight(160)

        layout.addWidget(self.text_box)

    @pyqtSlot(str, str)
    def append_log(self, text: str, category: str = "INFO"):
        verb = self.combo_verb.currentText()
        if verb == "Quiet" and category not in ("SUCCESS", "FATAL", "PHASE", "HEADER"):
            return
        if verb == "Normal" and category == "DEBUG":
            return

        cursor = self.text_box.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)

        fmt = QTextCharFormat()
        hex_color = CATEGORY_COLORS.get(category.upper(), "#c9d1d9")
        fmt.setForeground(QColor(hex_color))

        cursor.insertText(text.rstrip("\r\n") + "\n", fmt)

        if self.chk_autoscroll.isChecked():
            self.text_box.ensureCursorVisible()

    def toggle_collapse(self):
        self.is_expanded = not self.is_expanded
        self.text_box.setVisible(self.is_expanded)
        self.btn_toggle.setText("▼ LOGGER" if self.is_expanded else "▶ LOGGER")

    def clear_logs(self):
        self.text_box.clear()

    def copy_logs(self):
        text = self.text_box.toPlainText()
        lines = [l for l in text.split("\n") if l.strip()]
        last_10 = "\n".join(lines[-10:])
        if last_10:
            QApplication.clipboard().setText(last_10)
