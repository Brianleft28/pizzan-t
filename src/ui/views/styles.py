# QSS Dark Cyberpunk / Modern Theme for PizzaHunter

APP_STYLESHEET = """
QMainWindow {
    background-color: #12141a;
    color: #e0e6ed;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
}

QWidget {
    font-size: 13px;
    color: #c9d1d9;
}

/* Push Buttons */
QPushButton {
    background-color: #21262d;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: bold;
    color: #c9d1d9;
}

QPushButton:hover {
    background-color: #30363d;
    border-color: #8b949e;
}

QPushButton:pressed {
    background-color: #161b22;
}

/* Big Start/Stop Button */
QPushButton#startStopButton {
    background-color: #238636;
    color: #ffffff;
    font-size: 16px;
    font-weight: 900;
    border: none;
    border-radius: 8px;
    padding: 12px;
}

QPushButton#startStopButton:hover {
    background-color: #2ea043;
}

QPushButton#startStopButton[running="true"] {
    background-color: #da3633;
}

QPushButton#startStopButton[running="true"]:hover {
    background-color: #f85149;
}

/* QTabWidget */
QTabWidget::pane {
    border: 1px solid #30363d;
    border-radius: 6px;
    background-color: #161b22;
    top: -1px;
}

QTabBar::tab {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 4px;
    color: #8b949e;
    font-weight: 600;
}

QTabBar::tab:selected {
    background-color: #161b22;
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}

QTabBar::tab:hover:!selected {
    background-color: #21262d;
    color: #c9d1d9;
}

/* Inputs & ComboBoxes */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px 8px;
    color: #e6edf3;
    selection-background-color: #1f6feb;
}

QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #58a6ff;
}

/* CheckBox */
QCheckBox {
    spacing: 8px;
    color: #c9d1d9;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #30363d;
    background-color: #0d1117;
}

QCheckBox::indicator:checked {
    background-color: #1f6feb;
    border-color: #58a6ff;
}

/* GroupBox & Frames */
QGroupBox {
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
    color: #58a6ff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 4px;
}

QFrame#cardFrame {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
}

/* ScrollBar */
QScrollBar:vertical {
    background: #0d1117;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #30363d;
    min-height: 20px;
    border-radius: 5px;
}

QScrollBar::handle:vertical:hover {
    background: #58a6ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Status Bar */
QFrame#statsBar {
    background-color: #0d1117;
    border-top: 1px solid #30363d;
    padding: 4px;
}

QLabel#statsLabel {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    color: #7ee787;
    font-weight: bold;
}
"""
