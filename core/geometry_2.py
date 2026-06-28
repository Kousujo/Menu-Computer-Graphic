# core/geometry_2.py

import math
from core.algorithms import flood_fill


def get_filled_circle_pixels(xc: int, yc: int, R: int, color_tuple=(3, 105, 161)) -> list:
    """
    Tô màu hình tròn có tâm (xc, yc) và bán kính R bằng thuật toán Flood Fill.
    """
    if R <= 0:
        return []
    R_squared = R * R
    return flood_fill(xc, yc, lambda x, y: (x - xc) ** 2 + (y - yc) ** 2 <= R_squared, color_tuple)

def get_filled_ellipse_pixels(xc: int, yc: int, a: int, b: int, color_tuple=(16, 185, 129)) -> list:
    """
    Tô màu hình ellipse có tâm (xc, yc) và bán kính trục a, b bằng thuật toán Flood Fill.
    """
    if a <= 0 or b <= 0:
        return []
    a2 = a * a
    b2 = b * b
    vung_chua = a2 * b2
    return flood_fill(xc, yc, lambda x, y: b2 * ((x - xc) ** 2) + a2 * ((y - yc) ** 2) <= vung_chua, color_tuple)


# ==============================================================================
# 3 thuật toán tô màu hình tròn + 1 hàm điều phối duy nhất
# ==============================================================================

def _circle_fill_to_san(xc: int, yc: int, R: int, color_tuple=(3, 105, 161)) -> list:
    """Tô sẵn: duyệt bounding box, check pt đường tròn."""
    if R <= 0:
        return []
    pixels = []
    R2 = R * R
    for y in range(yc - R, yc + R + 1):
        for x in range(xc - R, xc + R + 1):
            if (x - xc) ** 2 + (y - yc) ** 2 <= R2:
                pixels.append((x, y, color_tuple))
    return pixels


def _circle_fill_scanline(xc: int, yc: int, R: int, color_tuple=(3, 105, 161)) -> list:
    """Scanline: với mỗi y, tính dx = sqrt(R² - dy²), tô từ xc-dx đến xc+dx."""
    if R <= 0:
        return []
    pixels = []
    for dy in range(-R, R + 1):
        dx = int(math.sqrt(R * R - dy * dy))
        for x in range(xc - dx, xc + dx + 1):
            pixels.append((x, yc + dy, color_tuple))
    return pixels


def _circle_fill_loang(xc: int, yc: int, R: int, color_tuple=(3, 105, 161)) -> list:
    """Tô loang: BFS flood fill từ tâm."""
    if R <= 0:
        return []
    R2 = R * R
    return flood_fill(xc, yc, lambda x, y: (x - xc) ** 2 + (y - yc) ** 2 <= R2, color_tuple)


# Registry: tên thuật toán -> hàm xử lý
_CIRCLE_ALGORITHMS = {
    "to_san":    _circle_fill_to_san,
    "scanline":  _circle_fill_scanline,
    "loang":     _circle_fill_loang,
}


def get_circle_fill_pixels(xc: int, yc: int, R: int,
                           algorithm: str = "loang",
                           color_tuple=(3, 105, 161)) -> list:
    """
    Hàm điều phối duy nhất cho hình tròn.

    Tham số:
        algorithm: "to_san" | "scanline" | "loang"
    """
    func = _CIRCLE_ALGORITHMS.get(algorithm)
    if func is None:
        print(f"Lỗi: Thuật toán '{algorithm}' không tồn tại. Dùng 'loang' thay thế.")
        return _circle_fill_loang(xc, yc, R, color_tuple)
    return func(xc, yc, R, color_tuple)