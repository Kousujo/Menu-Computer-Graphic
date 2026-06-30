# components/AnalysisOverlayPanel.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from styles.voltagent_styles import (qss_analysis_overlay, qss_analysis_title,
                                     qss_analysis_close_button)

class AnalysisOverlayPanel(QWidget):
    def __init__(self, parent_canvas):
        """
        Bảng báo cáo khảo sát CHỐNG XUYÊN THẤU TUYỆT ĐỐI
        """
        super().__init__(parent_canvas)
        self.setObjectName("AnalysisOverlayPanel")
        
        self.setAutoFillBackground(True)
        
        self.setFixedSize(760, 530)
        
        self.setStyleSheet(qss_analysis_overlay())
        
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setContentsMargins(22, 18, 22, 18)
        layout_chinh.setSpacing(12)
        
        # Tiêu đề
        lbl_title = QLabel("📊 KẾT QUẢ KHẢO SÁT & BIẾN THIÊN")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(qss_analysis_title())
        layout_chinh.addWidget(lbl_title)
        
        # Khung hiển thị nội dung HTML
        self.txt_content = QTextBrowser()
        self.txt_content.setFrameShape(QFrame.Shape.NoFrame)
        layout_chinh.addWidget(self.txt_content)
        
        # Nút đóng
        layout_nut = QHBoxLayout()
        layout_nut.addStretch()
        
        btn_dong = QPushButton("ĐÓNG BẢNG")
        btn_dong.setFixedSize(130, 36)
        btn_dong.setStyleSheet(qss_analysis_close_button())
        btn_dong.clicked.connect(self.hide)
        layout_nut.addWidget(btn_dong)
        layout_chinh.addLayout(layout_nut)
        
        self.hide()

    def cap_nhat_du_lieu_html(self, html_text):
        self.txt_content.setHtml(html_text)
        self.show()
        self.raise_()

    def parent_resize_event(self, canvas_width, canvas_height):
        """Căn giữa bảng khảo sát vào giữa Canvas chính"""
        x = max(10, (canvas_width - self.width()) // 2)
        y = max(10, (canvas_height - self.height()) // 2)
        self.move(x, y)