
from components.GraphFunctionPanel import GraphFunctionPanel
from components.AnalysisOverlayPanel import AnalysisOverlayPanel
from PyQt6.QtWidgets import QMessageBox, QLineEdit
from PyQt6.QtCore import QPointF
from core import geometry
import math


class Chuong1Panel(GraphFunctionPanel):
    def __init__(self, mainframe):
        super().__init__(mainframe, title_sidebar="CHƯƠNG 1: CÁC YẾU TỐ CƠ SỞ")

        all_algorithms = [
            "1. Hình tam giác thường",
            "2. Hình vuông",
            "3. Hình chữ nhật",
            "4. Hình bình hành",
            "5. Hình thoi",
            "6. Hình thang cân",
            "7. Đa giác đều có N cạnh",
            "8. Hình ngôi sao",
            "9. Cung tròn",
            "10. Cung Ellipse",
            "11. Đường tròn đi qua 3 điểm A, B, C",
            "12. Cung tròn đi qua 3 điểm A, B, C",
            "13. Hệ đường tròn đồng tâm",
            "14. Vòng bát chánh của Mahoraga",
            "15. Hoa văn đan kết 24 đường tròn",
            "16. Vòng tròn nan hoa đan xen",
            "17. Hoa văn 8 đường tròn giao tâm",
            "18. Vòng tròn lồng sao răng cưa",
            "19. Hàm bậc nhất (y = ax + b)",
            "20. Hàm bậc hai (y = ax² + bx + c)",
            "21. Hàm bậc ba (y = ax³ + bx² + cx + d)",
            "22. Hàm phân thức (y = (ax+b)/(cx+d))",
            "23. Hàm phân thức (y = (ax²+bx+c)/(dx+e))",
        ]

        self.list_yeu_cau.addItems(all_algorithms)

        self.inputs = {}
        self.list_yeu_cau.setCurrentRow(1)  # Start at first actual algorithm
        self.list_yeu_cau.currentRowChanged.connect(self.xu_ly_thay_doi_nhan_input)
        
        # ====================================================================
        # TẠO PANEL KHẢO SÁT OVERLAY (ẩn mặc định)
        # ====================================================================
        self.panel_khao_sat_overlay = AnalysisOverlayPanel(self.canvas)
        
        # Ẩn nút khảo sát mặc định, chỉ hiện khi chọn đồ thị hàm số
        self.btn_khao_sat.hide()
        self.btn_ve_hinh_moi.hide()
        
        self.xu_ly_thay_doi_nhan_input(1)

    def xu_ly_thay_doi_nhan_input(self, index):
        """
        Automatically clear and rebuild input form based on selected algorithm
        """
        self.xoa_toan_bo_input()
        self.inputs.clear()

        # Kiểm tra nếu là phần đồ thị hàm số (index 18-22) thì hiện nút khảo sát
        la_do_thi_ham_so = 18 <= index <= 22
        self.btn_khao_sat.setVisible(la_do_thi_ham_so)
        self.btn_ve_hinh_moi.setVisible(la_do_thi_ham_so)
        self.btn_ve_hinh.setVisible(not la_do_thi_ham_so)


        if index == 0:  # Hình tam giác
            self.them_o_nhap("canh_a", "Cạnh a (Đáy):", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("canh_b", "Cạnh b (Trái):", "160")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("canh_c", "Cạnh c (Phải):", "160")

        elif index == 1:  # Hình vuông
            self.them_o_nhap("canh", "Độ dài Cạnh:", "180")

        elif index == 2:  # Hình chữ nhật
            self.them_o_nhap("rong", "Chiều rộng:", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cao", "Chiều cao:", "120")

        elif index == 3:  # Hình bình hành
            self.them_o_nhap("day", "Chiều dài Đáy:", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cao", "Chiều cao:", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("do_nghieng", "Độ nghiêng (H-offset):", "60")

        elif index == 4:  # Hình thoi
            self.them_o_nhap("cheo_x", "Đường chéo X:", "200")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cheo_y", "Đường chéo Y:", "140")

        elif index == 5:  # Hình thang cân
            self.them_o_nhap("day_lon", "Đáy lớn:", "240")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("day_nho", "Đáy nhỏ:", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cao", "Chiều cao:", "100")

        elif index == 6:  # Đa giác đều
            self.them_o_nhap("so_canh", "Số cạnh N:", "6")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("ban_kinh", "Bán kính R:", "120")

        elif index == 7:  # Hình ngôi sao
            self.them_o_nhap("bk_ngoai", "Bán kính Ngoài:", "150")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("bk_trong", "Bán kính Trong:", "60")

        # ========================================================================
        # PHẦN 1B: CUNG TRÒN, ELLIPSE, VÒNG QUA 3 ĐIỂM (index 8-11)
        # ========================================================================

        elif index == 8:  # Cung tròn
            self.them_o_nhap("r", "Bán kính R:", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("goc_bat_dau", "Góc bắt đầu (độ):", "30")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("goc_ket_thuc", "Góc kết thúc (độ):", "300")

        elif index == 9:  # Cung Ellipse
            self.them_o_nhap("rx", "Bán kính Rx:", "150")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("ry", "Bán kính Ry:", "80")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("goc_bat_dau", "Góc bắt đầu (độ):", "45")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("goc_ket_thuc", "Góc kết thúc (độ):", "315")

        elif index == 10:  # Đường tròn qua 3 điểm
            self.them_o_nhap("ax", "Điểm A - X:", "x_tam - 100")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("ay", "Điểm A - Y:", "y_tam + 50")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("bx", "Điểm B - X:", "x_tam + 100")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("by", "Điểm B - Y:", "y_tam + 50")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cx", "Điểm C - X:", "x_tam")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cy", "Điểm C - Y:", "y_tam - 80")

        elif index == 11:  # Cung tròn qua 3 điểm
            self.them_o_nhap("ax", "Điểm A - X:", "x_tam - 120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("ay", "Điểm A - Y:", "y_tam + 60")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("bx", "Điểm B - X:", "x_tam")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("by", "Điểm B - Y:", "y_tam - 80")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cx", "Điểm C - X:", "x_tam + 120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("cy", "Điểm C - Y:", "y_tam + 60")

        # ========================================================================
        # PHẦN 2: HỌA TIẾT ĐƯỜNG TRÒN PHỨC TẠP (index 12-17)
        # ========================================================================

        elif index == 12:  # Hệ đường tròn đồng tâm
            self.them_o_nhap("basic_r", "Khoảng cách bán kính (R):", "35")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("so_vong", "Số vòng tròn đồng tâm:", "4")

        elif index == 13:  # Vòng bát chánh
            self.them_o_nhap("r", "Độ dài nan trục (R):", "120")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("r_nho", "Bán kính bóng tròn (r):", "25")

        elif index == 14:  # Hoa văn đan kết 24
            self.them_o_nhap("r", "Bán kính cánh tròn (r):", "40")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("R_ngoai", "Bán kính vòng tâm (R):", "90")

        elif index == 15:  # Vòng tròn nan hoa
            self.them_o_nhap("r", "Bán kính vòng hoa (R):", "120")

        elif index == 16:  # Hoa văn 8 đường tròn
            self.them_o_nhap("R", "Bán kính vòng tròn kết (R):", "90")

        elif index == 17:  # Vòng tròn lồng sao
            self.them_o_nhap("r", "Bán kính vòng lõi (r):", "80")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("r_ngoai", "Bán kính đỉnh nhọn (R):", "120")

        # ========================================================================
        # PHẦN 3: ĐỒ THỊ HÀM SỐ (index 18-22)
        # ========================================================================

        elif index == 18:  # Hàm bậc nhất
            self.them_o_nhap("scale", "Độ thu phóng lưới (Scale):", "40")
            self.them_o_nhap("a", "Hệ số a:", "1")
            self.them_o_nhap("b", "Hệ số b:", "2")

        elif index == 19:  # Hàm bậc hai
            self.them_o_nhap("scale", "Độ thu phóng lưới (Scale):", "40")
            self.them_o_nhap("a", "Hệ số a:", "1")
            self.them_o_nhap("b", "Hệ số b:", "-2")
            self.them_o_nhap("c", "Hệ số c:", "-1")

        elif index == 20:  # Hàm bậc ba
            self.them_o_nhap("scale", "Độ thu phóng lưới (Scale):", "40")
            self.them_o_nhap("a", "Hệ số a:", "1")
            self.them_o_nhap("b", "Hệ số b:", "0")
            self.them_o_nhap("c", "Hệ số c:", "-3")
            self.them_o_nhap("d", "Hệ số d:", "1")

        elif index == 21:  # Hàm phân thức 1/1
            self.them_o_nhap("scale", "Độ thu phóng lưới (Scale):", "40")
            self.them_o_nhap("a", "Hệ số a (tử):", "2")
            self.them_o_nhap("b", "Hệ số b (tử):", "1")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("c", "Hệ số c (mẫu):", "1")
            self.them_o_nhap("d", "Hệ số d (mẫu):", "-1")

        elif index == 22:  # Hàm phân thức 2/1
            self.them_o_nhap("scale", "Độ thu phóng lưới (Scale):", "40")
            self.them_o_nhap("a", "Hệ số a (tử):", "1")
            self.them_o_nhap("b", "Hệ số b (tử):", "1")
            self.them_o_nhap("c", "Hệ số c (tử):", "-2")
            self.form_layout.addRow(self.tao_duong_ngan_cach())
            self.them_o_nhap("d", "Hệ số d (mẫu):", "1")
            self.them_o_nhap("e", "Hệ số e (mẫu):", "1")

        self.cap_nhat_kich_thuoc_panel()

    def them_o_nhap(self, key, label_text, default_value):
        """Add input field to form"""
        txt_input = QLineEdit(default_value)
        self.form_layout.addRow(label_text, txt_input)
        self.inputs[key] = txt_input

    def xu_ly_logic_ve(self):
        """
        Unified drawing logic for all 23 algorithms
        """
        try:
            self.canvas.dat_lai_khung_nhin()

            x_tam = round((self.canvas.width() // 2) / 100) * 100
            y_tam = round((self.canvas.height() // 2) / 100) * 100

            index = self.list_yeu_cau.currentRow()
            pixels = []

            # ====================================================================
            # PHẦN 1: HỌA TIẾT CƠ BẢN
            # ====================================================================

            if index == 0:  # Hình tam giác
                pixels = geometry.get_triangle_pixels(
                    x_tam,
                    y_tam,
                    int(self.inputs["canh_a"].text()),
                    int(self.inputs["canh_b"].text()),
                    int(self.inputs["canh_c"].text()),
                )

            elif index == 1:  # Hình vuông
                canh = int(self.inputs["canh"].text())
                pixels = geometry.get_rectangle_pixels(x_tam, y_tam, canh, canh)

            elif index == 2:  # Hình chữ nhật
                pixels = geometry.get_rectangle_pixels(
                    x_tam,
                    y_tam,
                    int(self.inputs["rong"].text()),
                    int(self.inputs["cao"].text()),
                )

            elif index == 3:  # Hình bình hành
                pixels = geometry.get_parallelogram_pixels(
                    x_tam,
                    y_tam,
                    int(self.inputs["day"].text()),
                    int(self.inputs["cao"].text()),
                    int(self.inputs["do_nghieng"].text()),
                )

            elif index == 4:  # Hình thoi
                pixels = geometry.get_rhombus_pixels(
                    x_tam,
                    y_tam,
                    int(self.inputs["cheo_x"].text()),
                    int(self.inputs["cheo_y"].text()),
                )

            elif index == 5:  # Hình thang cân
                pixels = geometry.get_isosceles_trapezoid_pixels(
                    x_tam,
                    y_tam,
                    int(self.inputs["day_lon"].text()),
                    int(self.inputs["day_nho"].text()),
                    int(self.inputs["cao"].text()),
                )

            elif index == 6:  # Đa giác đều
                n = int(self.inputs["so_canh"].text())
                P = [geometry.ToaDo2D() for _ in range(n)]
                pixels = geometry.DrawPoly(
                    P,
                    n,
                    x_tam,
                    y_tam,
                    int(self.inputs["ban_kinh"].text()),
                )

            elif index == 7:  # Hình ngôi sao
                pixels = geometry.get_star_pixels(
                    x_tam,
                    y_tam,
                    int(self.inputs["bk_ngoai"].text()),
                    int(self.inputs["bk_trong"].text()),
                )

            # ====================================================================
            # PHẦN 1B: CUNG TRÒN, ELLIPSE, VÒNG QUA 3 ĐIỂM
            # ====================================================================

            elif index == 8:  # Cung tròn
                r = int(self.inputs["r"].text())
                g1 = float(self.inputs["goc_bat_dau"].text())
                g2 = float(self.inputs["goc_ket_thuc"].text())
                pixels = geometry.Arc(x_tam, y_tam, g1, g2, r)

            elif index == 9:  # Cung Ellipse
                rx = int(self.inputs["rx"].text())
                ry = int(self.inputs["ry"].text())
                g1 = float(self.inputs["goc_bat_dau"].text())
                g2 = float(self.inputs["goc_ket_thuc"].text())
                pixels = geometry.Sector(x_tam, y_tam, g1, g2, rx, ry)

            elif index == 10:  # Đường tròn qua 3 điểm
                # ponytail: Inputs are expressions relative to x_tam/y_tam;
                # eval them so user can type things like "x_tam - 100"
                ax = int(eval(self.inputs["ax"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                ay = int(eval(self.inputs["ay"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                bx = int(eval(self.inputs["bx"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                by = int(eval(self.inputs["by"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                cx = int(eval(self.inputs["cx"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                cy = int(eval(self.inputs["cy"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                A = geometry.ToaDo2D(ax, ay)
                B = geometry.ToaDo2D(bx, by)
                C = geometry.ToaDo2D(cx, cy)
                pixels = geometry.Circle3P(A, B, C)
                # ponytail: Vẽ vòng tròn màu nổi bật quanh 3 điểm A(đỏ), B(xanh lá), C(xanh dương)
                for x, y, color in [(ax, ay, (255, 50, 50)), (bx, by, (50, 255, 50)), (cx, cy, (50, 50, 255))]:
                    pixels.extend([(x + dx, y + dy, color) for dx, dy in 
                        [(0,0),(4,0),(-4,0),(0,4),(0,-4),(3,3),(-3,3),(3,-3),(-3,-3)]])

            elif index == 11:  # Cung tròn qua 3 điểm
                ax = int(eval(self.inputs["ax"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                ay = int(eval(self.inputs["ay"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                bx = int(eval(self.inputs["bx"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                by = int(eval(self.inputs["by"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                cx = int(eval(self.inputs["cx"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                cy = int(eval(self.inputs["cy"].text(), {"x_tam": x_tam, "y_tam": y_tam}))
                A = geometry.ToaDo2D(ax, ay)
                B = geometry.ToaDo2D(bx, by)
                C = geometry.ToaDo2D(cx, cy)
                pixels = geometry.Arc3P(A, B, C)
                # ponytail: Vẽ vòng tròn màu nổi bật quanh 3 điểm A(đỏ), B(xanh lá - điểm giữa), C(xanh dương)
                for x, y, color in [(ax, ay, (255, 50, 50)), (bx, by, (50, 255, 50)), (cx, cy, (50, 50, 255))]:
                    pixels.extend([(x + dx, y + dy, color) for dx, dy in 
                        [(0,0),(4,0),(-4,0),(0,4),(0,-4),(3,3),(-3,3),(3,-3),(-3,-3)]])

            # ====================================================================
            # PHẦN 2: HỌA TIẾT ĐƯỜNG TRÒN PHỨC TẠP
            # ====================================================================

            elif index == 12:  # Hệ đường tròn đồng tâm
                basic_r = int(self.inputs["basic_r"].text())
                so_vong = int(self.inputs["so_vong"].text())
                pixels = geometry.get_target_pixels(x_tam, y_tam, basic_r, so_vong)

            elif index == 13:  # Vòng bát chánh
                r = int(self.inputs["r"].text())
                r_nho = int(self.inputs["r_nho"].text())
                pixels = geometry.get_flower_8_petals_pixels(x_tam, y_tam, r, r_nho)

            elif index == 14:  # Hoa văn đan kết 24
                r = int(self.inputs["r"].text())
                R_ngoai = int(self.inputs["R_ngoai"].text())
                pixels = geometry.get_flower_24_petals_pixels(x_tam, y_tam, r, R_ngoai)

            elif index == 15:  # Vòng tròn nan hoa
                r = int(self.inputs["r"].text())
                pixels = geometry.get_wheel_with_spokes_pixels(x_tam, y_tam, r)

            elif index == 16:  # Hoa văn 8 đường tròn
                R = int(self.inputs["R"].text())
                pixels = geometry.get_circular_pattern_8_petals_pixels(x_tam, y_tam, R)

            elif index == 17:  # Vòng tròn lồng sao
                r = int(self.inputs["r"].text())
                r_ngoai = int(self.inputs["r_ngoai"].text())
                pixels = geometry.get_star_with_inner_circle_pixels(
                    x_tam, y_tam, r, r_ngoai
                )

            # ====================================================================
            # PHẦN 3: ĐỒ THỊ HÀM SỐ
            # ====================================================================

            elif index == 18:  # Hàm bậc nhất
                w_nua = self.canvas.width() / 2
                h_nua = self.canvas.height() / 2
                self.canvas.goc_toa_do_pan = QPointF(w_nua, h_nua)
                self.canvas.update()

                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                scale = float(self.inputs["scale"].text())
                pixels = geometry.get_line_function_pixels(0, 0, a, b, scale=scale)

            elif index == 19:  # Hàm bậc hai
                w_nua = self.canvas.width() / 2
                h_nua = self.canvas.height() / 2
                self.canvas.goc_toa_do_pan = QPointF(w_nua, h_nua)
                self.canvas.update()

                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                scale = float(self.inputs["scale"].text())
                pixels = geometry.get_quadratic_function_pixels(0, 0, a, b, c, scale=scale)

            elif index == 20:  # Hàm bậc ba
                w_nua = self.canvas.width() / 2
                h_nua = self.canvas.height() / 2
                self.canvas.goc_toa_do_pan = QPointF(w_nua, h_nua)
                self.canvas.update()

                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                d = float(self.inputs["d"].text())
                scale = float(self.inputs["scale"].text())
                pixels = geometry.get_cubic_function_pixels(0, 0, a, b, c, d, scale=scale)

            elif index == 21:  # Hàm phân thức 1/1
                w_nua = self.canvas.width() / 2
                h_nua = self.canvas.height() / 2
                self.canvas.goc_toa_do_pan = QPointF(w_nua, h_nua)
                self.canvas.update()

                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                d = float(self.inputs["d"].text())
                scale = float(self.inputs["scale"].text())
                pixels = geometry.get_rational_1_1_pixels(0, 0, a, b, c, d, scale=scale)

            elif index == 22:  # Hàm phân thức 2/1
                w_nua = self.canvas.width() / 2
                h_nua = self.canvas.height() / 2
                self.canvas.goc_toa_do_pan = QPointF(w_nua, h_nua)
                self.canvas.update()

                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                d = float(self.inputs["d"].text())
                e = float(self.inputs["e"].text())
                scale = float(self.inputs["scale"].text())
                pixels = geometry.get_rational_2_1_pixels(0, 0, a, b, c, d, e, scale=scale)

            self.canvas.cap_nhat_hinh_ve(pixels)

        except (ValueError, KeyError, IndexError) as e:
            print(f"Lỗi: {e}. Vui lòng kiểm tra lại dữ liệu nhập!")

    def xu_ly_logic_khao_sat(self):
        """Xử lý phân tích khảo sát toán học chuyên sâu với Giao diện Bảng Biến Thiên SGK nâng cao"""
        index = self.list_yeu_cau.currentRow()
        try:
            html_content = ""
            
            style_table = """
            <style>
                table.bbt { 
                    border-collapse: collapse; 
                    width: 100%; 
                    margin: 15px 0; 
                    border: 2px solid #334155; 
                    background-color: #111423;
                }
                table.bbt td { 
                    border: 1px solid #334155; 
                    padding: 6px; 
                    text-align: center; 
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 11pt;
                    color: #e2e8f0;
                }
                table.bbt td.label { 
                    background-color: #161925; 
                    color: #00f0ff; 
                    font-weight: bold; 
                    width: 12%; 
                }
                .neon-green { color: #10b981; font-weight: bold; }
                .neon-pink { color: #ff0055; font-weight: bold; }
                .neon-blue { color: #00f0ff; font-weight: bold; }
                .arrow-up { color: #ff0055; font-weight: bold; font-size: 13pt; }
                .arrow-down { color: #00f0ff; font-weight: bold; font-size: 13pt; }
            </style>
            """

            # =================================================================
            # 1. HÀM BẬC NHẤT: y = ax + b
            # =================================================================
            if index == 18:
                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                chieu = "ĐỒNG BIẾN trên ℝ" if a > 0 else ("NGHỊCH BIẾN trên ℝ" if a < 0 else "HÀM HẰNG")
                
                dong_y_phay = f"<td colspan='2'>{'+' if a > 0 else '-'}</td>"
                dong_y = f"<td>-∞</td><td class='arrow-up'>↗</td><td>+∞</td>" if a > 0 else f"<td>+∞</td><td class='arrow-down'>↘</td><td>-∞</td>"
                
                html_content = style_table + fr"""
                <p><b class='neon-blue'>Hàm số:</b> y = {a}x + {b}</p>
                <p><b>1. Tập xác định:</b> D = ℝ</p>
                <p><b>2. Sự biến thiên:</b></p>
                <ul>
                    <li><b>Đạo hàm:</b> y' = {a}</li>
                    <li><b>Chiều biến thiên:</b> Hàm số <span class='neon-green'>{chieu}</span> trên toàn bộ tập xác định.</li>
                    <li><b>Cực trị:</b> Hàm số không có cực trị.</li>
                </ul>
                <p><b>3. Bảng biến thiên chuẩn hóa:</b></p>
                <table class='bbt'>
                    <tr><td class='label'>x</td><td width='44%'>-∞</td><td width='44%'>+∞</td></tr>
                    <tr><td class='label'>y'</td>{dong_y_phay}</tr>
                    <tr><td class='label'>y</td>{dong_y}</tr>
                </table>
                """

            # =================================================================
            # 2. HÀM BẬC HAI: y = ax² + bx + c
            # =================================================================
            elif index == 19:
                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                if a == 0:
                    raise ValueError
                
                x_dinh = -b / (2 * a)
                y_dinh = a * (x_dinh**2) + b * x_dinh + c
                
                if a > 0:
                    bbt_y = f"""
                    <td>+∞</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td>+∞</td>
                    </tr>
                    <tr><td class='label' style='border:none;background:transparent;'></td>
                    <td></td>
                    <td class='arrow-down'>↘</td>
                    <td class='arrow-up'>↗</td>
                    <td></td>
                    </tr>
                    <tr><td class='label' style='border:none;background:transparent;'></td>
                    <td></td>
                    <td></td>
                    <td class='neon-pink'>{y_dinh:.2f}</td>
                    <td></td>
                    """
                    dong_y_phay = "<td>-</td><td>0</td><td>+</td>"
                    bien_thien = f"Nghịch biến trên khoảng (-∞; {x_dinh:.2f}) và đồng biến trên khoảng ({x_dinh:.2f}; +∞)"
                    cuc_tri = f"Hàm số đạt <b class='neon-green'>Cực tiểu</b> tại điểm: <span class='neon-blue'>I({x_dinh:.2f}; {y_dinh:.2f})</span>"
                else:
                    bbt_y = f"""
                    <td></td>
                    <td></td>
                    <td class='neon-pink'>{y_dinh:.2f}</td>
                    <td></td>
                    <td></td>
                    </tr>
                    <tr><td class='label' style='border:none;background:transparent;'></td>
                    <td></td>
                    <td class='arrow-up'>↗</td>
                    <td class='arrow-down'>↘</td>
                    <td></td>
                    </tr>
                    <tr><td class='label' style='border:none;background:transparent;'></td>
                    <td>-∞</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td>-∞</td>
                    """
                    dong_y_phay = "<td>+</td><td>0</td><td>-</td>"
                    bien_thien = f"Đồng biến trên khoảng (-∞; {x_dinh:.2f}) và nghịch biến trên khoảng ({x_dinh:.2f}; +∞)"
                    cuc_tri = f"Hàm số đạt <b class='neon-pink'>Cực đại</b> tại điểm: <span class='neon-blue'>I({x_dinh:.2f}; {y_dinh:.2f})</span>"

                html_content = style_table + fr"""
                <p><b class='neon-blue'>Hàm số:</b> y = {a}x² + {b}x + {c}</p>
                <p><b>1. Tập xác định:</b> D = ℝ</p>
                <p><b>2. Sự biến thiên:</b></p>
                <ul>
                    <li><b>Đạo hàm:</b> y' = {2*a}x + {b} ⇒ y' = 0 tại x = {x_dinh:.2f}</li>
                    <li><b>Sự biến thiên:</b> {bien_thien}</li>
                    <li><b>Cực trị:</b> {cuc_tri}</li>
                </ul>
                <p><b>3. Bảng biến thiên chuẩn hóa:</b></p>
                <table class='bbt'>
                    <tr><td class='label'>x</td><td>-∞</td><td colspan='2'>{x_dinh:.2f}</td><td>+∞</td></tr>
                    <tr><td class='label'>y'</td>{dong_y_phay}</tr>
                    <tr><td class='label'>y</td>{bbt_y}</tr>
                </table>
                """

            # =================================================================
            # 3. HÀM BẬC BA: y = ax³ + bx² + cx + d
            # =================================================================
            elif index == 20:
                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                d = float(self.inputs["d"].text())
                if a == 0:
                    raise ValueError

                A = 3 * a
                B = 2 * b
                C = c
                delta = B**2 - 4 * A * C
                
                html_content = style_table + fr"""
                <p><b class='neon-blue'>Hàm số:</b> y = {a}x³ + {b}x² + {c}x + {d}</p>
                <p><b>1. Tập xác định:</b> D = ℝ</p>
                <p><b>2. Sự biến thiên:</b> Đạo hàm y' = {A}x² + {B}x + {C} (Δ' = {delta:.2f})</p>
                """
                
                if delta <= 0:
                    tt_chieu = "ĐỒNG BIẾN trên ℝ" if a > 0 else "NGHỊCH BIẾN trên ℝ"
                    dong_y = f"<td>-∞</td><td class='arrow-up'>↗</td><td>+∞</td>" if a > 0 else f"<td>+∞</td><td class='arrow-down'>↘</td><td>-∞</td>"
                    html_content += fr"""
                    <ul>
                        <li><b>Chiều biến thiên:</b> Do y' không đổi dấu, hàm số <span class='neon-green'>{tt_chieu}</span>.</li>
                        <li><b>Cực trị:</b> Hàm số không có điểm cực trị nào.</li>
                    </ul>
                    <p><b>3. Bảng biến thiên chuẩn hóa:</b></p>
                    <table class='bbt'>
                        <tr><td class='label'>x</td><td width='44%'>-∞</td><td width='44%'>+∞</td></tr>
                        <tr><td class='label'>y'</td><td colspan='2'>{"++" if a>0 else "--"}</td></tr>
                        <tr><td class='label'>y</td>{dong_y}</tr>
                    </table>
                    """
                else:
                    x1 = (-B - math.sqrt(delta)) / (2 * A)
                    x2 = (-B + math.sqrt(delta)) / (2 * A)
                    if x1 > x2:
                        x1, x2 = x2, x1
                    
                    y1 = a*(x1**3) + b*(x1**2) + c*x1 + d
                    y2 = a*(x2**3) + b*(x2**2) + c*x2 + d
                    
                    if a > 0:
                        bbt_y = f"<td>-∞</td><td class='arrow-up'>↗</td><td class='neon-pink'>{y1:.2f}</td><td class='arrow-down'>↘</td><td class='neon-pink'>{y2:.2f}</td><td class='arrow-up'>↗</td><td>+∞</td>"
                        dong_y_phay = "<td>+</td><td>0</td><td>-</td><td>0</td><td>+</td>"
                    else:
                        bbt_y = f"<td>+∞</td><td class='arrow-down'>↘</td><td class='neon-pink'>{y1:.2f}</td><td class='arrow-up'>↗</td><td class='neon-pink'>{y2:.2f}</td><td class='arrow-down'>↘</td><td>-∞</td>"
                        dong_y_phay = "<td>-</td><td>0</td><td>+</td><td>0</td><td>-</td>"

                    html_content += fr"""
                    <ul>
                        <li><b>Cực trị:</b> Đạo hàm có 2 nghiệm phân biệt.</li>
                        <li>Điểm cực trị thứ nhất: <span class='neon-blue'>({x1:.2f}; {y1:.2f})</span></li>
                        <li>Điểm cực trị thứ hai: <span class='neon-blue'>({x2:.2f}; {y2:.2f})</span></li>
                    </ul>
                    <p><b>3. Bảng biến thiên chuẩn hóa:</b></p>
                    <table class='bbt'>
                        <tr><td class='label'>x</td><td>-∞</td><td>{x1:.2f}</td><td colspan='2'>{x2:.2f}</td><td>+∞</td></tr>
                        <tr><td class='label'>y'</td>{dong_y_phay}</tr>
                        <tr><td class='label'>y</td>{bbt_y}</tr>
                    </table>
                    """

            # =================================================================
            # 4. HÀM PHÂN THỨC: y = (ax + b) / (cx + d)
            # =================================================================
            elif index == 21:
                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                d = float(self.inputs["d"].text())
                if c == 0:
                    raise ValueError
                
                tc_dung = -d / c
                tc_ngang = a / c
                ladinh = a * d - b * c 
                
                chieu = "ĐỒNG BIẾN" if ladinh > 0 else "NGHỊCH BIẾN"
                dau = "+" if ladinh > 0 else "-"
                
                if ladinh > 0:
                    bbt_y = f"<td>{tc_ngang:.2f}</td><td class='arrow-up'>↗</td><td style='color:#ff0055; font-weight:bold;'>+∞</td><td style='color:#ff0055;'>||</td><td style='color:#ff0055; font-weight:bold;'>-∞</td><td class='arrow-up'>↗</td><td>{tc_ngang:.2f}</td>"
                else:
                    bbt_y = f"<td>{tc_ngang:.2f}</td><td class='arrow-down'>↘</td><td style='color:#ff0055; font-weight:bold;'>-∞</td><td style='color:#ff0055;'>||</td><td style='color:#ff0055; font-weight:bold;'>+∞</td><td class='arrow-down'>↘</td><td>{tc_ngang:.2f}</td>"

                html_content = style_table + fr"""
                <p><b class='neon-blue'>Hàm số:</b> y = ({a}x + {b}) / ({c}x + {d})</p>
                <p><b>1. Tập xác định:</b> D = ℝ \ {{{tc_dung:.2f}}}</p>
                <p><b>2. Sự biến thiên & Tiệm cận:</b></p>
                <ul>
                    <li><b>Đạo hàm:</b> y' = {ladinh} / ({c}x + {d})²</li>
                    <li><b>Tính đơn điệu:</b> Hàm số <span class='neon-green'>{chieu}</span> trên từng khoảng xác định (-∞; {tc_dung:.2f}) và ({tc_dung:.2f}; +∞).</li>
                    <li><b>Cực trị:</b> Hàm số không có cực trị.</li>
                    <li><b>Hệ tiệm cận:</b> Tiệm cận đứng: <span class='neon-pink'>x = {tc_dung:.2f}</span> | Tiệm cận ngang: <span class='neon-pink'>y = {tc_ngang:.2f}</span></li>
                </ul>
                <p><b>3. Bảng biến thiên dạng song song phân nhánh (SGK):</b></p>
                <table class='bbt'>
                    <tr><td class='label'>x</td><td>-∞</td><td colspan='2' style='color:#ff0055; font-weight:bold;'>{tc_dung:.2f}</td><td>+∞</td></tr>
                    <tr><td class='label'>y'</td><td>{dau}</td><td colspan='2' style='color:#ff0055; font-weight:bold;'>||</td><td>{dau}</td></tr>
                    <tr><td class='label'>y</td>{bbt_y}</tr>
                </table>
                """

            # =================================================================
            # 5. HÀM PHÂN THỨC: y = (ax² + bx + c) / (dx + e)
            # =================================================================
            elif index == 22:
                a = float(self.inputs["a"].text())
                b = float(self.inputs["b"].text())
                c = float(self.inputs["c"].text())
                d = float(self.inputs["d"].text())
                e = float(self.inputs["e"].text())
                if d == 0:
                    raise ValueError
                
                tc_dung = -e / d
                html_content = style_table + fr"""
                <p><b class='neon-blue'>Hàm số:</b> y = ({a}x² + {b}x + {c}) / ({d}x + {e})</p>
                <p><b>1. Tập xác định:</b> D = ℝ \ {{{tc_dung:.2f}}}</p>
                <p><b>2. Khảo sát biến thiên chuyên sâu:</b></p>
                <ul>
                    <li><b>Tiệm cận đứng:</b> Đường thẳng <span class='neon-pink'>x = {tc_dung:.2f}</span></li>
                    <li><b>Tiệm cận xiên:</b> Chia tử cho mẫu ta thu được tiệm cận xiên khi x tiến ra vô cùng.</li>
                    <li><b>Cực trị:</b> Cực đại và Cực tiểu xuất hiện đối xứng hai bên đường tiệm cận đứng.</li>
                </ul>
                <p><b>3. Bảng biến thiên mô phỏng tiệm cận:</b></p>
                <table class='bbt'>
                    <tr><td class='label'>x</td><td>-∞</td><td>X_CĐ</td><td style='color:#ff0055; font-weight:bold;'>{tc_dung:.2f}</td><td>X_CT</td><td>+∞</td></tr>
                    <tr><td class='label'>y'</td><td>+</td><td>0</td><td>-</td><td style='color:#ff0055; font-weight:bold;'>||</td><td>-</td><td>0</td><td>+</td></tr>
                    <tr><td class='label'>y</td><td>-∞ ↗</td><td class='neon-pink'>Cực Đại</td><td>↘ -∞</td><td style='color:#ff0055; font-weight:bold;'>||</td><td>+∞ ↘</td><td class='neon-green'>Cực Tiểu</td><td>↗ +∞</td></tr>
                </table>
                """

            self.panel_khao_sat_overlay.cap_nhat_du_lieu_html(html_content)
            self.panel_khao_sat_overlay.parent_resize_event(self.canvas.width(), self.canvas.height())
            
        except (ValueError, ZeroDivisionError):
            QMessageBox.warning(self, "Lỗi dữ liệu", "Hệ số nhập vào không hợp lệ hoặc làm mất bậc cao nhất của hàm số!")