# core/geometry.py
import math
from core.algorithms import bresenham_line, midpoint_circle

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