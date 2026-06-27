def bresenham_line(x1, y1, x2, y2):
    pixels = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        pixels.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return pixels

def midpoint_line(x1, y1, x2, y2):
    """
    Vẽ đoạn thẳng bằng thuật toán MidPoint, xử lý tất cả các trường hợp slope.
    - 0 <= |m| <= 1: x đóng vai trò biến chạy
    - |m| > 1:        y đóng vai trò biến chạy
    """
    pixels = []
    dx = x2 - x1
    dy = y2 - y1

    # Nếu là 1 điểm
    if dx == 0 and dy == 0:
        return [(x1, y1)]

    ax = abs(dx)
    ay = abs(dy)
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1

    # Trường hợp 1: |m| <= 1 -> x là biến chạy
    if ax >= ay:
        x = x1
        y = y1
        d = ay * 2 - ax           # ponytail: decision param ban đầu
        dE = ay * 2               # increment khi chọn E
        dNE = (ay - ax) * 2       # increment khi chọn NE
        while True:
            pixels.append((x, y))
            if x == x2:
                break
            if d <= 0:
                d += dE
            else:
                d += dNE
                y += sy
            x += sx
    # Trường hợp 2: |m| > 1 -> y là biến chạy
    else:
        x = x1
        y = y1
        d = ax * 2 - ay
        dE = ax * 2
        dNE = (ax - ay) * 2
        while True:
            pixels.append((x, y))
            if y == y2:
                break
            if d <= 0:
                d += dE
            else:
                d += dNE
                x += sx
            y += sy

    return pixels

def midpoint_circle(xc, yc, r):
    if r <= 0:
        return []
    pixels = []
    x = 0
    y = r
    p = 1 - r

    def sym8(x, y):
        pixels.extend([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ])

    sym8(x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        sym8(x, y)
    return pixels

def midpoint_ellipse(xc, yc, rx, ry):
    # FIX: Chặn bán kính hợp lệ để tránh vòng lặp vô hạn
    if rx <= 0 or ry <= 0:
        return []
        
    pixels = []
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

    def sym4(x, y):
        pixels.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y)
        ])

    # Vùng 1
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = two_ry2 * x
    dy = two_rx2 * y

    while dx < dy:
        sym4(x, y)
        x += 1
        dx += two_ry2
        if p1 < 0:
            p1 += ry2 + dx
        else:
            y -= 1
            dy -= two_rx2
            p1 += ry2 + dx - dy

    # Vùng 2
    p2 = (ry2 * (x + 0.5) * (x + 0.5)) + (rx2 * (y - 1) * (y - 1)) - (rx2 * ry2)
    while y >= 0:
        sym4(x, y)
        y -= 1
        dy -= two_rx2
        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += two_ry2
            p2 += rx2 - dy + dx

    return list(set(pixels))

def math_to_pixel(x_math, y_math, center_x, center_y, scale=20.0):
    px = int(center_x + x_math * scale)
    py = int(center_y - y_math * scale)
    return px, py