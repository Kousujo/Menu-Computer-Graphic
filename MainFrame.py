# MainFrame.py
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication

class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Thực Hành Đồ Họa Máy Tính")
        
        # Đặt kích thước cửa sổ
        self.resize(1200, 700)
        self.can_giua_man_hinh()

        # CardLayout quản lý tập trung các màn hình giao diện
        self.card_layout_manager = QStackedWidget()
        self.setCentralWidget(self.card_layout_manager)

        # Từ điển lưu vị trí index của các màn hình
        self.danh_sach_man_hinh = {}

        # -----------------------------------------------------------------
        # QUY HOẠCH NẠP MÔ-ĐUN TẬP TRUNG (MVC CONTROLLER)
        # -----------------------------------------------------------------
        # 1. Khởi tạo Menu chính (Nạp từ thư mục exercises)
        from exercises.ExerciseListPanel import ExerciseListPanel
        self.exercise_list_panel = ExerciseListPanel(self)
        self.addScreen(self.exercise_list_panel, "ExerciseList")

        # 2. Đăng ký danh sách các bài tập thực hành tại đây
        self.khoi_tao_cac_bai_thuc_hanh()

        # Hiển thị menu chính lúc khởi động
        self.showScreen("ExerciseList")

    def khoi_tao_cac_bai_thuc_hanh(self):
        """
        Nơi duy nhất bạn khai báo bài tập mới.
        Khởi tạo các chương học: Chương 1 và Chương 2
        """
        from exercises.Chuong_1 import Chuong1Panel
        self.addScreen(Chuong1Panel(self), "Chuong_1")

        from exercises.Chuong_2 import Chuong2Panel
        self.addScreen(Chuong2Panel(self), "Chuong_2")

    def addScreen(self, widget, name):
        self.card_layout_manager.addWidget(widget)
        self.danh_sach_man_hinh[name] = self.card_layout_manager.indexOf(widget)

    def showScreen(self, name):
        if name in self.danh_sach_man_hinh:
            self.card_layout_manager.setCurrentIndex(self.danh_sach_man_hinh[name])

    def can_giua_man_hinh(self):
        khung_man_hinh = QApplication.primaryScreen().availableGeometry().center() # type: ignore
        khung_cua_so = self.frameGeometry()
        khung_cua_so.moveCenter(khung_man_hinh)
        self.move(khung_cua_so.topLeft())