import pytest
from PyQt6.QtCore import Qt
from exercises.Bai_3 import Bai3Panel

# Giả lập một class MainFrame tối giản để Bai3Panel không bị lỗi khi gọi self.mainframe
class MockMainFrame:
    pass

def test_ve_ham_bac_nhat_tu_dong(qtbot):
    # 1. Khởi tạo giao diện Bai3Panel trong môi trường test
    mock_frame = MockMainFrame()
    panel = Bai3Panel(mock_frame)
    qtbot.addWidget(panel) # Đăng ký widget vào bot để kiểm soát
    
    # 2. Giả lập nhập liệu tự động vào các ô input
    # Ví dụ: Sửa hệ số a thành '2' và b thành '3'
    panel.inputs["a"].clear()
    qtbot.keyClicks(panel.inputs["a"], "2")
    
    panel.inputs["b"].clear()
    qtbot.keyClicks(panel.inputs["b"], "3")
    
    # 3. Giả lập tự động gọi hàm vẽ (hoặc nếu bạn có nút bấm thì giả lập click nút)
    panel.xu_ly_logic_ve()
    
    # 4. KIỂM TRA TỰ ĐỘNG (Assert)
    # Kiểm tra xem danh sách pixel sau khi vẽ có dữ liệu hay không (không bị rỗng)
    assert len(panel.canvas.danh_sach_pixel) > 0
    
    # Kiểm tra xem trục tọa độ đã được đưa về chính giữa màn hình chưa (tính năng mới sửa)
    expected_x = panel.canvas.width() / 2
    expected_y = panel.canvas.height() / 2
    assert panel.canvas.goc_toa_do_pan.x() == expected_x
    assert panel.canvas.goc_toa_do_pan.y() == expected_y

def test_nhap_chu_gay_loi_tu_dong(qtbot):
    mock_frame = MockMainFrame()
    panel = Bai3Panel(mock_frame)
    qtbot.addWidget(panel)
    
    # Giả lập nhập chữ "abc" vào ô hệ số để test xem bộ bắt lỗi ValueError có hoạt động không
    panel.inputs["a"].clear()
    qtbot.keyClicks(panel.inputs["a"], "abc")
    
    # Chạy hàm vẽ, nếu code của bạn bắt lỗi tốt và hiện QMessageBox, test sẽ pass
    panel.xu_ly_logic_ve()