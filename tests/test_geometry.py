"""Tests for core/geometry.py — pure logic, no GUI needed."""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.geometry import (
    ToaDo2D,
    STamGiac,
    DienTich,
    get_circle_pixels,
)

class TestCircleGeometry:
    def test_positive_radius(self):
        assert len(get_circle_pixels(0, 0, 30)) > 0

    def test_zero_radius(self):
        assert get_circle_pixels(0, 0, 0) == []

class TestSTamGiac:
    def test_right_triangle_3_4_5(self):
        """Tam giác vuông 3-4-5 → diện tích = 6."""
        A = ToaDo2D(0, 0)
        B = ToaDo2D(3, 0)
        C = ToaDo2D(0, 4)
        assert STamGiac(A, B, C) == 6

    def test_right_triangle_swapped_order(self):
        """Thứ tự đỉnh không ảnh hưởng kết quả."""
        A = ToaDo2D(0, 0)
        B = ToaDo2D(0, 4)
        C = ToaDo2D(3, 0)
        assert STamGiac(B, C, A) == 6

    def test_collinear_points(self):
        """Ba điểm thẳng hàng → diện tích = 0."""
        A = ToaDo2D(0, 0)
        B = ToaDo2D(2, 2)
        C = ToaDo2D(4, 4)
        assert STamGiac(A, B, C) == 0

    def test_arbitrary_triangle(self):
        """Tam giác bất kỳ: (0,0), (5,1), (2,6) → 14."""
        A = ToaDo2D(0, 0)
        B = ToaDo2D(5, 1)
        C = ToaDo2D(2, 6)
        assert STamGiac(A, B, C) == 14

    def test_negative_coordinates(self):
        """Tọa độ âm: (-2,-2), (2,-2), (0,2) → 8."""
        A = ToaDo2D(-2, -2)
        B = ToaDo2D(2, -2)
        C = ToaDo2D(0, 2)
        assert STamGiac(A, B, C) == 8


class TestDienTich:
    def test_unit_square(self):
        """Hình vuông đơn vị → diện tích = 1."""
        P = [ToaDo2D(0, 0), ToaDo2D(1, 0), ToaDo2D(1, 1), ToaDo2D(0, 1)]
        assert DienTich(P, 4) == 1

    def test_rectangle_4x5(self):
        """Hình chữ nhật 4×5 → diện tích = 20."""
        P = [ToaDo2D(0, 0), ToaDo2D(4, 0), ToaDo2D(4, 5), ToaDo2D(0, 5)]
        assert DienTich(P, 4) == 20

    def test_triangle_via_polygon(self):
        """Tam giác thông qua DienTich → 6."""
        P = [ToaDo2D(0, 0), ToaDo2D(3, 0), ToaDo2D(0, 4)]
        assert DienTich(P, 3) == 6

    def test_less_than_3_vertices(self):
        """Đa giác < 3 đỉnh → diện tích = 0."""
        P = [ToaDo2D(0, 0), ToaDo2D(5, 5)]
        assert DienTich(P, 2) == 0
        assert DienTich(P, 1) == 0
        assert DienTich([], 0) == 0

    def test_regular_hexagon_approx(self):
        """Lục giác đều gần đúng: kiểm tra DienTich > 0."""
        import math
        P = []
        for i in range(6):
            angle = math.pi / 3 * i
            P.append(ToaDo2D(math.cos(angle), math.sin(angle)))
        area = DienTich(P, 6)
        # Diện tích lục giác đều cạnh 1 ≈ 2.598 → int = 2
        assert area == 2

    def test_concave_polygon_still_works(self):
        """Shoelace vẫn tính đúng cho đa giác lõm (diện tích hình học)."""
        P = [ToaDo2D(0, 0), ToaDo2D(3, 0), ToaDo2D(1, 1), ToaDo2D(3, 3), ToaDo2D(0, 3)]
        assert DienTich(P, 5) > 0

    def test_polygon_with_negative_coordinates(self):
        """Đa giác có tọa độ âm."""
        P = [ToaDo2D(-2, -2), ToaDo2D(2, -2), ToaDo2D(2, 2), ToaDo2D(-2, 2)]
        assert DienTich(P, 4) == 16
