from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSignal

class GridImageItem(QWidget):
    clicked = pyqtSignal(object)
    double_clicked = pyqtSignal(object)
    remove_requested = pyqtSignal(object)

    def __init__(self, filepath, parent=None):
        super().__init__(parent)
        self.filepath = filepath
        self.selected = False
        self.is_hovered = False
        self.single_mode = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumSize(40, 40)

        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: transparent;")

        self.pixmap = QPixmap(filepath)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.image_label)

        # Floating Remove Button
        self.remove_btn = QPushButton("✕", self)
        self.remove_btn.setFixedSize(24, 24)
        self.remove_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(239, 68, 68, 0.9);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(220, 38, 38, 1);
            }
        """)
        self.remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_btn.clicked.connect(self.on_remove_clicked)
        self.remove_btn.hide()

        self.update_image()

    def set_selected(self, selected):
        self.selected = selected
        self.update()

    def on_remove_clicked(self):
        self.remove_requested.emit(self)

    def update_image(self):
        if not self.pixmap.isNull():
            margin = 0 if self.single_mode else 10
            self.layout().setContentsMargins(margin, margin, margin, margin)

            w = max(10, self.width() - margin * 2)
            h = max(10, self.height() - margin * 2)
            scaled = self.pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()
        self.remove_btn.move(max(0, self.width() - self.remove_btn.width() - 8), 8)

    def enterEvent(self, event):
        self.is_hovered = True
        self.remove_btn.show()
        self.remove_btn.raise_()
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.remove_btn.hide()
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self)
        super().mouseDoubleClickEvent(event)



    def paintEvent(self, event):
        if self.single_mode:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self.selected:
            painter.setPen(QPen(QColor("#38bdf8"), 3))
            painter.setBrush(QBrush(QColor(56, 189, 248, 20)))
        elif self.is_hovered:
            painter.setPen(QPen(QColor("#38bdf8"), 1))
            painter.setBrush(QBrush(QColor("#262626")))
        else:
            painter.setPen(QPen(QColor("#333333"), 1))
            painter.setBrush(QBrush(QColor("#1a1a1a")))
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 8, 8)
        painter.end()
