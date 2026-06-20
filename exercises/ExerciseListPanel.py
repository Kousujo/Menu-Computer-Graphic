# exercises/ExerciseListPanel.py
import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                             QLabel, QPushButton, QScrollArea, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class ExerciseListPanel(QWidget):
    def __init__(self, mainframe):
        super().__init__()
        self.mainframe = mainframe
        self.setObjectName("ExerciseListPanel")
        
        # Thiết lập nền tổng thể (Hỗ trợ nạp StyledBackground cho QWidget)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # 1. KHỞI TẠO LAYOUT CHÍNH (QVBoxLayout)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 100, 10, 10)  # Giữ nguyên topMargin 100 từ file .ui
        self.main_layout.setSpacing(30)

        # 2. KHỞI TẠO THÀNH PHẦN HEADER
        self.lbl_header = QLabel()
        self.lbl_header.setObjectName("lbl_header")
        # Sử dụng chuỗi HTML kết hợp text-shadow neon nguyên bản của bạn
        self.lbl_header.setText(
            '<p align="center"><span style="font-family:\'Montserrat\', \'Segoe UI\'; '
            'font-size:42pt; font-weight:bold; color:#ffffff; '
            'text-shadow: 0 0 5px #fff, 0 0 10px #ff0055, 0 0 20px #ff0055, 0 0 40px #ff0055;">'
            'DANH SÁCH BÀI TẬP</span></p>'
        )
        self.lbl_header.setMargin(10)
        
        # Hiệu ứng đổ bóng lớp phụ (Neon DropShadow) cho tiêu đề
        hieu_ung_neon = QGraphicsDropShadowEffect(self)
        hieu_ung_neon.setBlurRadius(25)
        hieu_ung_neon.setColor(QColor("#ff0055"))
        hieu_ung_neon.setOffset(0, 0)
        self.lbl_header.setGraphicsEffect(hieu_ung_neon)
        
        # Đưa Header vào layout chính, căn giữa theo chiều ngang
        self.main_layout.addWidget(self.lbl_header, alignment=Qt.AlignmentFlag.AlignHCenter)

        # 3. KHỞI TẠO VÙNG CUỘN (QScrollArea)
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("scrollArea")
        self.scroll_area.setWidgetResizable(True)
        
        # Widget nội dung bên trong vùng cuộn
        self.scroll_widget = QWidget()
        self.scroll_widget.setObjectName("scrollAreaWidgetContents")
        
        # Grid Layout quản lý các nút bấm bài tập
        self.grid_layout = QGridLayout(self.scroll_widget)
        self.grid_layout.setContentsMargins(40, 0, 40, 0) # leftMargin và rightMargin là 40
        
        # Tạo Spacer 2 bên để ép các nút bấm gom vào cột giữa cân đối
        self.spacer_trai = QSpacerItem(80, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.spacer_phai = QSpacerItem(80, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.grid_layout.addItem(self.spacer_trai, 3, 0)
        self.grid_layout.addItem(self.spacer_phai, 3, 2)

        # Khởi tạo các nút bấm bài tập
        self.btn_bai1 = QPushButton("Bài 1 : Vẽ đoạn thẳng")
        self.btn_bai1.setObjectName("btn_bai1")
        self.btn_bai1.clicked.connect(lambda: self.xu_ly_vao_bai("Bai_1"))
        self.grid_layout.addWidget(self.btn_bai1, 3, 1) # Hàng 3, Cột 1
        
        self.btn_bai2 = QPushButton("Bài 2 : Vẽ hình tròn")
        self.btn_bai2.setObjectName("btn_bai2")
        self.btn_bai2.clicked.connect(lambda: self.xu_ly_vao_bai("Bai_2"))
        self.grid_layout.addWidget(self.btn_bai2, 4, 1) # Hàng 4, Cột 1

        self.btn_bai_3 = QPushButton("BÀI 3: KHẢO SÁT & VẼ ĐỒ THỊ HÀM SỐ")
        self.btn_bai_3.clicked.connect(lambda: self.mainframe.showScreen("Bai_3"))
        self.grid_layout.addWidget(self.btn_bai_3, 5, 1) # Hàng 5, Cột 1    

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        # 4. KHỞI TẠO THÀNH PHẦN AUTHOR Ở GÓC DƯỚI
        self.lbl_author = QLabel("Developed by Kousujo")
        self.lbl_author.setObjectName("lbl_author")
        
        # Tạo một Layout ngang phụ để đẩy chữ Author về góc phải đáy
        self.layout_day = QHBoxLayout()
        self.layout_day.addStretch()
        self.layout_day.addWidget(self.lbl_author)
        self.main_layout.addLayout(self.layout_day)

        # 5. THIẾT LẬP STYLESHEET CHUẨN HOÀN TOÀN
        self.thiet_lap_stylesheets()

    def thiet_lap_stylesheets(self):
        # -----------------------------------------------------------------
        # XỬ LÝ ĐƯỜNG DẪN ẢNH NỀN TƯƠNG THÍCH CHO CẢ .PY VÀ .EXE
        # -----------------------------------------------------------------
        if hasattr(sys, '_MEIPASS'):
            # Khi chạy từ file .exe độc lập, PyInstaller giải nén tài nguyên vào thư mục tạm này
            goc_du_lieu = sys._MEIPASS # type: ignore
        else:
            # Khi chạy dev bằng file .py thông thường, quay ngược lên thư mục gốc dự án
            thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
            goc_du_lieu = os.path.dirname(thu_muc_hien_tai)

        # Nối chuỗi chính xác đến file ảnh nằm trong folder 'asset' và sửa dấu gạch chéo cho CSS
        duong_dan_anh_nen = os.path.join(goc_du_lieu, "asset", "neon2.jpg").replace("\\", "/")

        self.setStyleSheet(f"""
            /* Hình nền tổng thể sử dụng đường dẫn động */
            #ExerciseListPanel {{
                background-image: url("{duong_dan_anh_nen}");
                background-position: center;
                background-repeat: no-repeat;
            }}

            /* Vùng cuộn trong suốt */
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            #scrollAreaWidgetContents {{
                background-color: transparent;
            }}

            /* Thanh cuộn mượt mà phong cách Cyberpunk */
            QScrollBar:vertical {{
                background: #0f111a;
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: #ff0055;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #00f0ff;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none; background: none;
            }}

            /* Phong cách nút bấm Neon mượt mà */
            QPushButton {{
                background-color: #161925;
                color: #00f0ff; 
                font-family: 'Segoe UI', sans-serif;
                font-size: 15pt;
                font-weight: bold;
                border: 2px solid #00f0ff;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 12px; 
            }}
            QPushButton:hover {{
                color: #ffffff;
                background-color: #ff0055; 
                border: 2px solid #ffffff; 
            }}
            QPushButton:pressed {{
                background-color: #9d00ff;
                border: 2px solid #9d00ff;
            }}

            /* Chữ Author tinh tế ở góc đáy */
            #lbl_author {{
                font-family: 'Segoe UI', sans-serif;
                font-size: 15pt;
                font-weight: bold;
                color: #626880;
                letter-spacing: 1px;
            }}
            #lbl_author:hover {{
                color: #00f0ff;
            }}
        """)

    def xu_ly_vao_bai(self, ten_man_hinh):
        self.mainframe.showScreen(ten_man_hinh)