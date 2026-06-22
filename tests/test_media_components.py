import os
import sys
import unittest

from PyQt5.QtWidgets import QApplication

from components.pdf_viewer import PdfViewer
from components.video_viewer import VideoViewer


app = QApplication.instance() or QApplication(sys.argv)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestMediaComponents(unittest.TestCase):
    def test_pdf_component_loads_and_zooms(self):
        viewer = PdfViewer()
        path = os.path.join(PROJECT_ROOT, "public", "sample.pdf")

        self.assertTrue(viewer.load_document(path))
        self.assertIsNotNone(viewer.document)
        initial_zoom = viewer.zoom
        viewer.zoom_in()
        self.assertGreater(viewer.zoom, initial_zoom)

        viewer.clear()
        self.assertIsNone(viewer.document)

    def test_video_component_owns_playback_controls(self):
        viewer = VideoViewer()
        self.assertEqual(viewer.volume_slider.value(), 70)
        viewer.set_volume(35)
        self.assertEqual(viewer.media_player.volume(), 35)
        self.assertEqual(viewer.time_label.text(), "00:00 / 00:00")
        viewer.stop()


if __name__ == "__main__":
    unittest.main()
