from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class AnalysisOverlayPanel(QWidget):
    def __init__(self, parent_canvas):
        """
        Bảng báo cáo khảo sát
        """
        super().__init__(parent_canvas)
        self.setObjectName("AnalysisOverlayPanel")
        
        self.setAutoFillBackground(True)
        
        self.setFixedSize(760, 530)
        
        self.setStyleSheet("""
            QWidget#AnalysisOverlayPanel {
                background-color: #0b0e17; 
                border: 2px solid #00f0ff; 
                border-radius: 12px;
            }
            QTextBrowser {
                background-color: #0b0e17;
                color: #e2e8f0;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11pt;
                padding-left: 18px;   /* ◄ Đẩy toàn bộ chữ đầu dòng lùi vào trong */
                padding-right: 18px;  /* ◄ Giữ khoảng cách an toàn với thanh cuộn bên phải */
                padding-top: 10px;
            }
            QScrollBar:vertical {
                border: none; 
                background: #111423; 
                width: 10px; 
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #ff0055; 
                min-height: 40px; 
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00f0ff;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none; background: none;
            }
        """)
        
        layout_chinh = QVBoxLayout(self)
        layout_chinh.setContentsMargins(22, 18, 22, 18)
        layout_chinh.setSpacing(12)
        
        # Tiêu đề
        lbl_title = QLabel("📊 KẾT QUẢ KHẢO SÁT & BIẾN THIÊN")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("""
            QLabel {
                color: #00f0ff; 
                font-weight: 900; 
                font-size: 14pt; 
                font-family: 'Segoe UI'; 
                letter-spacing: 0.5px; 
                background-color: #0b0e17;
                padding: 4px 0px;
            }
        """)
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
        btn_dong.setStyleSheet("""
            QPushButton {
                background-color: #111423; color: #ff0055;
                font-weight: bold; border: 2px solid #ff0055; border-radius: 6px;
                font-family: 'Segoe UI'; font-size: 10pt;
            }
            QPushButton:hover { background-color: #ff0055; color: white; border: 2px solid #ffffff; }
        """)
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