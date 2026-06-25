# core/geometry_1.py
import math
from core.algorithms import bresenham_line, midpoint_circle, math_to_pixel

def get_triangle_pixels(x_tam, y_tam, a, b, c):
    if not ((a + b > c) and (a + c > b) and (b + c > a)):
        return []
    d_tu_b = (a**2 + c**2 - b**2) // (2 * a) if a != 0 else 0
    chieu_cao = int(math.sqrt(max(0, c**2 - d_tu_b**2)))
    
    xb, yb = x_tam - a // 2, y_tam + chieu_cao // 2
    xc, yc = x_tam + a // 2, y_tam + chieu_cao // 2
    xa, ya = xb + d_tu_b, y_tam - chieu_cao // 2

    return bresenham_line(xa, ya, xb, yb) + \
           bresenham_line(xb, yb, xc, yc) + \
           bresenham_line(xc, yc, xa, ya)

def get_rectangle_pixels(x_tam, y_tam, rong, cao):
    r_w, r_h = rong // 2, cao // 2
    return bresenham_line(x_tam - r_w, y_tam - r_h, x_tam + r_w, y_tam - r_h) + \
           bresenham_line(x_tam + r_w, y_tam - r_h, x_tam + r_w, y_tam + r_h) + \
           bresenham_line(x_tam + r_w, y_tam + r_h, x_tam - r_w, y_tam + r_h) + \
           bresenham_line(x_tam - r_w, y_tam + r_h, x_tam - r_w, y_tam - r_h)

def get_parallelogram_pixels(x_tam, y_tam, day, cao, do_nghieng):
    r_w, r_h = day // 2, cao // 2
    xa, ya = x_tam - r_w + do_nghieng, y_tam - r_h
    xb, yb = x_tam + r_w + do_nghieng, y_tam - r_h
    xc, yc = x_tam + r_w, y_tam + r_h
    xd, yd = x_tam - r_w, y_tam + r_h
    return bresenham_line(xa, ya, xb, yb) + \
           bresenham_line(xb, yb, xc, yc) + \
           bresenham_line(xc, yc, xd, yd) + \
           bresenham_line(xd, yd, xa, ya)

def get_rhombus_pixels(x_tam, y_tam, cheo_x, cheo_y):
    rx, ry = cheo_x // 2, cheo_y // 2
    return bresenham_line(x_tam, y_tam - ry, x_tam + rx, y_tam) + \
           bresenham_line(x_tam + rx, y_tam, x_tam, y_tam + ry) + \
           bresenham_line(x_tam, y_tam + ry, x_tam - rx, y_tam) + \
           bresenham_line(x_tam - rx, y_tam, x_tam, y_tam - ry)

def get_isosceles_trapezoid_pixels(x_tam, y_tam, day_lon, day_nho, cao):
    r_lon, r_nho, r_h = day_lon // 2, day_nho // 2, cao // 2
    xa, ya = x_tam - r_nho, y_tam - r_h
    xb, yb = x_tam + r_nho, y_tam - r_h
    xc, yc = x_tam + r_lon, y_tam + r_h
    xd, yd = x_tam - r_lon, y_tam + r_h
    return bresenham_line(xa, ya, xb, yb) + \
           bresenham_line(xb, yb, xc, yc) + \
           bresenham_line(xc, yc, xd, yd) + \
           bresenham_line(xd, yd, xa, ya)

def get_regular_polygon_pixels(x_tam, y_tam, n, r):
    if n < 3:
        return []
    pixels = []
    danh_sach_dinh = []
    for i in range(n):
        goc = i * (2 * math.pi / n) - math.pi / 2
        danh_sach_dinh.append((int(x_tam + r * math.cos(goc)), int(y_tam + r * math.sin(goc))))
    for i in range(n):
        pixels += bresenham_line(danh_sach_dinh[i][0], danh_sach_dinh[i][1], 
                                 danh_sach_dinh[(i + 1) % n][0], danh_sach_dinh[(i + 1) % n][1])
    return pixels

def get_star_pixels(x_tam, y_tam, r_ngoai, r_trong):
    tong_so_dinh = 10
    pixels = []
    danh_sach_dinh = []
    for i in range(tong_so_dinh):
        goc = i * (2 * math.pi / tong_so_dinh) - math.pi / 2
        r_hien_tai = r_ngoai if i % 2 == 0 else r_trong
        danh_sach_dinh.append((int(x_tam + r_hien_tai * math.cos(goc)), int(y_tam + r_hien_tai * math.sin(goc))))
    for i in range(tong_so_dinh):
        pixels += bresenham_line(danh_sach_dinh[i][0], danh_sach_dinh[i][1], 
                                 danh_sach_dinh[(i + 1) % tong_so_dinh][0], danh_sach_dinh[(i + 1) % tong_so_dinh][1])
    return pixels

def get_circle_pixels(x_tam, y_tam, r):
    """
    HÀM VẼ HÌNH TRÒN ĐƠN BẰNG MIDPOINT
    """
    if r <= 0:
        return []
    return midpoint_circle(x_tam, y_tam, r)

def get_concentric_circles_pixels(x_tam, y_tam, r_ngoai, r_trong):
    """
    HÀM VẼ CẶP ĐƯỜNG TRÒN ĐỒNG TÂM
    - Ứng dụng: Vẽ bánh xe, vòng nhẫn, mục tiêu bắn cung...
    """
    if r_ngoai <= 0 or r_trong <= 0:
        return []
    # Vẽ đường tròn lớn cộng nối tiếp với đường tròn nhỏ
    return midpoint_circle(x_tam, y_tam, r_ngoai) + midpoint_circle(x_tam, y_tam, r_trong)

def get_target_pixels(x_tam, y_tam, basic_r, so_vong):
    """Hình 1: Hệ đường tròn đồng tâm (Bia bắn cung)"""
    pixels = []
    for i in range(1, so_vong + 1):
        pixels.extend(midpoint_circle(x_tam, y_tam, basic_r * i))
    return pixels


def get_flower_8_petals_pixels(x_tam, y_tam, r, r_nho):
    """Hình 2: Trục hoa tiêu chuẩn quay vòng với 8 đường tròn nhỏ xung quanh"""
    pixels = []

    for i in range(8):
        goc = i * (math.pi / 4)

        # 1. Xác định vị trí tâm của đường tròn nhỏ ở đầu mút
        xf = int(x_tam + r * math.cos(goc))
        yf = int(y_tam + r * math.sin(goc))

        # 2. Tính toán điểm kết thúc mới của đoạn thẳng (rút ngắn đi một đoạn r_nho)
        r_thuc_te = max(0, r - r_nho)
        x_riem = int(x_tam + r_thuc_te * math.cos(goc))
        y_riem = int(y_tam + r_thuc_te * math.sin(goc))

        # 3. Vẽ đoạn thẳng từ tâm chính tới sát rìa biên đường tròn nhỏ
        pixels.extend(bresenham_line(x_tam, y_tam, x_riem, y_riem))

        # 4. Vẽ đường tròn nhỏ ở đầu mút
        pixels.extend(midpoint_circle(xf, yf, r_nho))

    return pixels


def get_flower_24_petals_pixels(x_tam, y_tam, r, R_ngoai):
    """Hình 3: Hoa văn đan kết từ 24 đường tròn nhỏ xoay quanh tâm"""
    pixels = []
    for i in range(24):
        goc = i * (2 * math.pi / 24)
        xi = int(x_tam + R_ngoai * math.cos(goc))
        yi = int(y_tam + R_ngoai * math.sin(goc))
        pixels.extend(midpoint_circle(xi, yi, r))
    return pixels


def get_wheel_with_spokes_pixels(x_tam, y_tam, r):
    """Hình 4: Vòng tròn kết hợp từ nhiều lớp nan hoa đan xen"""
    pixels = []
    so_vong = 36
    for i in range(so_vong):
        goc = i * (2 * math.pi / so_vong)
        xi = int(x_tam + (r // 3) * math.cos(goc))
        yi = int(y_tam + (r // 3) * math.sin(goc))
        pixels.extend(midpoint_circle(xi, yi, r))
    return pixels


def get_circular_pattern_8_petals_pixels(x_tam, y_tam, R):
    """Hình 5: Chuỗi tổ hợp đối xứng gồm 8 đường tròn giao nhau tại tâm"""
    pixels = []
    for i in range(8):
        goc = i * (math.pi / 4)
        xi = int(x_tam + R * math.cos(goc))
        yi = int(y_tam + R * math.sin(goc))
        pixels.extend(midpoint_circle(xi, yi, R))
    return pixels


def get_star_with_inner_circle_pixels(x_tam, y_tam, r, r_ngoai):
    """Hình 6: Đường tròn nội tiếp lồng trong ngôi sao nhiều múi nhọn"""
    pixels = []
    pixels.extend(midpoint_circle(x_tam, y_tam, r))

    so_dinh = 24  # Số múi răng cưa đan xung quanh
    for i in range(so_dinh):
        goc = i * (2 * math.pi / so_dinh)
        ri = r_ngoai if i % 2 == 0 else r
        xi = int(x_tam + ri * math.cos(goc))
        yi = int(y_tam + ri * math.sin(goc))

        goc_ke = (i + 1) * (2 * math.pi / so_dinh)
        ri_ke = r if i % 2 == 0 else r_ngoai
        xf_ke = int(x_tam + ri_ke * math.cos(goc_ke))
        yf_ke = int(y_tam + ri_ke * math.sin(goc_ke))

        pixels.extend(bresenham_line(xi, yi, xf_ke, yf_ke))
    return pixels

def get_line_function_pixels(x_tam, y_tam, a, b, x_min=-15, x_max=15, step=0.1, scale=40):
    """1. Hàm bậc nhất: y = ax + b"""
    pixel_points = []
    x = x_min
    while x <= x_max:
        y = a * x + b
        pixel_points.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step

    pixels = []
    for i in range(len(pixel_points) - 1):
        pixels.extend(bresenham_line(pixel_points[i][0], pixel_points[i][1], pixel_points[i+1][0], pixel_points[i+1][1]))
    return pixels

def get_quadratic_function_pixels(x_tam, y_tam, a, b, c, x_min=-15, x_max=15, step=0.05, scale=40):
    """2. Hàm bậc hai (Parabol): y = ax^2 + bx + c"""
    pixel_points = []
    x = x_min
    while x <= x_max:
        y = a * (x**2) + b * x + c
        pixel_points.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step

    pixels = []
    for i in range(len(pixel_points) - 1):
        pixels.extend(bresenham_line(pixel_points[i][0], pixel_points[i][1], pixel_points[i+1][0], pixel_points[i+1][1]))
    return pixels

def get_cubic_function_pixels(x_tam, y_tam, a, b, c, d, x_min=-15, x_max=15, step=0.05, scale=40):
    """3. Hàm bậc ba: y = ax^3 + bx^2 + cx + d"""
    pixel_points = []
    x = x_min
    while x <= x_max:
        y = a * (x**3) + b * (x**2) + c * x + d
        pixel_points.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step

    pixels = []
    for i in range(len(pixel_points) - 1):
        pixels.extend(bresenham_line(pixel_points[i][0], pixel_points[i][1], pixel_points[i+1][0], pixel_points[i+1][1]))
    return pixels

def get_rational_1_1_pixels(x_tam, y_tam, a, b, c, d, x_min=-15, x_max=15, step=0.02, scale=40):
    """4. Hàm phân thức bậc 1 / bậc 1: y = (ax + b) / (cx + d)"""
    pixels = []
    
    # Xác định điểm tiệm cận đứng: cx + d = 0 -> x = -d/c
    if c == 0:  # Trở thành hàm bậc nhất nếu c = 0
        # Nếu cả c và d = 0 thì mẫu số luôn 0 -> không xác định
        if d == 0:
            return []
        return get_line_function_pixels(x_tam, y_tam, a/d, b/d, x_min, x_max, step, scale)
        
    tiem_can_dung = -d / c
    epsilon = 0.05  # Khoảng cách an toàn để ngắt không nối đường thẳng qua tiệm cận
    
    # Nhánh 1: chạy từ x_min đến sát tiệm cận đứng bên trái
    pixel_points_1 = []
    x = x_min
    while x < tiem_can_dung - epsilon:
        y = (a * x + b) / (c * x + d)
        pixel_points_1.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step
        
    # Nhánh 2: chạy từ sát tiệm cận đứng bên phải đến x_max
    pixel_points_2 = []
    x = tiem_can_dung + epsilon
    while x <= x_max:
        y = (a * x + b) / (c * x + d)
        pixel_points_2.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step

    # Nối pixel độc lập cho từng nhánh để không bị dính đường thẳng dọc sai quy tắc
    for i in range(len(pixel_points_1) - 1):
        pixels.extend(bresenham_line(pixel_points_1[i][0], pixel_points_1[i][1], pixel_points_1[i+1][0], pixel_points_1[i+1][1]))
    for i in range(len(pixel_points_2) - 1):
        pixels.extend(bresenham_line(pixel_points_2[i][0], pixel_points_2[i][1], pixel_points_2[i+1][0], pixel_points_2[i+1][1]))
        
    return pixels

def get_rational_2_1_pixels(x_tam, y_tam, a, b, c, d, e, x_min=-15, x_max=15, step=0.02, scale=40):
    """5. Hàm phân thức bậc 2 / bậc 1: y = (ax^2 + bx + c) / (dx + e)"""
    pixels = []
    if d == 0:
        return []
        
    tiem_can_dung = -e / d
    epsilon = 0.05
    
    # Nhánh 1
    pixel_points_1 = []
    x = x_min
    while x < tiem_can_dung - epsilon:
        y = (a * (x**2) + b * x + c) / (d * x + e)
        pixel_points_1.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step
        
    # Nhánh 2
    pixel_points_2 = []
    x = tiem_can_dung + epsilon
    while x <= x_max:
        y = (a * (x**2) + b * x + c) / (d * x + e)
        pixel_points_2.append(math_to_pixel(x, y, x_tam, y_tam, scale))
        x += step

    for i in range(len(pixel_points_1) - 1):
        pixels.extend(bresenham_line(pixel_points_1[i][0], pixel_points_1[i][1], pixel_points_1[i+1][0], pixel_points_1[i+1][1]))
    for i in range(len(pixel_points_2) - 1):
        pixels.extend(bresenham_line(pixel_points_2[i][0], pixel_points_2[i][1], pixel_points_2[i+1][0], pixel_points_2[i+1][1]))
        
    return pixels