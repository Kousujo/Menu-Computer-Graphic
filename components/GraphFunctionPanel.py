# components/GraphFunctionPanel.py
from typing import override

from components.BaseGraphicPanel import BaseGraphicPanel
from PyQt6.QtWidgets import QPushButton, QHBoxLayout

class GraphFunctionPanel(BaseGraphicPanel):
    def __init__(self, mainframe, title_sidebar="KHẢO SÁT HÀM SỐ"):
        super().__init__(mainframe, title_sidebar=title_sidebar)
        
        self.chỉnh_sua_nut_sidebar()

    def chỉnh_sua_nut_sidebar(self):
        """
        Bóc tách nút cũ và sắp xếp lại layout nút bấm theo hàng ngang
        để tích hợp thêm nút Khảo sát mà không làm vỡ giao diện.
        """
        self.btn_ve_hinh.hide()
        
        self.btn_khao_sat = QPushButton("KHẢO SÁT")
        self.btn_khao_sat.setFixedHeight(46)
        self.btn_khao_sat.setStyleSheet("""
            QPushButton {
                font-weight: 800; font-size: 10pt; letter-spacing: 0.5px;
                border: None; border-radius: 6px;
                background-color: #10b981; color: #ffffff; /* Màu xanh lá đặc trưng cho khảo sát */
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:pressed { background-color: #047857; }
        """)
        
        self.btn_ve_hinh_moi = QPushButton("VẼ ĐỒ THỊ")
        self.btn_ve_hinh_moi.setFixedHeight(46)
        self.btn_ve_hinh_moi.setStyleSheet("""
            QPushButton {
                font-weight: 800; font-size: 10pt; letter-spacing: 0.5px;
                border: None; border-radius: 6px;
                background-color: #0ea5e9; color: #ffffff;
            }
            QPushButton:hover { background-color: #0284c7; }
            QPushButton:pressed { background-color: #0369a1; }
        """)
        
        layout_hang_nut = QHBoxLayout()
        layout_hang_nut.setSpacing(8)
        layout_hang_nut.addWidget(self.btn_ve_hinh_moi, stretch=1)
        layout_hang_nut.addWidget(self.btn_khao_sat, stretch=1)
        
        layout_sb = self.sidebar_phai.layout()
        
        layout_sb.insertLayout(4, layout_hang_nut)  # type: ignore
        layout_sb.insertSpacing(5, 6) # type: ignore
        
        self.btn_ve_hinh_moi.clicked.connect(self.xu_ly_logic_ve)
        self.btn_khao_sat.clicked.connect(self.xu_ly_logic_khao_sat)

    def xu_ly_logic_khao_sat(self):
        pass

    def xu_ly_logic_ve(self):
        pass