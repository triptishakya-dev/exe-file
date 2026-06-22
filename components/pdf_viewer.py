import fitz
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget
from config.styles import MEDIA_BUTTON_STYLE


class PdfViewer(QWidget):
    """Self-contained PDF document, navigation, rendering and zoom."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.document = None
        self.current_page = 0
        self.zoom = 1.2
        self.setStyleSheet("background-color: #121212;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        controls = QWidget()
        controls.setFixedHeight(50)
        controls.setStyleSheet("background-color:#1e1e1e; border-bottom:1px solid #333;")
        controls_layout = QHBoxLayout(controls)

        self.previous_button = QPushButton("◀ Prev")
        self.page_label = QLabel("Page 0 of 0")
        self.next_button = QPushButton("Next ▶")
        self.zoom_out_button = QPushButton("🔍-")
        self.zoom_label = QLabel("100%")
        self.zoom_in_button = QPushButton("🔍+")

        controls_layout.addWidget(self.previous_button)
        controls_layout.addWidget(self.page_label)
        controls_layout.addWidget(self.next_button)
        controls_layout.addStretch()
        controls_layout.addWidget(self.zoom_out_button)
        controls_layout.addWidget(self.zoom_label)
        controls_layout.addWidget(self.zoom_in_button)
        layout.addWidget(controls)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color:#121212; padding:10px;")
        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)

        self.previous_button.clicked.connect(self.previous_page)
        self.next_button.clicked.connect(self.next_page)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.zoom_in_button.clicked.connect(self.zoom_in)

        for button in (self.previous_button, self.next_button, self.zoom_out_button, self.zoom_in_button):
            button.setStyleSheet(MEDIA_BUTTON_STYLE)
        self.page_label.setStyleSheet("color:#e0e0e0; font-weight:bold;")
        self.zoom_label.setStyleSheet("color:#a0a0a0;")

    def load_document(self, filepath):
        self.clear()
        try:
            self.document = fitz.open(filepath)
            self.current_page = 0
            self.zoom = 1.2
            self.render_page()
            return True
        except Exception as error:
            self.image_label.setText(f"Failed to load PDF: {error}")
            return False

    def clear(self):
        if self.document:
            self.document.close()
        self.document = None

    def render_page(self):
        if not self.document:
            return
        page_count = len(self.document)
        if not page_count:
            self.page_label.setText("No pages")
            return

        self.current_page = max(0, min(self.current_page, page_count - 1))
        self.page_label.setText(f"Page {self.current_page + 1} of {page_count}")
        self.zoom_label.setText(f"{int(self.zoom * 100)}%")
        self.previous_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < page_count - 1)

        try:
            page = self.document.load_page(self.current_page)
            pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom, self.zoom))
            image_format = QImage.Format.Format_RGBA8888 if pix.alpha else QImage.Format.Format_RGB888
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, image_format)
            self.image_label.setPixmap(QPixmap.fromImage(image))
        except Exception as error:
            self.image_label.setText(f"Error rendering page: {error}")

    def previous_page(self):
        if self.document and self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def next_page(self):
        if self.document and self.current_page < len(self.document) - 1:
            self.current_page += 1
            self.render_page()

    def zoom_in(self):
        if self.document and self.zoom < 4.0:
            self.zoom += 0.2
            self.render_page()

    def zoom_out(self):
        if self.document and self.zoom > 0.4:
            self.zoom -= 0.2
            self.render_page()
