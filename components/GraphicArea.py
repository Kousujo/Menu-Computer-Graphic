from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF, QPoint, QTimer
from PyQt6.QtGui import QPainter, QColor, QPen, QTransform

class GraphicArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #ffffff; border: 2px solid #e0e0e0; border-radius: 8px;")
        self.danh_sach_pixel = []
        
        self.he_so_zoom = 1.0
        self.goc_toa_do_pan = QPointF(0, 0)
        self.vi_tri_chuot_cu = QPointF()
        self.dang_keo_chuot = False

        # Animation engine
        self._timer_hoat_anh = QTimer(self)
        self._timer_hoat_anh.setInterval(10)
        self._timer_hoat_anh.timeout.connect(self._xu_ly_frame_hoat_anh)
        self._generator_hoat_anh = None
        self._dang_hoat_anh = False

    def dat_lai_khung_nhin(self):
        self.he_so_zoom = 1.0
        self.goc_toa_do_pan = QPointF(0, 0)
        self.update()

    def cap_nhat_hinh_ve(self, danh_sach_pixel):
        self.danh_sach_pixel = danh_sach_pixel
        self.update()

    def cap_nhat_hinh_ve_co_hoat_anh(self, generator):
        """Nhận generator, chạy animation với QTimer (nhịp 10ms)."""
        self._timer_hoat_anh.stop()
        self.danh_sach_pixel = []
        self._generator_hoat_anh = generator
        self._dang_hoat_anh = True
        self._timer_hoat_anh.start()

    def _xu_ly_frame_hoat_anh(self):
        """Callback QTimer: lấy batch tiếp theo từ generator và vẽ."""
        gen = self._generator_hoat_anh
        if gen is None:
            self._timer_hoat_anh.stop()
            self._dang_hoat_anh = False
            return
        try:
            batch = next(gen)
            self.danh_sach_pixel.extend(batch)
            self.update()
        except StopIteration:
            self._timer_hoat_anh.stop()
            self._dang_hoat_anh = False
            self._generator_hoat_anh = None

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 1. Bật khử răng cưa riêng cho đường lưới để nét đứt không bị gãy
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        ma_tran = QTransform()
        ma_tran.translate(self.goc_toa_do_pan.x(), self.goc_toa_do_pan.y())
        ma_tran.scale(self.he_so_zoom, self.he_so_zoom)
        painter.setTransform(ma_tran)

        but_luoi = QPen(QColor("#cbd5e1"), 1, Qt.PenStyle.DashLine)
        painter.setPen(but_luoi)

        khoang_cach_o_luoi = 100
        gioi_han_ao = 4000 

        for x in range(-gioi_han_ao, gioi_han_ao, khoang_cach_o_luoi):
            painter.drawLine(x, -gioi_han_ao, x, gioi_han_ao)

        for y in range(-gioi_han_ao, gioi_han_ao, khoang_cach_o_luoi):
            painter.drawLine(-gioi_han_ao, y, gioi_han_ao, y)
            
        but_truc_goc = QPen(QColor("#94a3b8"), 1.5, Qt.PenStyle.SolidLine)
        painter.setPen(but_truc_goc)
        painter.drawLine(0, -gioi_han_ao, 0, gioi_han_ao)
        painter.drawLine(-gioi_han_ao, 0, gioi_han_ao, 0)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        but_mac_dinh = QPen(QColor("#1e293b"), 3)
        painter.setPen(but_mac_dinh)
        
        if self.danh_sach_pixel:
            for p in self.danh_sach_pixel:
                if len(p) == 3: # Định dạng chương 2: (x, y, (r, g, b))
                    x, y, color = p
                    painter.setPen(QPen(QColor(color[0], color[1], color[2]), 3))
                    painter.drawPoint(int(x), int(y))
                elif len(p) == 2: # Định dạng chương 1: (x, y)
                    x, y = p
                    painter.setPen(but_mac_dinh)
                    painter.drawPoint(int(x), int(y))

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.he_so_zoom *= 1.15
        else:
            self.he_so_zoom /= 1.15
        self.he_so_zoom = max(0.2, min(self.he_so_zoom, 30.0))
        self.update()

    def mousePressEvent(self, event):
        if event.button() in [Qt.MouseButton.RightButton, Qt.MouseButton.MiddleButton]:
            self.dang_keo_chuot = True
            self.vi_tri_chuot_cu = event.position()

    def mouseMoveEvent(self, event):
        if self.dang_keo_chuot:
            vi_tri_hien_tai = event.position()
            dx = (vi_tri_hien_tai.x() - self.vi_tri_chuot_cu.x()) / self.he_so_zoom
            dy = (vi_tri_hien_tai.y() - self.vi_tri_chuot_cu.y()) / self.he_so_zoom
            self.goc_toa_do_pan += QPointF(dx, dy)
            self.vi_tri_chuot_cu = vi_tri_hien_tai
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() in [Qt.MouseButton.RightButton, Qt.MouseButton.MiddleButton]:
            self.dang_keo_chuot = False