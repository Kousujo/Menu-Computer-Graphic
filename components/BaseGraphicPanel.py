from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QLabel, QListWidget, QFormLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from components.GraphicArea import GraphicArea

class BaseGraphicPanel(QWidget):
    def __init__(self, mainframe, title_sidebar="DANH SÁCH YÊU CẦU"):
        super().__init__()
        self.mainframe = mainframe
        
        self.font_chu_he_thong = QFont("Segoe UI", 14)
        self.setFont(self.font_chu_he_thong)
        self.setStyleSheet("background-color: #f8fafc;")

        layout_tong = QHBoxLayout(self)
        layout_tong.setContentsMargins(10, 10, 10, 10)
        layout_tong.setSpacing(12)

        # =================================================================
        # KHU VỰC BÊN TRÁI: CANVAS VÀ PANEL NHẬP LIỆU DYNAMIC
        # =================================================================
        vung_trai = QWidget()
        layout_trai = QVBoxLayout(vung_trai)
        layout_trai.setContentsMargins(0, 0, 0, 0)

        self.canvas = GraphicArea()
        layout_trai.addWidget(self.canvas)

        self.panel_nhap_lieu = QFrame(self.canvas)
        self.panel_nhap_lieu.setAutoFillBackground(True)
        self.panel_nhap_lieu.setGeometry(20, 20, 340, 50) 
        self.panel_nhap_lieu.setStyleSheet("""
            QFrame#PanelNoi {
                background-color: #1e293b; 
                border: 1px solid #334155; 
                border-radius: 8px;
            }
            QLabel {
                color: #f1f5f9; 
                font-size: 10pt; 
                font-weight: 600;
                border: none;
                background: transparent;
            }
            QLineEdit {
                background-color: #334155; 
                color: #38bdf8; 
                border: 1px solid #475569; 
                border-radius: 4px; 
                padding: 6px; 
                min-height: 25px;
                font-size: 11pt;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 1px solid #38bdf8;
            }
        """)
        self.panel_nhap_lieu.setObjectName("PanelNoi")
        
        layout_noi = QVBoxLayout(self.panel_nhap_lieu)
        layout_noi.setContentsMargins(12, 12, 12, 12)

        self.btn_an_hien_form = QPushButton("Thu gọn bảng điều khiển ▲")
        self.btn_an_hien_form.setStyleSheet("""
            QPushButton {
                font-size: 10pt; font-weight: bold; padding: 5px; 
                border: 1px solid #475569; border-radius: 4px;
                background-color: #334155; color: #cbd5e1;
            }
            QPushButton:hover { background-color: #475569; color: #ffffff; }
        """)
        self.btn_an_hien_form.clicked.connect(self.xu_ly_an_hien_panel)
        layout_noi.addWidget(self.btn_an_hien_form)

        self.khung_input = QWidget()
        self.khung_input.setStyleSheet("background: transparent; border: none;")
        self.form_layout = QFormLayout(self.khung_input)
        self.form_layout.setContentsMargins(0, 8, 0, 0)
        self.form_layout.setVerticalSpacing(8)
        layout_noi.addWidget(self.khung_input)

        layout_tong.addWidget(vung_trai, stretch=1)

        # =================================================================
        # KHU VỰC BÊN PHẢI: SIDEBAR
        # =================================================================
        self.sidebar_phai = QFrame()
        self.sidebar_phai.setFixedWidth(310)
        self.sidebar_phai.setStyleSheet("""
            QFrame { background-color: #0f172a; border-radius: 8px; }
            QLabel { color: #ffffff; border: none; }
        """)
        
        layout_sb = QVBoxLayout(self.sidebar_phai)
        layout_sb.setContentsMargins(18, 20, 18, 20)

        self.lbl_sb_title = QLabel(title_sidebar)
        self.lbl_sb_title.setStyleSheet("font-weight: 800; font-size: 12pt; color: #38bdf8; letter-spacing: 1px;")
        layout_sb.addWidget(self.lbl_sb_title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_sb.addSpacing(10)

        self.list_yeu_cau = QListWidget()
        self.list_yeu_cau.setStyleSheet("""
            QListWidget {
                border: 1px solid #1e293b; border-radius: 6px;
                background-color: #1e293b; color: #e2e8f0;
                font-size: 10pt; font-weight: 500; padding: 5px;
                outline: none;
            }
            QListWidget::item {
                padding: 10px; border-radius: 4px; margin-bottom: 4px;
            }
            QListWidget::item:hover {
                background-color: #334155; color: #38bdf8;
            }
            QListWidget::item:selected {
                background-color: #0284c7; color: #ffffff; font-weight: bold;
            }
            QListWidget::focus {
                border: 1px solid #1e293b;
            }
        """)
        layout_sb.addWidget(self.list_yeu_cau)
        layout_sb.addSpacing(15)

        self.btn_ve_hinh = QPushButton("KÍCH HOẠT VẼ HÌNH")
        self.btn_ve_hinh.setFixedHeight(46)
        self.btn_ve_hinh.setStyleSheet("""
            QPushButton {
                font-weight: 800; font-size: 10pt; letter-spacing: 0.5px;
                border: none; border-radius: 6px;
                background-color: #0ea5e9; color: #ffffff;
            }
            QPushButton:hover { background-color: #0284c7; }
            QPushButton:pressed { background-color: #0369a1; }
        """)
        self.btn_ve_hinh.clicked.connect(self.xu_ly_logic_ve)
        layout_sb.addWidget(self.btn_ve_hinh)
        layout_sb.addSpacing(6)

        btn_thoat_bai = QPushButton("QUAY LẠI TRANG CHỦ")
        btn_thoat_bai.setFixedHeight(42)
        btn_thoat_bai.setStyleSheet("""
            QPushButton {
                font-weight: 600; font-size: 9pt;
                border: 1px solid #334155; border-radius: 6px;
                background-color: #1e293b; color: #94a3b8;
            }
            QPushButton:hover { background-color: #334155; color: #f1f5f9; border: 1px solid #475569; }
        """)
        btn_thoat_bai.clicked.connect(lambda: self.mainframe.showScreen("ExerciseList"))
        layout_sb.addWidget(btn_thoat_bai)

        layout_tong.addWidget(self.sidebar_phai)

    def tao_duong_ngan_cach(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setStyleSheet("color: #334155; background-color: #334155; max-height: 1px; border: none; margin: 2px 0px;")
        return line

    def xoa_toan_bo_input(self):
        while self.form_layout.count() > 0:
            item = self.form_layout.takeAt(0)
            widget = item.widget()  # type: ignore
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def xu_ly_an_hien_panel(self):
        if self.khung_input.isVisible():
            self.khung_input.hide()
            self.panel_nhap_lieu.setFixedHeight(45)
            self.btn_an_hien_form.setText("Mở rộng bảng điều khiển ▼")
        else:
            self.khung_input.show()
            self.panel_nhap_lieu.setMinimumHeight(0)
            self.panel_nhap_lieu.setMaximumHeight(16777215)
            self.cap_nhat_kich_thuoc_panel()
            self.btn_an_hien_form.setText("Thu gọn bảng điều khiển ▲")

    def cap_nhat_kich_thuoc_panel(self):
        if self.khung_input.isVisible():
            QTimer.singleShot(1, self._thuc_thi_co_gian)

    def _thuc_thi_co_gian(self):
        if self.panel_nhap_lieu.layout():
            self.panel_nhap_lieu.layout().activate() # type: ignore
        self.panel_nhap_lieu.adjustSize()
        self.panel_nhap_lieu.setFixedWidth(340)

    def xu_ly_logic_ve(self):
        pass