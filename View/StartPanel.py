import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QGraphicsDropShadowEffect,
                             QMessageBox)
from PyQt6.QtGui import QColor, QMouseEvent, QPainter, QPixmap
from PyQt6.QtCore import Qt


class StartPanel(QWidget):
    def __init__(self, mainframe):
        super().__init__()
        self.mainframe = mainframe
        self.setObjectName("StartPanel")

        # -----------------------------------------------------------------
        # TẢI ẢNH NỀN (GIỮ NGUYÊN CHẤT LƯỢNG, KHÔNG KÉO GIÃN)
        # -----------------------------------------------------------------
        if hasattr(sys, '_MEIPASS'):
            goc_du_lieu = sys._MEIPASS  # type: ignore
        else:
            thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
            goc_du_lieu = os.path.dirname(thu_muc_hien_tai)

        duong_dan_anh_nen = os.path.join(goc_du_lieu, "asset", "background.jpg").replace("\\", "/")
        self._anh_nen = QPixmap(duong_dan_anh_nen)

        # -----------------------------------------------------------------
        # LAYOUT CHÍNH
        # -----------------------------------------------------------------
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 80, 10, 10)
        self.main_layout.setSpacing(40)

        # HEADER
        self.lbl_header = QLabel()
        self.lbl_header.setObjectName("lbl_header")
        self.lbl_header.setText(
            '<p align="center"><span style="font-family:\'Montserrat\', \'Segoe UI\'; '
            'font-size:42pt; font-weight:bold; color:#ffffff; '
            'text-shadow: 0 0 5px #fff, 0 0 10px #ff0055, 0 0 20px #ff0055, 0 0 40px #ff0055;">'
            'DANH SÁCH BÀI TẬP</span></p>'
        )
        self.lbl_header.setMargin(10)

        hieu_ung_neon = QGraphicsDropShadowEffect(self)
        hieu_ung_neon.setBlurRadius(25)
        hieu_ung_neon.setColor(QColor("#ff0055"))
        hieu_ung_neon.setOffset(0, 0)
        self.lbl_header.setGraphicsEffect(hieu_ung_neon)

        self.main_layout.addWidget(self.lbl_header, alignment=Qt.AlignmentFlag.AlignHCenter)

        # NÚT BẮT ĐẦU
        self.btn_bat_dau = QPushButton("BẮT ĐẦU")
        self.btn_bat_dau.setObjectName("btn_bat_dau")
        self.btn_bat_dau.clicked.connect(lambda: self.xu_ly_vao_bai("Exercises"))
        self.main_layout.addWidget(self.btn_bat_dau, alignment=Qt.AlignmentFlag.AlignCenter)

        # AUTHOR
        self.lbl_author = QLabel("Developed by Kousujo")
        self.lbl_author.setObjectName("lbl_author")
        self.lbl_author.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_author.mousePressEvent = self.hien_thi_thong_tin_tac_gia

        self.layout_day = QHBoxLayout()
        self.layout_day.addStretch()
        self.layout_day.addWidget(self.lbl_author)
        self.main_layout.addLayout(self.layout_day)

        self.thiet_lap_stylesheets()

    # ponytail: paintEvent vẽ ảnh nền giữ tỷ lệ thay vì dùng background-image CSS (bị stretch)
    def paintEvent(self, event):
        painter = QPainter(self)
        if not self._anh_nen.isNull():
            # Vẽ ảnh với KeepAspectRatioByExpanding — fill đầy widget, giữ tỷ lệ, không méo
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            scaled = self._anh_nen.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            # Cắt ảnh từ góc trên trái để phủ toàn bộ widget
            x = (scaled.width() - self.width()) // 2
            y = (scaled.height() - self.height()) // 2
            painter.drawPixmap(self.rect(), scaled, scaled.rect().adjusted(x, y, x, y))

    def resizeEvent(self, event):
        self.update()
        super().resizeEvent(event)

    def hien_thi_thong_tin_tac_gia(self, ev: QMouseEvent | None):  # type: ignore[override]
        QMessageBox.about(self, "Thông tin tác giả",
            "<p style='font-size:16pt; line-height:2;'>"
            "<b>Tên:</b> Ưng Nguyễn Tiến Thành (Kousujo)<br>"
            "<b>Lớp:</b> 25CNTT2</p>")

    def thiet_lap_stylesheets(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #161925;
                color: #00f0ff; 
                font-family: 'Segoe UI', sans-serif;
                font-size: 15pt;
                font-weight: bold;
                border: 2px solid #00f0ff;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                color: #ffffff;
                background-color: #ff0055; 
                border: 2px solid #ffffff; 
            }
            QPushButton:pressed {
                background-color: #9d00ff;
                border: 2px solid #9d00ff;
            }

            #btn_bat_dau {
                font-size: 28pt;
                padding: 30px 100px;
                min-width: 300px;
                border-radius: 20px;
                letter-spacing: 6px;
                border: 3px solid #00f0ff;
            }
            #btn_bat_dau:hover {
                background-color: #ff0055;
                border: 3px solid #ffffff;
            }

            #lbl_author {
                font-family: 'Segoe UI', sans-serif;
                font-size: 20pt;
                font-weight: bold;
                color: #F2F2F2;
                letter-spacing: 1px;
                padding: 70px 15px 15px 0px;
            }
            #lbl_author:hover {
                color: #00f0ff;
            }
        """)

    def xu_ly_vao_bai(self, ten_man_hinh):
        self.mainframe.showScreen(ten_man_hinh)