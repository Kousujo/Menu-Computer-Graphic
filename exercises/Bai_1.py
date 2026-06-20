# exercises/Bai_1.py
from components.BaseGraphicPanel import BaseGraphicPanel
from PyQt6.QtWidgets import QLineEdit
from core import geometry_1

class Bai1Panel(BaseGraphicPanel):
    def __init__(self, mainframe):
        super().__init__(mainframe, title_sidebar="THUẬT TOÁN ĐOẠN THẲNG")
        
        self.list_yeu_cau.addItems([
            "1. Hình tam giác thường",
            "2. Hình vuông",
            "3. Hình chữ nhật",
            "4. Hình bình hành",
            "5. Hình thoi",
            "6. Hình thang cân",
            "7. Đa giác đều có N cạnh",
            "8. Hình ngôi sao"
        ])
        
        self.inputs = {}
        self.list_yeu_cau.setCurrentRow(0)
        self.list_yeu_cau.currentRowChanged.connect(self.xu_ly_thay_doi_nhan_input)
        self.xu_ly_thay_doi_nhan_input(0)

    def xu_ly_thay_doi_nhan_input(self, index):
        self.xoa_toan_bo_input()
        self.inputs.clear()

        if index == 0:
            self.them_o_nhap("canh_a", "Cạnh a (Đáy):", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("canh_b", "Cạnh b (Trái):", "160")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("canh_c", "Cạnh c (Phải):", "160")

        elif index == 1: # Hình vuông
            self.them_o_nhap("canh", "Độ dài Cạnh:", "180")

        elif index == 2: # Hình chữ nhật
            self.them_o_nhap("rong", "Chiều rộng:", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cao", "Chiều cao:", "120")

        elif index == 3: # Hình bình hành
            self.them_o_nhap("day", "Chiều dài Đáy:", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cao", "Chiều cao:", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("do_nghieng", "Độ nghiêng (H-offset):", "60")

        elif index == 4: # Hình thoi
            self.them_o_nhap("cheo_x", "Đường chéo X:", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cheo_y", "Đường chéo Y:", "140")

        elif index == 5: # Hình thang cân
            self.them_o_nhap("day_lon", "Đáy lớn:", "240")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("day_nho", "Đáy nhỏ:", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cao", "Chiều cao:", "100")

        elif index == 6: # Đa giác đều
            self.them_o_nhap("so_canh", "Số cạnh N:", "6")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("ban_kinh", "Bán kính R:", "120")

        elif index == 7: # Hình ngôi sao
            self.them_o_nhap("bk_ngoai", "Bán kính Ngoài:", "150")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("bk_trong", "Bán kính Trong:", "60")

        self.cap_nhat_kich_thuoc_panel()

    def them_o_nhap(self, key, label_text, default_value):
        txt_input = QLineEdit(default_value)
        self.form_layout.addRow(label_text, txt_input)
        self.inputs[key] = txt_input

    def xu_ly_logic_ve(self):
        try:
            self.canvas.dat_lai_khung_nhin()
            
            x_tam = round((self.canvas.width() // 2) / 100) * 100
            y_tam = round((self.canvas.height() // 2) / 100) * 100
            
            index = self.list_yeu_cau.currentRow()
            pixels = []

            if index == 0:
                pixels = geometry_1.get_triangle_pixels(
                    x_tam, y_tam,
                    int(self.inputs["canh_a"].text()),
                    int(self.inputs["canh_b"].text()),
                    int(self.inputs["canh_c"].text())
                )
            elif index == 1:
                canh = int(self.inputs["canh"].text())
                pixels = geometry_1.get_rectangle_pixels(x_tam, y_tam, canh, canh) # Tận dụng hình chữ nhật cho hình vuông
                
            elif index == 2:
                pixels = geometry_1.get_rectangle_pixels(
                    x_tam, y_tam,
                    int(self.inputs["rong"].text()),
                    int(self.inputs["cao"].text())
                )
            elif index == 3:
                pixels = geometry_1.get_parallelogram_pixels(
                    x_tam, y_tam,
                    int(self.inputs["day"].text()),
                    int(self.inputs["cao"].text()),
                    int(self.inputs["do_nghieng"].text())
                )
            elif index == 4:
                pixels = geometry_1.get_rhombus_pixels(
                    x_tam, y_tam,
                    int(self.inputs["cheo_x"].text()),
                    int(self.inputs["cheo_y"].text())
                )
            elif index == 5:
                pixels = geometry_1.get_isosceles_trapezoid_pixels(
                    x_tam, y_tam,
                    int(self.inputs["day_lon"].text()),
                    int(self.inputs["day_nho"].text()),
                    int(self.inputs["cao"].text())
                )
            elif index == 6:
                pixels = geometry_1.get_regular_polygon_pixels(
                    x_tam, y_tam,
                    int(self.inputs["so_canh"].text()),
                    int(self.inputs["ban_kinh"].text())
                )
            elif index == 7:
                pixels = geometry_1.get_star_pixels(
                    x_tam, y_tam,
                    int(self.inputs["bk_ngoai"].text()),
                    int(self.inputs["bk_trong"].text())
                )

            self.canvas.cap_nhat_hinh_ve(pixels)
            
        except (ValueError, KeyError, IndexError):
            print("Lỗi định dạng dữ liệu đầu vào. Vui lòng kiểm tra lại!")