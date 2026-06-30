# exercises/ExerciseListPanel.py
# ponytail: centralized QSS only, no inline styles. Layout follows MARGIN=24, SPACING=16.

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QMessageBox,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QMouseEvent, QColor
from PyQt6.QtCore import Qt
from styles.voltagent_styles import (
    Color, MARGIN, SPACING,
    qss_button_secondary, qss_card_feature,
    qss_label_eyebrow, qss_label_title, qss_label_body,
    qss_divider, qss_container_panel, qss_container_inner,
)


# ─── Chapter metadata ────────────────────────────────────────────────────────

_CHAPTERS = [
    # (index, title, subtitle, algo_line, emoji, enabled)
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

_LOCKED_SUFFIX = "  🔒"
_CHAPTER_SCREEN_NAMES = [
    "Chuong_1", "Chuong_2", "Chuong_3", "Chuong_4",
    "Chuong_5", "Chuong_6", "Chuong_7",
]


# ─── Double-Bezel card builder ───────────────────────────────────────────────

def _build_chapter_card(
    index: int,
    title: str,
    subtitle: str,
    emoji: str,
    enabled: bool,
    on_click,
) -> QFrame:
    """Build a chapter card using the Double-Bezel nested container pattern.

    Outer tray (qss_container_panel -> #containerPanel) wraps an inner core
    (qss_container_inner -> #containerInner) that holds the actual content.
    """
    tray = QFrame()
    tray.setObjectName("containerPanel")
    tray.setStyleSheet(qss_container_panel())
    tray_layout = QVBoxLayout(tray)
    tray_layout.setContentsMargins(8, 8, 8, 8)

    core = QFrame()
    core.setObjectName("containerInner")
    core.setStyleSheet(qss_container_inner())
    core_layout = QVBoxLayout(core)
    core_layout.setContentsMargins(16, 14, 16, 14)
    core_layout.setSpacing(4)

    # Row 1: emoji + eyebrow number
    header_row = QHBoxLayout()
    header_row.setContentsMargins(0, 0, 0, 0)
    header_row.setSpacing(8)

    lbl_emoji = QLabel(emoji)
    lbl_emoji.setStyleSheet("font-size: 20px; background: transparent; border: none;")
    header_row.addWidget(lbl_emoji)

    lbl_number = QLabel(f"CHƯƠNG {index}")
    lbl_number.setStyleSheet(qss_label_eyebrow())
    header_row.addWidget(lbl_number)
    header_row.addStretch()

    # Lock indicator for disabled chapters
    if not enabled:
        lbl_lock = QLabel("🔒")
        lbl_lock.setStyleSheet("font-size: 14px; background: transparent; border: none;")
        header_row.addWidget(lbl_lock)

    core_layout.addLayout(header_row)

    # Row 2: title
    display_title = title + (_LOCKED_SUFFIX if not enabled else "")
    lbl_title = QLabel(display_title)
    lbl_title.setStyleSheet(qss_label_title())
    lbl_title.setWordWrap(True)
    core_layout.addWidget(lbl_title)

    # Row 3: subtitle / algorithms list
    lbl_sub = QLabel(subtitle)
    lbl_sub.setStyleSheet(qss_label_body())
    lbl_sub.setWordWrap(True)
    core_layout.addWidget(lbl_sub)

    tray_layout.addWidget(core)

    # Shadow for enabled cards (premium depth)
    if enabled:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 120))
        shadow.setOffset(0, 4)
        tray.setGraphicsEffect(shadow)

    # Click handler
    if enabled:
        def _on_card_click(a0, idx=index):
            on_click(idx)
        tray.mousePressEvent = _on_card_click

    # Reduce opacity for locked chapters
    if not enabled:
        core.setStyleSheet(
            qss_container_inner().replace(
                "background-color: #1a1a1a;",
                "background-color: #1a1a1a; opacity: 0.55;"
            )
        )

    return tray


def _build_utility_card() -> QFrame:
    """Utilities card — Double-Bezel with two action buttons."""
    tray = QFrame()
    tray.setObjectName("containerPanel")
    tray.setStyleSheet(qss_container_panel())
    tray_layout = QVBoxLayout(tray)
    tray_layout.setContentsMargins(8, 8, 8, 8)

    core = QFrame()
    core.setObjectName("containerInner")
    core.setStyleSheet(qss_container_inner())
    core_layout = QVBoxLayout(core)
    core_layout.setContentsMargins(16, 14, 16, 14)
    core_layout.setSpacing(10)

    lbl_util = QLabel("TIỆN ÍCH")
    lbl_util.setStyleSheet(qss_label_eyebrow())
    core_layout.addWidget(lbl_util)

    btn_docs = QPushButton("📖  Open Documentation")
    btn_docs.setStyleSheet(qss_button_secondary())
    btn_docs.setCursor(Qt.CursorShape.PointingHandCursor)
    core_layout.addWidget(btn_docs)

    btn_reset = QPushButton("🧹  Reset System Canvas")
    btn_reset.setStyleSheet(qss_button_secondary())
    btn_reset.setCursor(Qt.CursorShape.PointingHandCursor)
    core_layout.addWidget(btn_reset)

    tray_layout.addWidget(core)
    return tray


def _build_info_card() -> QFrame:
    """Author info card — Double-Bezel with status labels."""
    tray = QFrame()
    tray.setObjectName("containerPanel")
    tray.setStyleSheet(qss_container_panel())
    tray_layout = QVBoxLayout(tray)
    tray_layout.setContentsMargins(8, 8, 8, 8)

    core = QFrame()
    core.setObjectName("containerInner")
    core.setStyleSheet(qss_container_inner())
    core_layout = QVBoxLayout(core)
    core_layout.setContentsMargins(16, 14, 16, 14)
    core_layout.setSpacing(6)

    lbl_info = QLabel("THÔNG TIN")
    lbl_info.setStyleSheet(qss_label_eyebrow())
    core_layout.addWidget(lbl_info)

    items = [
        ("📚", "Course: Computer Graphics"),
        ("👤", "Developer: Kousujo"),
    ]
    for icon, text in items:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        lbl_icon = QLabel(icon)
        lbl_icon.setStyleSheet("font-size: 14px; background: transparent; border: none;")
        lbl_text = QLabel(text)
        lbl_text.setStyleSheet(qss_label_body())
        row.addWidget(lbl_icon)
        row.addWidget(lbl_text)
        row.addStretch()
        core_layout.addLayout(row)

    # Status row with green dot
    status_row = QHBoxLayout()
    status_row.setContentsMargins(0, 0, 0, 0)
    status_row.setSpacing(8)
    lbl_dot = QLabel("●")
    lbl_dot.setStyleSheet(
        f"font-size: 12px; color: {Color.SUCCESS}; background: transparent; border: none;"
    )
    lbl_status = QLabel("System Status: Active")
    lbl_status.setStyleSheet(f"font-size: 10pt; color: {Color.SUCCESS}; background: transparent; border: none;")
    status_row.addWidget(lbl_dot)
    status_row.addWidget(lbl_status)
    status_row.addStretch()
    core_layout.addLayout(status_row)

    tray_layout.addWidget(core)
    return tray


# ─── Main Panel ──────────────────────────────────────────────────────────────

class ExerciseListPanel(QWidget):
    """Main menu — asymmetrical grid of chapter cards + right sidebar."""

    def __init__(self, mainframe):
        super().__init__()
        self.mainframe = mainframe

        self.setObjectName("ExerciseListPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"background-color: {Color.CANVAS};")

        # ── Root layout ──────────────────────────────────────────────────
        root = QVBoxLayout(self)
        root.setContentsMargins(MARGIN, MARGIN, MARGIN, MARGIN)
        root.setSpacing(SPACING)

        # ── 1. Header ─────────────────────────────────────────────────────
        lbl_header = QLabel("ĐỒ HỌA MÁY TÍNH")
        lbl_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_header.setStyleSheet(
            f"font-weight: 700; font-size: 32px; letter-spacing: 1px; "
            f"color: {Color.INK_STRONG}; background: transparent; border: none; "
            f"padding: 12px 0px;"
        )
        root.addWidget(lbl_header)

        # ── 2. Body: Left chapters + Right sidebar ─────────────────────────
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(SPACING)

        # ---- 2a. Left: Chapter grid (4 rows, 2 columns) -------------------
        ch_layout = QGridLayout()
        ch_layout.setContentsMargins(0, 0, 0, 0)
        ch_layout.setSpacing(12)

        for i, (index, title, subtitle, emoji, enabled) in enumerate(_CHAPTERS):
            card = _build_chapter_card(
                index, title, subtitle, emoji, enabled,
                on_click=self._on_chapter_click,
            )
            if index == 1:
                # Chapter 1: full-width row
                ch_layout.addWidget(card, 0, 0, 1, 2)
            else:
                # Others: pair in rows 1-3, columns 0-1
                row = 1 + (index - 2) // 2
                col = (index - 2) % 2
                ch_layout.addWidget(card, row, col)

        ch_layout.setRowStretch(0, 0)  # Ch1 auto
        ch_layout.setRowStretch(1, 1)
        ch_layout.setRowStretch(2, 1)
        ch_layout.setRowStretch(3, 1)
        ch_layout.setColumnStretch(0, 1)
        ch_layout.setColumnStretch(1, 1)

        # Wrap chapter grid in a container widget
        ch_widget = QWidget()
        ch_widget.setLayout(ch_layout)
        ch_widget.setStyleSheet("background: transparent; border: none;")
        body.addWidget(ch_widget, stretch=3)

        # ---- 2b. Right: Sidebar (fixed 300px) -----------------------------
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(0, 0, 0, 0)
        sidebar.setSpacing(SPACING)

        sidebar.addWidget(_build_utility_card())
        sidebar.addWidget(_build_info_card())
        sidebar.addStretch()

        sb_widget = QWidget()
        sb_widget.setFixedWidth(300)
        sb_widget.setLayout(sidebar)
        sb_widget.setStyleSheet("background: transparent; border: none;")
        body.addWidget(sb_widget, stretch=0)

        root.addLayout(body, stretch=1)

        # ── 3. Footer: Author label (right-aligned) ────────────────────────
        footer = QHBoxLayout()
        footer.setContentsMargins(0, 0, 0, 0)
        footer.addStretch()

        self.lbl_author = QLabel("Developed by Kousujo")
        self.lbl_author.setObjectName("lbl_author")
        self.lbl_author.setStyleSheet(qss_label_body())
        self.lbl_author.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_author.mousePressEvent = self._show_author_info
        footer.addWidget(self.lbl_author)

        root.addLayout(footer)

    # ── Handlers ─────────────────────────────────────────────────────────────

    def _on_chapter_click(self, index: int) -> None:
        """Navigate to the chapter screen."""
        screen_name = _CHAPTER_SCREEN_NAMES[index - 1]
        self.mainframe.showScreen(screen_name)

    def _show_author_info(self, ev: QMouseEvent | None) -> None:  # type: ignore[override]
        QMessageBox.about(self, "Thông tin tác giả",
            "<p style='font-size:16pt; line-height:2;'>"
            "<b>Tên:</b> Ưng Nguyễn Tiến Thành (Kousujo)<br>"
            "<b>Lớp:</b> 25CNTT2</p>")