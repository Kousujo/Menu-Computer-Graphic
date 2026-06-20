# core/algorithms.py

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

def midpoint_circle(xc, yc, r):
    """
    THUẬT TOÁN MIDPOINT VẼ ĐƯỜNG TRÒN
    - Nhận vào: Tọa độ tâm (xc, yc) và bán kính R.
    - Trả về: Danh sách các pixel (x, y) tạo nên đường tròn.
    - Nguyên lý: Chỉ tính toán cho 1/8 đường tròn (từ góc 90 độ đến 45 độ),
      sau đó lấy đối xứng gương ra 8 phần để được đường tròn hoàn chỉnh.
    """
    pixels = []
    x = 0
    y = r
    p = 1 - r  # Biến quyết định (Decision Parameter) ban đầu

    def duyet_8_diem(xc, yc, x, y):
        """ Hàm lấy đối xứng 1 điểm ra 8 vùng của đường tròn """
        return [
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ]

    # Nạp 8 điểm xuất phát đầu tiên (tại các đỉnh trục tọa độ)
    pixels.extend(duyet_8_diem(xc, yc, x, y))

    # Vòng lặp tính toán cho đến khi đường phân giác x = y cắt đồ thị (hết 1/8 đường tròn)
    while x < y:
        x += 1
        if p < 0:
            # Điểm tiếp theo nằm bên trong đường tròn tròn -> Chọn điểm (x+1, y)
            p = p + 2 * x + 1
        else:
            # Điểm tiếp theo nằm ngoài đường tròn -> Chọn hạ xuống (x+1, y-1)
            y -= 1
            p = p + 2 * (x - y) + 1
        
        # Lấy đối xứng các điểm mới tính được sang 8 hướng
        pixels.extend(duyet_8_diem(xc, yc, x, y))
        
    return pixels

# algorithms.py

def midpoint_ellipse(xc, yc, rx, ry):
    """
    THUẬT TOÁN MIDPOINT VẼ HÌNH ELIP
    - Nhận vào: Tâm (xc, yc), bán kính lớn rx, bán kính nhỏ ry.
    - Nguyên lý: Duyệt 1/4 hình elip ở góc phần tư thứ nhất, chia làm 2 miền:
      + Miền 1: Độ dốc tiếp tuyến < 1 (dx < dy) -> Tăng x, quyết định y.
      + Miền 2: Độ dốc tiếp tuyến > 1 (dx >= dy) -> Giảm y, quyết định x.
      Sau đó lấy đối xứng gương ra 4 hướng.
    """
    pixels = []
    x = 0
    y = ry

    # Các biến bình phương bổ trợ để tối ưu tốc độ tính toán
    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

    def duyet_4_diem(xc, yc, x, y):
        """ Hàm lấy đối xứng 1 điểm ra 4 góc phần tư của Elip """
        return [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y)
        ]

    # -----------------------------------------------------------------
    # MIỀN 1: Tiếp tuyến có độ dốc < 1 (dx < dy)
    # -----------------------------------------------------------------
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = two_ry2 * x
    dy = two_rx2 * y

    while dx < dy:
        pixels.extend(duyet_4_diem(xc, yc, x, y))
        x += 1
        if p1 < 0:
            dx = dx + two_ry2
            p1 = p1 + dx + ry2
        else:
            y -= 1
            dx = dx + two_ry2
            dy = dy - two_rx2
            p1 = p1 + dx - dy + ry2
            
    # -----------------------------------------------------------------
    # MIỀN 2: Tiếp tuyến có độ dốc >= 1 (dx >= dy)
    # -----------------------------------------------------------------
    p2 = (ry2 * (x + 0.5) * (x + 0.5)) + (rx2 * (y - 1) * (y - 1)) - (rx2 * ry2)

    while y >= 0:
        pixels.extend(duyet_4_diem(xc, yc, x, y))
        y -= 1
        if p2 > 0:
            dy = dy - two_rx2
            p2 = p2 + rx2 - dy
        else:
            x += 1
            dx = dx + two_ry2
            dy = dy - two_rx2
            p2 = p2 + dx - dy + rx2

    return pixels

def math_to_pixel(x_math, y_math, x_tam, y_tam, scale=40):
    """
    Ánh xạ tọa độ Đề-các (thực) sang tọa độ Pixel màn hình (nguyên)
    - scale: số pixel tương ứng với 1 đơn vị toán học (mặc định 40px = 1đv)
    - Trục Y toán học hướng lên, trục Y màn hình hướng xuống dưới nên phải trừ (-)
    """
    x_pixel = int(round(x_tam + x_math * scale))
    y_pixel = int(round(y_tam - y_math * scale))
    return x_pixel, y_pixel