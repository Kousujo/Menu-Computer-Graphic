# exercises/ExerciseListPanel.py
# ponytail: hybrid QWebEngineView + QWebChannel bridge, HTML in external file.

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import Qt, QObject, pyqtSlot, QUrl
from styles.voltagent_styles import Color
import os


# ─── Chapter metadata ────────────────────────────────────────────────────────

_CHAPTERS = [
    (1, "CÁC YẾU TỐ CƠ SỞ CỦA ĐỒ HỌA",
     "Thuật toán: DDA, Bresenham, Circle, Oval...", "📐", True),
    (2, "TÔ MÀU",
     "Flood Fill, Scanline", "🎨", True),
    (3, "BIẾN ĐỔI ĐỒ HỌA 2D",
     "Translation, Rotation, Scaling", "🔄", False),
    (4, "BIẾN ĐỔI 3D & PROJECTION",
     "3D Transform, Perspective", "🧊", False),
    (5, "QUAN SÁT ĐỒ HỌA 3D",
     "Camera, Viewport", "👁️", False),
    (6, "ĐƯỜNG CONG & MẶT CONG",
     "Bezier, B-Spline, Surface", "📈", False),
    (7, "KHỬ CHE KHUẤT",
     "Z-Buffer, Painter", "🔲", False),
]

# map: "Chương 1" → "Chuong_1"
_CHAPTER_TO_SCREEN = {
    f"Chương {i}": f"Chuong_{i}"
    for i in range(1, 8)
}


# ─── Python ↔ JavaScript bridge ──────────────────────────────────────────────

class UIBridge(QObject):
    """Bridge object exposed to JavaScript via QWebChannel as 'pyBridge'."""

    def __init__(self, mainframe):
        super().__init__()
        self.mainframe = mainframe

    @pyqtSlot(str)
    def open_chapter(self, chapter_name: str):
        """Called from JS when an active chapter card is clicked."""
        screen = _CHAPTER_TO_SCREEN.get(chapter_name)
        if screen and hasattr(self.mainframe, 'showScreen'):
            self.mainframe.showScreen(screen)

    @pyqtSlot()
    def show_author_info(self):
        """Called from JS when the author footer link is clicked."""
        QMessageBox.about(
            None, "Thông tin tác giả",
            "<p style='font-size:16pt; line-height:2;'>"
            "<b>Tên:</b> Ưng Nguyễn Tiến Thành (Kousujo)<br>"
            "<b>Lớp:</b> 25CNTT2</p>"
        )


# ─── HTML payload loader ─────────────────────────────────────────────────────

def _html_path() -> str:
    """Return absolute path to the external HTML file shipped with the panel."""
    return os.path.join(os.path.dirname(__file__), "exercise_list_panel.html")


# ─── Main Panel ──────────────────────────────────────────────────────────────

class ExerciseListPanel(QWidget):
    """Main menu — hybrid QWebEngineView frontend + Python QWebChannel bridge."""

    def __init__(self, mainframe):
        super().__init__()
        self.mainframe = mainframe

        self.setObjectName("ExerciseListPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {Color.CANVAS};")

        # ── Bridge ───────────────────────────────────────────────────────
        self.bridge = UIBridge(mainframe)

        # ── Web channel ──────────────────────────────────────────────────
        self.channel = QWebChannel()
        self.channel.registerObject("pyBridge", self.bridge)

        # ── Web engine view ──────────────────────────────────────────────
        self.web_view = QWebEngineView()
        page = self.web_view.page()
        if page is not None:
            page.setWebChannel(self.channel)
        self.web_view.load(QUrl.fromLocalFile(_html_path()))

        # ── Layout ───────────────────────────────────────────────────────
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self.web_view)