import os
import glob
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QPlainTextEdit, QComboBox, QLabel, QApplication
)
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#c792ea"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            "def", "class", "import", "from", "return", "if", "elif", "else",
            "for", "while", "try", "except", "finally", "with", "as", "in",
            "not", "and", "or", "True", "False", "None", "self", "raise", "break",
            "continue", "pass", "yield", "lambda", "global", "nonlocal", "assert"
        ]
        for pattern in [r"\b" + kw + r"\b" for kw in keywords]:
            self.highlighting_rules.append((QRegularExpression(pattern), keyword_format))

        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#c3e88d"))
        self.highlighting_rules.append((QRegularExpression(r'".*?"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'.*?'"), string_format))

        # Decorators
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor("#ffcb6b"))
        self.highlighting_rules.append((QRegularExpression(r"@[a-zA-Z_][a-zA-Z0-9_]*"), decorator_format))

        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#f78c6c"))
        self.highlighting_rules.append((QRegularExpression(r"\b[0-9]+(\.[0-9]+)?\b"), number_format))

        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#546e7a"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r"#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)


class BrainViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("🧠 Archivo:"))

        self.combo_files = QComboBox()
        self.combo_files.currentTextChanged.connect(self.load_selected_file)
        toolbar.addWidget(self.combo_files, stretch=1)

        btn_refresh = QPushButton("🔄")
        btn_refresh.setFixedSize(30, 26)
        btn_refresh.clicked.connect(self.refresh_file_list)
        toolbar.addWidget(btn_refresh)

        btn_copy = QPushButton("📋 Copiar")
        btn_copy.setFixedHeight(26)
        btn_copy.clicked.connect(self.copy_code)
        toolbar.addWidget(btn_copy)

        layout.addLayout(toolbar)

        # Editor
        self.code_edit = QPlainTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setFont(QFont("Consolas", 10))
        self.code_edit.setStyleSheet(
            "background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px;"
        )
        self.highlighter = PythonHighlighter(self.code_edit.document())

        layout.addWidget(self.code_edit)

        self.refresh_file_list()

    def refresh_file_list(self):
        base = os.path.dirname(os.path.abspath(__file__))
        # Go up to workspace root
        root = os.path.abspath(os.path.join(base, "..", "..", "..", ".."))
        patterns = [
            os.path.join(root, "src", "*.py"),
            os.path.join(root, "src", "modes", "*.py"),
            os.path.join(root, "*.py"),
        ]
        files = []
        for p in patterns:
            for f in sorted(glob.glob(p)):
                rel = os.path.relpath(f, root)
                files.append(rel)

        current = self.combo_files.currentText()
        self.combo_files.blockSignals(True)
        self.combo_files.clear()
        self.combo_files.addItems(files)
        if current in files:
            self.combo_files.setCurrentText(current)
        self.combo_files.blockSignals(False)
        self.load_selected_file(self.combo_files.currentText())

    def load_selected_file(self, rel_path: str):
        if not rel_path:
            return
        base = os.path.dirname(os.path.abspath(__file__))
        root = os.path.abspath(os.path.join(base, "..", "..", "..", ".."))
        full = os.path.join(root, rel_path)
        if os.path.exists(full):
            try:
                with open(full, "r", encoding="utf-8") as f:
                    self.code_edit.setPlainText(f.read())
            except Exception as e:
                self.code_edit.setPlainText(f"# Error reading {rel_path}: {e}")

    def copy_code(self):
        QApplication.clipboard().setText(self.code_edit.toPlainText())
