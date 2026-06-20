# core/geometry_2.py
import math
from core.algorithms import bresenham_line, midpoint_circle

def get_target_pixels(x_tam, y_tam, basic_r, so_vong):
    """Hình 1: Hệ 4 đường tròn đồng tâm (Bia bắn cung)"""
    pixels = []
    for i in range(1, so_vong + 1):
        pixels.extend(midpoint_circle(x_tam, y_tam, basic_r * i))
    return pixels

def get_flower_8_petals_pixels(x_tam, y_tam, r, r_nho):
    """Hình 2: Trục hoa tiêu chuẩn quay vòng với 8 đường tròn nhỏ xung quanh (Đã sửa lỗi đâm xuyên)"""
    pixels = []
    
    for i in range(8):
        goc = i * (math.pi / 4)
        
        # 1. Xác định vị trí tâm của đường tròn nhỏ ở đầu mút (giữ nguyên để không lệch vị trí hình)
        xf = int(x_tam + r * math.cos(goc))
        yf = int(y_tam + r * math.sin(goc))
        
        # 2. Tính toán điểm kết thúc mới của đoạn thẳng (rút ngắn đi một đoạn r_nho)
        r_thuc_te = max(0, r - r_nho)
        x_riem = int(x_tam + r_thuc_te * math.cos(goc))
        y_riem = int(y_tam + r_thuc_te * math.sin(goc))
        
        # 3. Vẽ nan thẳng bằng Bresenham nhưng chỉ nối từ tâm chính tới sát rìa biên đường tròn nhỏ
        pixels.extend(bresenham_line(x_tam, y_tam, x_riem, y_riem))
        
        # 4. Vẽ đường tròn nhỏ ở đầu mút bằng Midpoint
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
    """Hình 4: Vòng tròn ảo diệu kết hợp từ nhiều lớp nan hoa đan xen"""
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