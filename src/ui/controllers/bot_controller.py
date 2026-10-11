import time
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from src.bot_main import ShinyBot

class BotWorker(QObject):
    log_received = pyqtSignal(str, str)
    stats_updated = pyqtSignal(dict)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.bot = None
        self._running = False

    def start_bot(self):
        class LogProxy:
            def __init__(self, signal_emitter):
                self.signal_emitter = signal_emitter
                self.buffer = []

            def insert(self, index, text, category="INFO"):
                self.buffer.append(text)
                self.signal_emitter.emit(text, category)

            def see(self, index):
                pass

            def delete(self, start, end):
                self.buffer.clear()

            def get(self, start, end):
                return "".join(self.buffer)

        proxy = LogProxy(self.log_received)
        self.bot = ShinyBot(log_widget=proxy)
        self.bot.start()
        self._running = True

        while self._running and self.bot and self.bot.running:
            time.sleep(1)
            # Emit stats
            try:
                enc = self.bot.encounters
                sess = self.bot.session_encounters
                dittos = self.bot.session_dittos
                elapsed = self.bot.get_elapsed_time()
                elapsed_obj = self.bot.logger.start_time
                seconds = (datetime.now() - elapsed_obj).total_seconds()
                rate = (sess / (seconds / 60)) if seconds > 60 else 0
                mode = self.bot.config.get("mode", "Horda").capitalize()

                stats = {
                    "mode": mode,
                    "encounters": enc,
                    "session": sess,
                    "dittos": dittos,
                    "rate": rate,
                    "elapsed": elapsed,
                    "running": True
                }
                self.stats_updated.emit(stats)
            except Exception:
                pass

        if self.bot and self.bot.running:
            self.bot.stop()
        self.finished.emit()

    def stop_bot(self):
        self._running = False
        if self.bot:
            self.bot.stop()
            self.bot = None


class BotController(QObject):
    log_signal = pyqtSignal(str, str)
    stats_signal = pyqtSignal(dict)
    bot_stopped = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    def is_running(self):
        return self.worker is not None and self.worker._running

    def start(self):
        if self.is_running():
            return

        self.thread = QThread()
        self.worker = BotWorker()
        self.worker.moveToThread(self.thread)

        self.worker.log_received.connect(self.log_signal.emit)
        self.worker.stats_updated.connect(self.stats_signal.emit)

        self.thread.started.connect(self.worker.start_bot)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.bot_stopped.emit)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def stop(self):
        if self.worker:
            self.worker.stop_bot()
