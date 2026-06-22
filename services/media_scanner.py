import os
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal
from config.constants import ALL_EXTS

class ImageWorker(QThread):
    file_found = pyqtSignal(str, str, str) # filepath, filename, date_str
    finished_loading = pyqtSignal()

    def __init__(self, folder_path, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.running = True

    def stop(self):
        self.running = False
        self.requestInterruption()
        self.wait()

    def run(self):
        try:
            files = [f for f in os.listdir(self.folder_path)
                     if f.lower().endswith(ALL_EXTS)]
        except Exception:
            files = []

        files.sort()

        for filename in files:
            if not self.running:
                break
            filepath = os.path.join(self.folder_path, filename)
            try:
                stat = os.stat(filepath)
                dt = datetime.fromtimestamp(stat.st_ctime)
                date_str = dt.strftime("%Y-%m-%d %H:%M")
                self.file_found.emit(filepath, filename, date_str)
            except Exception as e:
                print(f"Error scanning {filepath}: {e}")

        self.finished_loading.emit()
