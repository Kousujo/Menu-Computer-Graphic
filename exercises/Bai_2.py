# exercises/Bai_2.py
from components.BaseGraphicPanel import BaseGraphicPanel
from PyQt6.QtWidgets import QLineEdit
# ĐỔI ĐƯỜNG DẪN: Gọi trực tiếp tầng toán học độc lập của bài 2
from core import geometry_2

class Bai2Panel(BaseGraphicPanel):
    def __init__(self, mainframe):
        super().__init__(mainframe, title_sidebar="BÀI TẬP ĐƯỜNG TRÒN NÂNG CAO") #
        
        # Đưa 6 hình mẫu từ ảnh vào danh sách hiển thị
        self.list_yeu_cau.addItems([
            "1. Hệ đường tròn đồng tâm",
            "2. Vòng bát chánh của Mahoraga",
            "3. Hoa văn đan kết 24 đường tròn",
            "4. Vòng tròn nan hoa đan xen",
            "5. Hoa văn 8 đường tròn giao tâm",
            "6. Vòng tròn lồng sao răng cưa"
        ]) #
        
        self.inputs = {} #
        self.list_yeu_cau.setCurrentRow(0) #
        
        self.list_yeu_cau.currentRowChanged.connect(self.xu_ly_thay_doi_nhan_input) #
        self.xu_ly_thay_doi_nhan_input(0) #

    def xu_ly_thay_doi_nhan_input(self, index): #
        """Tự động dọn dẹp và hiển thị form nhập thông số chuẩn theo từng hình"""
        self.xoa_toan_bo_input() #
        self.inputs.clear() #

        if index == 0:
            self.them_o_nhap("basic_r", "Khoảng cách bán kính (R):", "35")
            self.form_layout.addRow(self.tao_duong_ngan_cach()) #
            self.them_o_nhap("so_vong", "Số vòng tròn đồng tâm:", "4")
        elif index == 1:
            self.them_o_nhap("r", "Độ dài nan trục (R):", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach()) #
            self.them_o_nhap("r_nho", "Bán kính bóng tròn (r):", "25")
        elif index == 2:
            self.them_o_nhap("r", "Bán kính cánh tròn (r):", "40")
            self.form_layout.addRow(self.tao_duong_ngan_cach()) #
            self.them_o_nhap("R_ngoai", "Bán kính vòng tâm (R):", "90")
        elif index == 3:
            self.them_o_nhap("r", "Bán kính vòng hoa (R):", "120")
        elif index == 4:
            self.them_o_nhap("R", "Bán kính vòng tròn kết (R):", "90")
        elif index == 5:
            self.them_o_nhap("r", "Bán kính vòng lõi (r):", "80")
            self.form_layout.addRow(self.tao_duong_ngan_cach()) #
            self.them_o_nhap("r_ngoai", "Bán kính đỉnh nhọn (R):", "120")

        self.cap_nhat_kich_thuoc_panel() #

    def them_o_nhap(self, key, label_text, default_value): #
        txt_input = QLineEdit(default_value) #
        self.form_layout.addRow(label_text, txt_input) #
        self.inputs[key] = txt_input #

    def xu_ly_logic_ve(self): #
        try:
            self.canvas.dat_lai_khung_nhin() #
            
            # Khóa tọa độ vẽ vào tâm màn hình lưới
            x_tam = round((self.canvas.width() // 2) / 100) * 100 #
            y_tam = round((self.canvas.height() // 2) / 100) * 100 #
            
            index = self.list_yeu_cau.currentRow() #
            pixels = [] #

            # Gọi trực tiếp qua biến `geometry_2` tương ứng với file hình học mới
            if index == 0:
                basic_r = int(self.inputs["basic_r"].text())
                so_vong = int(self.inputs["so_vong"].text())
                pixels = geometry_2.get_target_pixels(x_tam, y_tam, basic_r, so_vong)
            elif index == 1:
                r = int(self.inputs["r"].text())
                r_nho = int(self.inputs["r_nho"].text())
                pixels = geometry_2.get_flower_8_petals_pixels(x_tam, y_tam, r, r_nho)
            elif index == 2:
                r = int(self.inputs["r"].text())
                R_ngoai = int(self.inputs["R_ngoai"].text())
                pixels = geometry_2.get_flower_24_petals_pixels(x_tam, y_tam, r, R_ngoai)
            elif index == 3:
                r = int(self.inputs["r"].text())
                pixels = geometry_2.get_wheel_with_spokes_pixels(x_tam, y_tam, r)
            elif index == 4:
                R = int(self.inputs["R"].text())
                pixels = geometry_2.get_circular_pattern_8_petals_pixels(x_tam, y_tam, R)
            elif index == 5:
                r = int(self.inputs["r"].text())
                r_ngoai = int(self.inputs["r_ngoai"].text())
                pixels = geometry_2.get_star_with_inner_circle_pixels(x_tam, y_tam, r, r_ngoai)

            # Đẩy mảng tọa độ sang cho Canvas hiển thị ra màn hình
            self.canvas.cap_nhat_hinh_ve(pixels) #
            
        except (ValueError, KeyError, IndexError): #
            print("Lỗi định dạng dữ liệu đầu vào. Vui lòng nhập số nguyên hợp lệ!") #