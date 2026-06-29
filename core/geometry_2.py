# core/geometry_2.py
#
# Mô-đun tô màu hình tròn và ellipse.
# Mỗi hình có 3 thuật toán: to_san (bounding box brute-force),
# scanline (quét dòng), loang (flood fill BFS).
# Hình tròn và ellipse có registry riêng + 2 hàm dispatch:
#   get_*_fill_pixels(...)         → list pixel
#   get_*_fill_pixels_tung_buoc(...) → generator (animated)

import math
from core.algorithms import flood_fill


# ==============================================================================
# HÌNH TRÒN — 3 thuật toán tô
# ==============================================================================

def _circle_fill_to_san(xc: int, yc: int, R: int, color_tuple=(3, 105, 161)) -> list:
    """Tô sẵn: duyệt bounding box, kiểm tra pt đường tròn."""
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
    """Scanline: với mỗi y, tính dx = sqrt(R² - dy²), tô từ xc−dx đến xc+dx."""
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


_CIRCLE_ALGORITHMS = {
    "to_san":   _circle_fill_to_san,
    "scanline": _circle_fill_scanline,
    "loang":    _circle_fill_loang,
}


def get_circle_fill_pixels(xc: int, yc: int, R: int,
                           algorithm: str = "loang",
                           color_tuple=(3, 105, 161)) -> list:
    """Hàm điều phối duy nhất cho hình tròn.

    Tham số:
        algorithm: "to_san" | "scanline" | "loang"
    """
    func = _CIRCLE_ALGORITHMS.get(algorithm)
    if func is None:
        print(f"Lỗi: Thuật toán '{algorithm}' không tồn tại. Dùng 'loang' thay thế.")
        return _circle_fill_loang(xc, yc, R, color_tuple)
    return func(xc, yc, R, color_tuple)


# ==============================================================================
# HÌNH ELLIPSE — 3 thuật toán tô (trước đây chỉ có loang)
# ==============================================================================

def _ellipse_fill_to_san(xc: int, yc: int, a: int, b: int, color_tuple=(16, 185, 129)) -> list:
    """Tô sẵn: duyệt bounding box, kiểm tra pt ellipse."""
    if a <= 0 or b <= 0:
        return []
    pixels = []
    a2, b2 = a * a, b * b
    vung_chua = a2 * b2
    for y in range(yc - b, yc + b + 1):
        for x in range(xc - a, xc + a + 1):
            if b2 * ((x - xc) ** 2) + a2 * ((y - yc) ** 2) <= vung_chua:
                pixels.append((x, y, color_tuple))
    return pixels


def _ellipse_fill_scanline(xc: int, yc: int, a: int, b: int, color_tuple=(16, 185, 129)) -> list:
    """Scanline: với mỗi y, tính dx từ pt ellipse, tô từ xc−dx đến xc+dx."""
    if a <= 0 or b <= 0:
        return []
    pixels = []
    a2 = a * a
    for dy in range(-b, b + 1):
        # dx = a * sqrt(1 - dy²/b²)  (làm tròn xuống)
        dx = int(math.sqrt(max(0, a2 * (1 - (dy * dy) / (b * b)))))
        for x in range(xc - dx, xc + dx + 1):
            pixels.append((x, yc + dy, color_tuple))
    return pixels


def _ellipse_fill_loang(xc: int, yc: int, a: int, b: int, color_tuple=(16, 185, 129)) -> list:
    """Tô loang: BFS flood fill từ tâm."""
    if a <= 0 or b <= 0:
        return []
    a2, b2 = a * a, b * b
    vung_chua = a2 * b2
    return flood_fill(xc, yc, lambda x, y: b2 * ((x - xc) ** 2) + a2 * ((y - yc) ** 2) <= vung_chua, color_tuple)


_ELLIPSE_ALGORITHMS = {
    "to_san":   _ellipse_fill_to_san,
    "scanline": _ellipse_fill_scanline,
    "loang":    _ellipse_fill_loang,
}


def get_ellipse_fill_pixels(xc: int, yc: int, a: int, b: int,
                            algorithm: str = "loang",
                            color_tuple=(16, 185, 129)) -> list:
    """Hàm điều phối duy nhất cho hình ellipse.

    Tham số:
        algorithm: "to_san" | "scanline" | "loang"
    """
    func = _ELLIPSE_ALGORITHMS.get(algorithm)
    if func is None:
        print(f"Lỗi: Thuật toán '{algorithm}' không tồn tại. Dùng 'loang' thay thế.")
        return _ellipse_fill_loang(xc, yc, a, b, color_tuple)
    return func(xc, yc, a, b, color_tuple)


# ==============================================================================
# Animated variants (generator yield từng batch / frame)
# ==============================================================================

# --- Circle animated ---

def _circle_fill_scanline_tung_buoc(xc: int, yc: int, R: int,
                                    color_tuple=(3, 105, 161)):
    """Generator: yield từng dòng scanline của hình tròn."""
    if R <= 0:
        return
    for dy in range(-R, R + 1):
        dx = int(math.sqrt(R * R - dy * dy))
        row = []
        for x in range(xc - dx, xc + dx + 1):
            row.append((x, yc + dy, color_tuple))
        yield row


def _circle_fill_loang_tung_buoc(xc: int, yc: int, R: int,
                                 color_tuple=(3, 105, 161), batch_size=300):
    """Generator: yield từng batch BFS từ tâm hình tròn."""
    if R <= 0:
        return
    R2 = R * R
    from core.algorithms import flood_fill_tung_buoc
    yield from flood_fill_tung_buoc(
        xc, yc,
        lambda x, y: (x - xc) ** 2 + (y - yc) ** 2 <= R2,
        color_tuple, batch_size=batch_size
    )


_CIRCLE_ALGORITHMS_TUNG_BUOC = {
    "scanline": _circle_fill_scanline_tung_buoc,
    "loang":    _circle_fill_loang_tung_buoc,
}


def get_circle_fill_pixels_tung_buoc(xc: int, yc: int, R: int,
                                     algorithm: str = "loang",
                                     color_tuple=(3, 105, 161),
                                     batch_size=300):
    """Generator điều phối cho hình tròn (animated).
    algorithm: "scanline" | "loang"
    """
    func = _CIRCLE_ALGORITHMS_TUNG_BUOC.get(algorithm)
    if func is None:
        print(f"Lỗi: Thuật toán '{algorithm}' không có animation. Dùng 'loang' thay thế.")
        func = _circle_fill_loang_tung_buoc
    # ponytail: scanline không nhận batch_size, loang thì có
    if algorithm == "scanline":
        yield from func(xc, yc, R, color_tuple)
    else:
        yield from func(xc, yc, R, color_tuple, batch_size=batch_size)


# --- Ellipse animated (trước đây chỉ có loang) ---

def _ellipse_fill_scanline_tung_buoc(xc: int, yc: int, a: int, b: int,
                                     color_tuple=(16, 185, 129)):
    """Generator: yield từng dòng scanline của hình ellipse."""
    if a <= 0 or b <= 0:
        return
    a2 = a * a
    for dy in range(-b, b + 1):
        dx = int(math.sqrt(max(0, a2 * (1 - (dy * dy) / (b * b)))))
        row = []
        for x in range(xc - dx, xc + dx + 1):
            row.append((x, yc + dy, color_tuple))
        yield row


def _ellipse_fill_loang_tung_buoc(xc: int, yc: int, a: int, b: int,
                                  color_tuple=(16, 185, 129), batch_size=300):
    """Generator: yield từng batch BFS từ tâm ellipse."""
    if a <= 0 or b <= 0:
        return
    a2, b2 = a * a, b * b
    vung_chua = a2 * b2
    from core.algorithms import flood_fill_tung_buoc
    yield from flood_fill_tung_buoc(
        xc, yc,
        lambda x, y: b2 * ((x - xc) ** 2) + a2 * ((y - yc) ** 2) <= vung_chua,
        color_tuple, batch_size=batch_size
    )


_ELLIPSE_ALGORITHMS_TUNG_BUOC = {
    "scanline": _ellipse_fill_scanline_tung_buoc,
    "loang":    _ellipse_fill_loang_tung_buoc,
}


def get_ellipse_fill_pixels_tung_buoc(xc: int, yc: int, a: int, b: int,
                                      algorithm: str = "loang",
                                      color_tuple=(16, 185, 129),
                                      batch_size=300):
    """Generator điều phối cho hình ellipse (animated).
    algorithm: "scanline" | "loang"
    """
    func = _ELLIPSE_ALGORITHMS_TUNG_BUOC.get(algorithm)
    if func is None:
        print(f"Lỗi: Thuật toán '{algorithm}' không có animation. Dùng 'loang' thay thế.")
        func = _ellipse_fill_loang_tung_buoc
    if algorithm == "scanline":
        yield from func(xc, yc, a, b, color_tuple)
    else:
        yield from func(xc, yc, a, b, color_tuple, batch_size=batch_size)