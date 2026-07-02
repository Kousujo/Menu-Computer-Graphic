# core/geometry.py

import math


# ==============================================================================
# TOẠ ĐỘ & DIỆN TÍCH
# ==============================================================================

class ToaDo2D:
    """Lớp biểu diễn điểm 2 chiều với tọa độ x, y."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def STamGiac(A, B, C):
    """Tính diện tích tam giác ABC bằng cross product 2D."""
    return int(0.5 * abs((B.x - A.x) * (C.y - A.y) - (C.x - A.x) * (B.y - A.y)))


def DienTich(P, n):
    """Tính diện tích đa giác lồi n đỉnh bằng công thức shoelace."""
    if n < 3:
        return 0
    area = 0.0
    for i in range(n):
        x1, y1 = P[i].x, P[i].y
        x2, y2 = P[(i + 1) % n].x, P[(i + 1) % n].y
        area += x1 * y2 - x2 * y1
    return int(0.5 * abs(area))


# ==============================================================================
# HÌNH TRÒN — toán học thuần tuý (không vòng lặp pixel, không màu)
# ==============================================================================

def _circle_bounds_generator(xc: int, yc: int, R: int):
    """
    Generator thuần toán học: tính biên scanline cho từng dòng của hình tròn.
    Yields (y, x_start, x_end) — chưa có pixel, chưa có màu.
    Dùng int(round(...)) để tránh clipping pixel.
    """
    if R <= 0:
        return
    R2 = R * R
    for dy in range(-R, R + 1):
        dx = int(round(math.sqrt(R2 - dy * dy)))
        yield (yc + dy, xc - dx, xc + dx)


def _circle_inside_condition(xc: int, yc: int, R: int):
    """Trả về lambda kiểm tra điểm (x, y) có nằm trong hình tròn không."""
    if R <= 0:
        return lambda x, y: False
    R2 = R * R
    return lambda x, y: (x - xc) ** 2 + (y - yc) ** 2 <= R2


# ==============================================================================
# HÌNH ELLIPSE — toán học thuần tuý (không vòng lặp pixel, không màu)
# ==============================================================================

def _ellipse_bounds_generator(xc: int, yc: int, a: int, b: int):
    """
    Generator thuần toán học: tính biên scanline cho từng dòng của ellipse.
    Yields (y, x_start, x_end) — chưa có pixel, chưa có màu.
    """
    if a <= 0 or b <= 0:
        return
    a2 = a * a
    b2 = b * b
    for dy in range(-b, b + 1):
        if b2 == 0:
            continue
        dx = int(round(math.sqrt(max(0, a2 * (1 - (dy * dy) / b2)))))
        yield (yc + dy, xc - dx, xc + dx)


def _ellipse_inside_condition(xc: int, yc: int, a: int, b: int):
    """Trả về lambda kiểm tra điểm (x, y) có nằm trong ellipse không."""
    if a <= 0 or b <= 0:
        return lambda x, y: False
    a2, b2 = a * a, b * b
    vung_chua = a2 * b2
    return lambda x, y: b2 * ((x - xc) ** 2) + a2 * ((y - yc) ** 2) <= vung_chua


# ==============================================================================
# COORDINATORS — định tuyến toán học → thuật toán generic (không logic fill)
# ==============================================================================

def get_circle_fill_pixels(xc: int, yc: int, R: int,
                           algorithm: str = "loang",
                           color_tuple=(3, 105, 161),
                           batch_size=300):
    """
    Generator điều phối cho hình tròn.
    Chỉ định tuyến: forward công thức toán sang engine tô trong core.algorithms.

    algorithm:
      "scanline" → fill_horizontal_lines_animation với bounds generator
      "loang"    → flood_fill_animation với inside condition + batch_size
      "to_san"   → flood_fill_animation với batch_size cực lớn (tô tức thì)
    """
    if R <= 0:
        return

    from core.algorithms import fill_horizontal_lines_animation, flood_fill_animation

    if algorithm == "scanline":
        yield from fill_horizontal_lines_animation(
            _circle_bounds_generator(xc, yc, R),
            color_tuple=color_tuple
        )
    elif algorithm == "to_san":
        # ponytail: dùng flood fill với batch_size cực lớn → tô tức thì 1 batch
        yield from flood_fill_animation(
            xc, yc,
            _circle_inside_condition(xc, yc, R),
            color_tuple=color_tuple,
            batch_size=999999
        )
    else:  # "loang" hoặc fallback
        yield from flood_fill_animation(
            xc, yc,
            _circle_inside_condition(xc, yc, R),
            color_tuple=color_tuple,
            batch_size=batch_size
        )


def get_ellipse_fill_pixels(xc: int, yc: int, a: int, b: int,
                            algorithm: str = "loang",
                            color_tuple=(16, 185, 129),
                            batch_size=300):
    """
    Generator điều phối cho hình ellipse.
    Chỉ định tuyến: forward công thức toán sang engine tô trong core.algorithms.

    algorithm:
      "scanline" → fill_horizontal_lines_animation với bounds generator
      "loang"    → flood_fill_animation với inside condition + batch_size
      "to_san"   → flood_fill_animation với batch_size cực lớn (tô tức thì)
    """
    if a <= 0 or b <= 0:
        return

    from core.algorithms import fill_horizontal_lines_animation, flood_fill_animation

    if algorithm == "scanline":
        yield from fill_horizontal_lines_animation(
            _ellipse_bounds_generator(xc, yc, a, b),
            color_tuple=color_tuple
        )
    elif algorithm == "to_san":
        yield from flood_fill_animation(
            xc, yc,
            _ellipse_inside_condition(xc, yc, a, b),
            color_tuple=color_tuple,
            batch_size=999999
        )
    else:  # "loang" hoặc fallback
        yield from flood_fill_animation(
            xc, yc,
            _ellipse_inside_condition(xc, yc, a, b),
            color_tuple=color_tuple,
            batch_size=batch_size
        )


# ==============================================================================
# HÀM TIỆN ÍCH — outline hình tròn (dùng cho fill)
# ==============================================================================

def get_circle_pixels(xc, yc, r, color_tuple=(30, 30, 30)):
    """Trả về outline hình tròn (viền) dùng midpoint, có màu."""
    from core.algorithms import midpoint_circle
    outline = midpoint_circle(xc, yc, r)
    return [(x, y, color_tuple) for x, y in outline]