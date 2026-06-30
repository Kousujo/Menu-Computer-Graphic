# BaseGraphicPanel.py
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame,
                              QPushButton, QLabel, QListWidget, QFormLayout,
                              QScrollArea)
from PyQt6.QtCore import Qt
from components.GraphicArea import GraphicArea
from styles.voltagent_styles import (Color, qss_panel_input_overlay,
                                     qss_sidebar, qss_list_widget, qss_button_primary,
                                     qss_button_secondary, qss_label_eyebrow,
                                     qss_divider)

_PANEL_CHIEU_CAO_CO_DINH = 260  # ponytail: đủ cho ~6-7 input, nếu dài hơn thì scroll


class BaseGraphicPanel(QWidget):
    def __init__(self, mainframe, title_sidebar="DANH SÁCH YÊU CẦU"):
        super().__init__()
        self.mainframe = mainframe
        self.setStyleSheet(f"background-color: {Color.CANVAS};")

        layout_tong = QHBoxLayout(self)
        layout_tong.setContentsMargins(10, 10, 10, 10)
        layout_tong.setSpacing(12)

        # =================================================================
        # KHU VỰC BÊN TRÁI: CANVAS + PANEL NHẬP LIỆU (OVERLAY)
        # =================================================================
        vung_trai = QWidget()
        layout_trai = QVBoxLayout(vung_trai)
        layout_trai.setContentsMargins(0, 0, 0, 0)

        self.canvas = GraphicArea()
        layout_trai.addWidget(self.canvas)

        self.panel_nhap_lieu = QFrame(self.canvas)
        self.panel_nhap_lieu.setAutoFillBackground(True)
        self.panel_nhap_lieu.setGeometry(20, 20, 340, 50)
        self.panel_nhap_lieu.setStyleSheet(qss_panel_input_overlay())
        self.panel_nhap_lieu.setObjectName("PanelNoi")

        layout_noi = QVBoxLayout(self.panel_nhap_lieu)
        layout_noi.setContentsMargins(12, 12, 12, 12)

        self.btn_an_hien_form = QPushButton("Thu gọn bảng điều khiển ▲")
        self.btn_an_hien_form.setStyleSheet(qss_button_secondary())
        self.btn_an_hien_form.clicked.connect(self.xu_ly_an_hien_panel)
        layout_noi.addWidget(self.btn_an_hien_form)

        # Khung cuộn chứa layout nhập liệu chính — cố định chiều cao
        self.khung_cuon = QScrollArea()
        self.khung_cuon.setWidgetResizable(True)
        self.khung_cuon.setFixedHeight(_PANEL_CHIEU_CAO_CO_DINH)
        # ponytail: viewport mặc định nền trắng → set transparent để ko có vệt trắng
        self.khung_cuon.viewport().setStyleSheet("background: transparent; border: none;")

        self.khung_input = QWidget()
        self.khung_input.setStyleSheet("background: transparent; border: none;")
        self.form_layout = QFormLayout(self.khung_input)
        self.form_layout.setContentsMargins(0, 8, 0, 0)
        self.form_layout.setVerticalSpacing(8)

        self.khung_cuon.setWidget(self.khung_input)
        layout_noi.addWidget(self.khung_cuon)

        # ponytail: set kích thước cố định ngay từ đầu để panel mở đúng khi vào chương
        self.panel_nhap_lieu.setFixedHeight(45 + _PANEL_CHIEU_CAO_CO_DINH)
        self.panel_nhap_lieu.setFixedWidth(340)

        layout_tong.addWidget(vung_trai, stretch=1)

        # =================================================================
        # KHU VỰC BÊN PHẢI: SIDEBAR
        # =================================================================
        self.sidebar_phai = QFrame()
        self.sidebar_phai.setFixedWidth(310)
        self.sidebar_phai.setStyleSheet(qss_sidebar())

        layout_sb = QVBoxLayout(self.sidebar_phai)
        layout_sb.setContentsMargins(18, 20, 18, 20)

        self.lbl_sb_title = QLabel(title_sidebar)
        self.lbl_sb_title.setStyleSheet(qss_label_eyebrow())
        layout_sb.addWidget(self.lbl_sb_title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_sb.addSpacing(10)

        self.list_yeu_cau = QListWidget()
        self.list_yeu_cau.setStyleSheet(qss_list_widget())
        layout_sb.addWidget(self.list_yeu_cau)
        layout_sb.addSpacing(15)

        self.btn_ve_hinh = QPushButton("KÍCH HOẠT VẼ HÌNH")
        self.btn_ve_hinh.setFixedHeight(46)
        self.btn_ve_hinh.setStyleSheet(qss_button_primary())
        self.btn_ve_hinh.clicked.connect(self.xu_ly_logic_ve)
        layout_sb.addWidget(self.btn_ve_hinh)
        layout_sb.addSpacing(6)

        btn_thoat_bai = QPushButton("QUAY LẠI TRANG CHỦ")
        btn_thoat_bai.setFixedHeight(42)
        btn_thoat_bai.setStyleSheet(qss_button_secondary())
        btn_thoat_bai.clicked.connect(lambda: self.mainframe.showScreen("ExerciseList"))
        layout_sb.addWidget(btn_thoat_bai)

        layout_tong.addWidget(self.sidebar_phai)

    def tao_duong_ngan_cach(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Plain)
        line.setStyleSheet(qss_divider())
        return line

    def xoa_toan_bo_input(self):
        while self.form_layout.count() > 0:
            item = self.form_layout.takeAt(0)
            widget = item.widget()  # type: ignore
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def xu_ly_an_hien_panel(self):
        if self.khung_cuon.isVisible():
            self.khung_cuon.hide()
            self.panel_nhap_lieu.setFixedHeight(45)
            self.btn_an_hien_form.setText("Mở rộng bảng điều khiển ▼")
        else:
            self.khung_cuon.show()
            self.panel_nhap_lieu.setFixedHeight(45 + _PANEL_CHIEU_CAO_CO_DINH)
            self.btn_an_hien_form.setText("Thu gọn bảng điều khiển ▲")
        self.panel_nhap_lieu.setFixedWidth(340)

    def cap_nhat_kich_thuoc_panel(self):
        """Cập nhật kích thước panel sau khi thêm/xoá input."""
        if self.khung_cuon.isVisible():
            self.panel_nhap_lieu.setFixedHeight(45 + _PANEL_CHIEU_CAO_CO_DINH)
            self.panel_nhap_lieu.setFixedWidth(340)

    def xu_ly_logic_ve(self):
        pass