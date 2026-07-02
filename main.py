import sys
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication


class MainFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Thực Hành Đồ Họa Máy Tính")
        self.resize(1280, 720)
        self.can_giua_man_hinh()

        self.card_layout_manager = QStackedWidget()
        self.setCentralWidget(self.card_layout_manager)

        self.danh_sach_man_hinh = {}

        # 1. Khởi tạo Menu chính
        from View.StartPanel import StartPanel
        self.start_panel = StartPanel(self)
        self.addScreen(self.start_panel, "ExerciseList")

        # 2. Đăng ký danh sách các bài tập thực hành
        self.khoi_tao_cac_bai_thuc_hanh()

        self.showScreen("ExerciseList")

    def khoi_tao_cac_bai_thuc_hanh(self):
        """Nơi duy nhất bạn khai báo bài tập mới."""
        from View.ExercisesPanel import Chuong1Panel
        self.addScreen(Chuong1Panel(self), "Chuong_1")

    def addScreen(self, widget, name):
        self.card_layout_manager.addWidget(widget)
        self.danh_sach_man_hinh[name] = self.card_layout_manager.indexOf(widget)

    def showScreen(self, name):
        if name in self.danh_sach_man_hinh:
            self.card_layout_manager.setCurrentIndex(self.danh_sach_man_hinh[name])

    def can_giua_man_hinh(self):
        khung_man_hinh = QApplication.primaryScreen().availableGeometry().center()
        khung_cua_so = self.frameGeometry()
        khung_cua_so.moveCenter(khung_man_hinh)
        self.move(khung_cua_so.topLeft())


def main():
    app = QApplication(sys.argv)

    chuong_trinh = MainFrame()
    chuong_trinh.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
