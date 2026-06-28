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

def is_point_in_convex_polygon(px, py, vertices):
    """
    Kiem tra mot diem (px, py) co nam trong da giac loi (vertices) hay khong.
    vertices la danh sach cac diem dang [(x0, y0), (x1, y1), ...].
    Su dung tich vo huong (cross product) de kiem tra huong cua tat ca cac canh.
    """
    n = len(vertices)
    if n < 3:
        return False
    sign = 0
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        cross_product = (px - x1) * (y2 - y1) - (py - y1) * (x2 - x1)
        if cross_product != 0:
            current_sign = 1 if cross_product > 0 else -1
            if sign == 0:
                sign = current_sign
            elif sign != current_sign:
                return False
    return True

def is_point_in_polygon(px, py, vertices):
    """
    Kiem tra mot diem (px, py) co nam trong da giac bat ky (loi hoac lom) hay khong.
    Su dung thuat toan Ray Casting (Jordan Curve Theorem).
    """
    n = len(vertices)
    if n < 3:
        return False
    inside = False
    x1, y1 = vertices[0]
    for i in range(n + 1):
        x2, y2 = vertices[i % n]
        if py > min(y1, y2):
            if py <= max(y1, y2):
                if px <= max(x1, x2):
                    if y1 != y2:
                        x_inters = (py - y1) * (x2 - x1) / (y2 - y1) + x1
                        if x1 == x2 or px <= x_inters:
                            inside = not inside
        x1, y1 = x2, y2
    return inside

def scanline_polygon_fill(vertices, color_tuple=(3, 105, 161)):
    """
    To mau da giac bang thuat toan Scanline Fill.
    """
    if len(vertices) < 3:
        return []
    pixels = []
    ymin = int(min(y for _, y in vertices))
    ymax = int(max(y for _, y in vertices))
    
    # Lay cac canh
    edges = []
    n = len(vertices)
    for i in range(n):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        if p1[1] != p2[1]: # Bo qua cac canh nam ngang
            if p1[1] < p2[1]:
                edges.append((p1, p2))
            else:
                edges.append((p2, p1))
                
    for y in range(ymin, ymax + 1):
        # Tim giao diem cua scanline y voi cac canh
        intersections = []
        for p1, p2 in edges:
            if p1[1] <= y < p2[1]:
                # Giao diem tuyen tinh
                x = p1[0] + (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])
                intersections.append(x)
        intersections.sort()
        for i in range(0, len(intersections) - 1, 2):
            x_start = int(round(intersections[i]))
            x_end = int(round(intersections[i+1]))
            for x in range(x_start, x_end + 1):
                pixels.append((x, y, color_tuple))
    return pixels

def flood_fill(start_x, start_y, is_inside_boundary, color_tuple=(3, 105, 161), max_pixels=50000):
    """
    To mau bang thuat toan Loang (Flood Fill).
    Su dung co che hang doi (queue-based BFS) de tranh loi Stack Overflow tren Python.
    is_inside_boundary: function nhan vao (x, y) tra ve True neu diem do can duoc to mau.
    """
    pixels = []
    visited = set()
    queue = [(start_x, start_y)]
    visited.add((start_x, start_y))
    
    while queue and len(pixels) < max_pixels:
        cx, cy = queue.pop(0)
        if is_inside_boundary(cx, cy):
            pixels.append((cx, cy, color_tuple))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return pixels

if __name__ == "__main__":
    # Test check cho cac thuat toan vua duoc them (ponytail: test nhanh khong can framework)
    test_vertices = [(0, 0), (4, 0), (4, 4), (0, 4)] # Hinh vuong
    assert is_point_in_convex_polygon(2, 2, test_vertices) == True, "Diem o giua phai trong da giac"
    assert is_point_in_convex_polygon(5, 5, test_vertices) == False, "Diem ben ngoai phai ngoai da giac"
    assert is_point_in_polygon(2, 2, test_vertices) == True, "Diem o giua phai trong da giac (Jordan)"
    assert is_point_in_polygon(5, 5, test_vertices) == False, "Diem ngoai phai ngoai da giac (Jordan)"
    scanline_px = scanline_polygon_fill(test_vertices)
    assert len(scanline_px) > 0, "Scanline fill phai tra ve cac pixel"
    flood_px = flood_fill(2, 2, lambda x, y: 0 <= x <= 4 and 0 <= y <= 4)
    assert len(flood_px) > 0, "Flood fill phai loang duoc pixel"
    print("Moi bai kiem tra thiet lap thành cong!")
