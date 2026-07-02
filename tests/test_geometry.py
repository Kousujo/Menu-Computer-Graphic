"""Tests for core/geometry.py — pure logic, no GUI needed."""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.geometry import (
    ToaDo2D,
    get_triangle_pixels,
    get_rectangle_pixels,
    get_parallelogram_pixels,
    get_rhombus_pixels,
    get_isosceles_trapezoid_pixels,
    get_star_pixels,
    get_circle_pixels,
    get_target_pixels,
    get_flower_8_petals_pixels,
    get_flower_24_petals_pixels,
    get_wheel_with_spokes_pixels,
    get_circular_pattern_8_petals_pixels,
    get_star_with_inner_circle_pixels,
    get_line_function_pixels,
    get_quadratic_function_pixels,
    get_cubic_function_pixels,
    get_rational_1_1_pixels,
    get_rational_2_1_pixels,
    DrawPoly,
    Circle3P,
    Arc3P,
)


class TestTriangle:
    def test_invalid_triangle(self):
        assert get_triangle_pixels(0, 0, 1, 1, 3) == []

    def test_valid_triangle(self):
        assert len(get_triangle_pixels(0, 0, 5, 5, 5)) > 0

    def test_zero_side(self):
        assert get_triangle_pixels(0, 0, 0, 5, 5) == []


class TestRectangle:
    def test_basic(self):
        assert len(get_rectangle_pixels(0, 0, 100, 50)) > 0

    def test_square(self):
        assert len(get_rectangle_pixels(0, 0, 50, 50)) > 0


class TestParallelogram:
    def test_basic(self):
        assert len(get_parallelogram_pixels(0, 0, 100, 50, 10)) > 0


class TestRhombus:
    def test_basic(self):
        assert len(get_rhombus_pixels(0, 0, 100, 60)) > 0


class TestIsoscelesTrapezoid:
    def test_basic(self):
        assert len(get_isosceles_trapezoid_pixels(0, 0, 100, 60, 50)) > 0


class TestStar:
    def test_basic(self):
        assert len(get_star_pixels(0, 0, 50, 20)) > 0


class TestCircleGeometry:
    def test_positive_radius(self):
        assert len(get_circle_pixels(0, 0, 30)) > 0

    def test_zero_radius(self):
        assert get_circle_pixels(0, 0, 0) == []


class TestTarget:
    def test_basic(self):
        assert len(get_target_pixels(0, 0, 50, 3)) > 0

    def test_zero_rings(self):
        assert get_target_pixels(0, 0, 50, 0) == []


class TestFlower8Petals:
    def test_basic(self):
        assert len(get_flower_8_petals_pixels(0, 0, 80, 30)) > 0


class TestFlower24Petals:
    def test_basic(self):
        assert len(get_flower_24_petals_pixels(0, 0, 30, 80)) > 0


class TestWheelWithSpokes:
    def test_basic(self):
        assert len(get_wheel_with_spokes_pixels(0, 0, 80)) > 0


class TestCircularPattern8Petals:
    def test_basic(self):
        assert len(get_circular_pattern_8_petals_pixels(0, 0, 80)) > 0


class TestStarWithInnerCircle:
    def test_basic(self):
        assert len(get_star_with_inner_circle_pixels(0, 0, 30, 70)) > 0


class TestDrawPoly:
    def test_less_than_3(self):
        assert DrawPoly([ToaDo2D()]*2, 2, 0, 0, 50) == []

    def test_triangle(self):
        P = [ToaDo2D() for _ in range(3)]
        pts = DrawPoly(P, 3, 0, 0, 50)
        assert len(pts) > 0
        for p in P:
            assert p.x != 0 or p.y != 0

    def test_hexagon(self):
        P = [ToaDo2D() for _ in range(6)]
        assert len(DrawPoly(P, 6, 0, 0, 50)) > 0

    def test_zero_radius(self):
        assert DrawPoly([ToaDo2D()]*3, 3, 0, 0, 0) == []


class TestCircle3P:
    def test_collinear(self):
        assert Circle3P(ToaDo2D(0,0), ToaDo2D(1,0), ToaDo2D(2,0)) == []

    def test_non_collinear(self):
        assert len(Circle3P(ToaDo2D(0,0), ToaDo2D(4,0), ToaDo2D(2,3))) > 0


class TestArc3P:
    def test_collinear(self):
        assert Arc3P(ToaDo2D(0,0), ToaDo2D(1,0), ToaDo2D(2,0)) == []

    def test_non_collinear(self):
        assert len(Arc3P(ToaDo2D(0,0), ToaDo2D(2,2), ToaDo2D(4,0))) > 0


class TestLineFunction:
    def test_basic(self):
        pts = get_line_function_pixels(0, 0, 1, 0, -15, 15, 0.1, 40)
        assert len(pts) > 0


class TestQuadraticFunction:
    def test_basic(self):
        pts = get_quadratic_function_pixels(0, 0, 1, 0, 0, -15, 15, 0.05, 40)
        assert len(pts) > 0


class TestCubicFunction:
    def test_basic(self):
        pts = get_cubic_function_pixels(0, 0, 1, 0, 0, 0, -15, 15, 0.05, 40)
        assert len(pts) > 0


class TestRational1_1:
    def test_basic(self):
        pts = get_rational_1_1_pixels(0, 0, 1, 0, 1, 0, -15, 15, 0.02, 40)
        assert len(pts) > 0

    def test_vertical_asymptote(self):
        pts = get_rational_1_1_pixels(0, 0, 1, 0, 1, 0, -15, 15, 0.02, 40)
        assert isinstance(pts, list)


class TestRational2_1:
    def test_basic(self):
        pts = get_rational_2_1_pixels(0, 0, 1, 0, 0, 1, 0, -15, 15, 0.02, 40)
        assert len(pts) > 0

    def test_vertical_asymptote(self):
        pts = get_rational_2_1_pixels(0, 0, 1, 0, 0, 1, 0, -15, 15, 0.02, 40)
        assert isinstance(pts, list)
