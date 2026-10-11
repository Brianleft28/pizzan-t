from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel

class StatsBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statsBar")
        self.setFixedHeight(32)
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        self.label_stats = QLabel("🎯 Inactivo | Enc: 0 | Session: 0 | Dittos: 0 | Rate: 0.0/min | ⏱️ 00:00:00")
        self.label_stats.setObjectName("statsLabel")
        layout.addWidget(self.label_stats)
        layout.addStretch()

    def update_stats(self, stats: dict):
        mode = stats.get("mode", "Horda")
        enc = stats.get("encounters", 0)
        sess = stats.get("session", 0)
        dittos = stats.get("dittos", 0)
        rate = stats.get("rate", 0.0)
        elapsed = stats.get("elapsed", "00:00:00")
        running = stats.get("running", False)

        color = "#7ee787" if running else "#8b949e"
        status_text = (
            f"🎯 {mode} | Enc: {enc} | Sess: {sess} | "
            f"Dittos: {dittos} | Rate: {rate:.1f}/min | ⏱️ {elapsed}"
        )
        self.label_stats.setText(status_text)
        self.label_stats.setStyleSheet(f"color: {color};")

    def reset(self):
        self.label_stats.setText("🎯 Inactivo | Enc: 0 | Session: 0 | Dittos: 0 | Rate: 0.0/min | ⏱️ 00:00:00")
        self.label_stats.setStyleSheet("color: #8b949e;")
