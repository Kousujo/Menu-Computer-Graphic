# core/geometry_3.py
from core.algorithms import bresenham_line, math_to_pixel

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