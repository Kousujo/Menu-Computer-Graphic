import sys
from PyQt6.QtWidgets import QApplication
from MainFrame import MainFrame

def main():
    app = QApplication(sys.argv)
    
    chuong_trinh = MainFrame()
    chuong_trinh.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()