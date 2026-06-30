# exercises/Chuong_2.py

from components.BaseGraphicPanel import BaseGraphicPanel
from PyQt6.QtWidgets import QLineEdit, QLabel, QRadioButton, QButtonGroup, QFrame, QHBoxLayout
from core.geometry_2 import (
    _circle_fill,
    _circle_fill_scanline,
    _circle_fill_flood,
    _ellipse_fill,
    _ellipse_fill_scanline,
    _ellipse_fill_flood,
)
from core.geometry_1 import get_circle_pixels
from core.algorithms import midpoint_ellipse


class Chuong2Panel(BaseGraphicPanel):
    def __init__(self, mainframe):
        super().__init__(mainframe, title_sidebar="CHƯƠNG 2: THUẬT TOÁN TÔ MÀU")

        # Khai báo các bài tập chương 2
        self.list_yeu_cau.addItem("Bài 1: Tô màu hình tròn")
        self.list_yeu_cau.addItem("Bài 2: Tô màu hình Ellipse")

        # Từ điển chứa các ô input tham số động
        self.inputs = {}

        # Biến lưu tên thuật toán đã chọn
        self._selected_algorithm = "loang"

        # Lắng nghe sự kiện thay đổi bài tập trong danh sách
        self.list_yeu_cau.currentRowChanged.connect(self.thay_doi_bai_tap)

        # Chọn bài tập mặc định đầu tiên
        self.list_yeu_cau.setCurrentRow(0)

    def thay_doi_bai_tap(self, row):
        """Xóa form cũ và sinh động các trường nhập liệu tương ứng bài tập"""
        self.xoa_toan_bo_input()
        self.inputs.clear()

        # Lấy kích thước tương đối của khung vẽ làm tâm mặc định ngẫu nhiên
        tam_x = self.canvas.width() // 2 if self.canvas.width() > 0 else 300
        tam_y = self.canvas.height() // 2 if self.canvas.height() > 0 else 300

        if row == 0:  # Tô màu hình tròn
            self.them_o_nhap("xc", "Tâm X (xc):", str(tam_x))
            self.them_o_nhap("yc", "Tâm Y (yc):", str(tam_y))
            self.them_o_nhap("r", "Bán kính (R):", "100")
            self._them_algorithm_selector()
        elif row == 1:  # Tô màu hình Ellipse
            self.them_o_nhap("xc", "Tâm X (xc):", str(tam_x))
            self.them_o_nhap("yc", "Tâm Y (yc):", str(tam_y))
            self.them_o_nhap("a", "Bán kính trục lớn (a):", "150")
            self.them_o_nhap("b", "Bán kính trục nhỏ (b):", "80")
            self._them_algorithm_selector()

        self.cap_nhat_kich_thuoc_panel()

    def _them_algorithm_selector(self):
        """Thêm 3 radio button chọn thuật toán + checkbox animation vào form."""
        group = QButtonGroup(self)
        radio_to_san = QRadioButton("Tô sẵn")
        radio_scanline = QRadioButton("Scanline")
        radio_loang = QRadioButton("Tô loang")

        for rb in [radio_to_san, radio_scanline, radio_loang]:
            rb.setStyleSheet("""
                QRadioButton {
                    color: #f1f5f9; font-size: 10pt; font-weight: 600;
                    spacing: 6px; background: transparent; border: none;
                }
                QRadioButton::indicator {
                    width: 16px; height: 16px; border-radius: 8px;
                    border: 2px solid #475569; background: transparent;
                }
                QRadioButton::indicator:checked {
                    border: 2px solid #38bdf8; background: #38bdf8;
                }
            """)
            group.addButton(rb)

        # Khôi phục lựa chọn trước đó
        alg = self._selected_algorithm
        if alg == "to_san":
            radio_to_san.setChecked(True)
        elif alg == "scanline":
            radio_scanline.setChecked(True)
        else:
            radio_loang.setChecked(True)

        # Cập nhật _selected_algorithm khi người dùng chọn radio khác
        def on_changed(btn):
            if btn.isChecked():
                self._selected_algorithm = {
                    "Tô sẵn": "to_san",
                    "Scanline": "scanline",
                    "Tô loang": "loang",
                }.get(btn.text(), "loang")
        group.buttonToggled.connect(on_changed)

        selector = QFrame()
        selector.setStyleSheet("background: transparent; border: none;")
        layout_rb = QHBoxLayout(selector)
        layout_rb.setContentsMargins(0, 4, 0, 4)
        layout_rb.setSpacing(12)
        layout_rb.addWidget(radio_to_san)
        layout_rb.addWidget(radio_scanline)
        layout_rb.addWidget(radio_loang)
        layout_rb.addStretch()

        label = QLabel("Thuật toán tô:")
        label.setStyleSheet("color: #f1f5f9; font-size: 10pt; font-weight: 600; border: none; background: transparent;")
        self.form_layout.addRow(label, selector)


    def them_o_nhap(self, key, label_text, value_default):
        label = QLabel(label_text)
        edit = QLineEdit()
        edit.setText(value_default)
        self.form_layout.addRow(label, edit)
        self.inputs[key] = edit

    def xu_ly_logic_ve(self):
        """Được gọi khi người dùng click vào nút 'KÍCH HOẠT VẼ HÌNH'"""
        row = self.list_yeu_cau.currentRow()
        if row == -1:
            return

        try:
            # Thu thập và ép kiểu dữ liệu an toàn từ form
            params = {k: int(v.text().strip()) for k, v in self.inputs.items()}
        except ValueError:
            print("Lỗi: Vui lòng nhập thông số hình học hợp lệ ở dạng số nguyên!")
            return

        xc = params.get("xc", 200)
        yc = params.get("yc", 200)

        if row == 0:  # Tô màu hình tròn
            r = params.get("r", 50)
            if self._selected_algorithm == "to_san":
                # Tô sẵn: vẽ outline trước, sau đó tô màu (outline vẽ sau nên nằm trên)
                outline = get_circle_pixels(xc, yc, r)
                fill = _circle_fill(xc, yc, r, color_tuple=(3, 105, 161))
                danh_sach_pixel = fill + outline
                self.canvas.cap_nhat_hinh_ve(danh_sach_pixel)
                return
            # Scanline hoặc Tô loang: animation
            def circle_gen():
                outline = get_circle_pixels(xc, yc, r)
                if outline:
                    yield outline
                if self._selected_algorithm == "scanline":
                    yield from _circle_fill_scanline(xc, yc, r, color_tuple=(3, 105, 161))
                else:
                    yield from _circle_fill_flood(xc, yc, r, color_tuple=(3, 105, 161), batch_size=400)
            self.canvas.cap_nhat_hinh_ve_co_hoat_anh(circle_gen())
            return

        elif row == 1:  # Tô màu hình Ellipse
            a = params.get("a", 80)
            b = params.get("b", 50)
            if self._selected_algorithm == "to_san":
                outline = midpoint_ellipse(xc, yc, a, b)
                fill = _ellipse_fill(xc, yc, a, b, color_tuple=(16, 185, 129))
                danh_sach_pixel = fill + outline
                self.canvas.cap_nhat_hinh_ve(danh_sach_pixel)
                return
            def ellipse_gen():
                outline = midpoint_ellipse(xc, yc, a, b)
                if outline:
                    yield outline
                if self._selected_algorithm == "scanline":
                    yield from _ellipse_fill_scanline(xc, yc, a, b, color_tuple=(16, 185, 129))
                else:
                    yield from _ellipse_fill_flood(xc, yc, a, b, color_tuple=(16, 185, 129), batch_size=400)
            self.canvas.cap_nhat_hinh_ve_co_hoat_anh(ellipse_gen())
            return