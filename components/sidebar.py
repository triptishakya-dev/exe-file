from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor, QPainter, QBrush, QPen, QPainterPath
from PyQt5.QtCore import Qt, pyqtSignal, pyqtProperty, QPropertyAnimation, QEasingCurve, QRect, QPoint, QSize
from config.constants import CARD_BG, CARD_HOVER, CARD_SELECTED, TEXT_COLOR

class ImageCard(QWidget):
    clicked = pyqtSignal(str, object)  # filepath, self

    def __init__(self, filepath, filename, date_str, parent=None):
        super().__init__(parent)
        self.filepath = filepath
        self.selected = False
        self._bg_color = CARD_BG
        self.thumb_loaded = False

        self.setFixedSize(280, 100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(80, 80)

        # Set initial rounded placeholder
        placeholder = QPixmap(80, 80)
        placeholder.fill(Qt.GlobalColor.transparent)
        painter = QPainter(placeholder)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#333333"), 2))
        painter.setBrush(QBrush(QColor("#1a1a1a")))
        painter.drawRoundedRect(1, 1, 78, 78, 8, 8)
        painter.end()
        self.thumb_label.setPixmap(placeholder)
        self.thumb_label.setStyleSheet("background-color: transparent;")

        layout.addWidget(self.thumb_label)

        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        fm = self.fontMetrics()
        elided_name = fm.elidedText(filename, Qt.TextElideMode.ElideRight, 150)

        self.name_label = QLabel(elided_name)
        self.name_label.setStyleSheet(f"color: {TEXT_COLOR}; font-weight: bold; font-size: 14px; background: transparent;")

        self.date_label = QLabel(date_str)
        self.date_label.setStyleSheet("color: #888888; font-size: 12px; background: transparent;")

        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.date_label)

        layout.addLayout(text_layout)

        self.anim = QPropertyAnimation(self, b"bgColor")
        self.anim.setDuration(150)
        self.anim.setEasingCurve(QEasingCurve.Type.OutQuad)

    def set_thumbnail(self, pixmap):
        self.thumb_label.setPixmap(pixmap)
        self.thumb_loaded = True

    @pyqtProperty(QColor)
    def bgColor(self):
        return self._bg_color

    @bgColor.setter
    def bgColor(self, color):
        self._bg_color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self._bg_color))
        if self.selected:
            painter.setPen(QPen(QColor("#38bdf8"), 2))
        else:
            painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 10, 10)

    def get_mainwindow(self):
        p = self.parent()
        while p:
            if isinstance(p, QMainWindow):
                return p
            p = p.parent()
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.pos()
            self.mouse_pressed_selected = self.selected

            modifiers = QApplication.keyboardModifiers()
            has_mod = bool(modifiers & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier | Qt.KeyboardModifier.ShiftModifier))

            print(f"Debug Card Press: {self.name_label.text()} (selected={self.selected}, has_mod={has_mod})")
            if self.selected and not has_mod:
                print(f"Debug Card Press: Deferring click emission for {self.name_label.text()}")
                pass
            else:
                self.clicked.emit(self.filepath, self)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if hasattr(self, 'drag_start_pos'):
                if (event.pos() - self.drag_start_pos).manhattanLength() >= QApplication.startDragDistance():
                    if self.selected:
                        mw = self.get_mainwindow()
                        if mw:
                            mw.start_drag_operations(self)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if hasattr(self, 'drag_start_pos'):
                diff = (event.pos() - self.drag_start_pos).manhattanLength()
                print(f"Debug Card Release: {self.name_label.text()} (drag_diff={diff})")
                if diff < QApplication.startDragDistance():
                    modifiers = QApplication.keyboardModifiers()
                    has_mod = bool(modifiers & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier | Qt.KeyboardModifier.ShiftModifier))
                    if self.selected and not has_mod and getattr(self, 'mouse_pressed_selected', False):
                        print(f"Debug Card Release: Triggering deferred click for {self.name_label.text()}")
                        self.clicked.emit(self.filepath, self)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        if not self.selected:
            self.anim.stop()
            self.anim.setStartValue(self._bg_color)
            self.anim.setEndValue(CARD_HOVER)
            self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.selected:
            self.anim.stop()
            self.anim.setStartValue(self._bg_color)
            self.anim.setEndValue(CARD_BG)
            self.anim.start()
        super().leaveEvent(event)

    def set_selected(self, selected):
        self.selected = selected
        self.anim.stop()
        if selected:
            self.bgColor = CARD_SELECTED
        else:
            self.bgColor = CARD_BG


class SidebarListWidget(QWidget):
    selection_box_changed = pyqtSignal(QRect)
    selection_box_finished = pyqtSignal(QRect)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rubber_band = None
        self.origin = QPoint()
        self.setMouseTracking(True)

    def get_mainwindow(self):
        p = self.parent()
        while p:
            if isinstance(p, QMainWindow):
                return p
            p = p.parent()
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.origin = event.pos()
            if not self.rubber_band:
                from PyQt5.QtWidgets import QRubberBand
                self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

            modifiers = QApplication.keyboardModifiers()
            has_mod = bool(modifiers & (Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.MetaModifier | Qt.KeyboardModifier.ShiftModifier))
            if not has_mod:
                mw = self.get_mainwindow()
                if mw:
                    mw.clear_sidebar_selection()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rubber_band and self.rubber_band.isVisible():
            rect = QRect(self.origin, event.pos()).normalized()
            self.rubber_band.setGeometry(rect)
            self.selection_box_changed.emit(rect)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rubber_band and self.rubber_band.isVisible():
            self.rubber_band.hide()
            rect = QRect(self.origin, event.pos()).normalized()
            self.selection_box_finished.emit(rect)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
