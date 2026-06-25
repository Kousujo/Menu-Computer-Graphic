# exercises/Chuong_2.py

from components.BaseGraphicPanel import BaseGraphicPanel
from PyQt6.QtWidgets import QLineEdit, QLabel
from core.geometry_2 import get_filled_circle_pixels, get_filled_ellipse_pixels
class Chuong2Panel(BaseGraphicPanel):
    def __init__(self, mainframe):
        super().__init__(mainframe, title_sidebar="CHƯƠNG 2: THUẬT TOÁN TÔ MÀU")
        
        # Khai báo các bài tập chương 2
        self.list_yeu_cau.addItem("Bài 1: Tô màu hình tròn")
        self.list_yeu_cau.addItem("Bài 2: Tô màu hình Ellipse")
        
        # Từ điển chứa các ô input tham số động
        self.inputs = {}
        
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
            self.tao_truong_nhap("xc", "Tâm X (xc):", str(tam_x))
            self.tao_truong_nhap("yc", "Tâm Y (yc):", str(tam_y))
            self.tao_truong_nhap("r", "Bán kính (R):", "100")
        elif row == 1:  # Tô màu hình Ellipse
            self.tao_truong_nhap("xc", "Tâm X (xc):", str(tam_x))
            self.tao_truong_nhap("yc", "Tâm Y (yc):", str(tam_y))
            self.tao_truong_nhap("a", "Bán kính trục lớn (a):", "150")
            self.tao_truong_nhap("b", "Bán kính trục nhỏ (b):", "80")
            
        self.cap_nhat_kich_thuoc_panel()

    def tao_truong_nhap(self, key, label_text, value_default):
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

        danh_sach_pixel = []
        
        if row == 0:  # Tô màu hình tròn
            xc = params.get("xc", 200)
            yc = params.get("yc", 200)
            r = params.get("r", 50)
            # Màu xanh dương đại diện
            danh_sach_pixel = get_filled_circle_pixels(xc, yc, r, color_tuple=(3, 105, 161))
            
        elif row == 1:  # Tô màu hình Ellipse
            xc = params.get("xc", 200)
            yc = params.get("yc", 200)
            a = params.get("a", 80)
            # Màu xanh lá đại diện
            b = params.get("b", 50)
            danh_sach_pixel = get_filled_ellipse_pixels(xc, yc, a, b, color_tuple=(16, 185, 129))

        # Đẩy dữ liệu ra bộ đệm vẽ và yêu cầu canvas render lại đồ họa
        self.canvas.cap_nhat_hinh_ve(danh_sach_pixel)