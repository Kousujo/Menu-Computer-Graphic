# core/geometry_2.py

def get_filled_circle_pixels(xc: int, yc: int, R: int, color_tuple=(3, 105, 161)) -> list:
    """
    Tô màu hình tròn có tâm (xc, yc) và bán kính R dựa trên phương trình: 
    (x - xc)^2 + (y - yc)^2 <= R^2
    """
    if R <= 0:
        return []
    pixels = []
    R_squared = R * R
    
    # Quét không gian bao quanh hình tròn
    for x in range(xc - R, xc + R + 1):
        for y in range(yc - R, yc + R + 1):
            if (x - xc) ** 2 + (y - yc) ** 2 <= R_squared:
                pixels.append((x, y, color_tuple))
    return pixels

def get_filled_ellipse_pixels(xc: int, yc: int, a: int, b: int, color_tuple=(16, 185, 129)) -> list:
    """
    Tô màu hình ellipse có tâm (xc, yc) và bán kính trục a, b dựa trên phương trình: 
    (x - xc)^2/a^2 + (y - yc)^2/b^2 <= 1
    Quy đổi thành dạng không phân số để tránh chia cho 0: 
    b^2 * (x - xc)^2 + a^2 * (y - yc)^2 <= a^2 * b^2
    """
    if a <= 0 or b <= 0:
        return []
    pixels = []
    a2 = a * a
    b2 = b * b
    vung_chua = a2 * b2
    
    # Quét hình chữ nhật giới hạn bao quanh Elip
    for x in range(xc - a, xc + a + 1):
        for y in range(yc - b, yc + b + 1):
            if b2 * ((x - xc) ** 2) + a2 * ((y - yc) ** 2) <= vung_chua:
                pixels.append((x, y, color_tuple))
    return pixels