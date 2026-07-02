"""Tests for core/algorithms.py — pure logic, no GUI needed."""

import math
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.algorithms import (
    bresenham_line,
    midpoint_line,
    midpoint_circle,
    midpoint_ellipse,
    math_to_pixel,
)


class TestBresenhamLine:
    def test_horizontal_line(self):
        pts = bresenham_line(0, 0, 10, 0)
        assert len(pts) == 11
        assert pts[0] == (0, 0)
        assert pts[-1] == (10, 0)
        assert all(y == 0 for _, y in pts)

    def test_vertical_line(self):
        pts = bresenham_line(5, 0, 5, 7)
        assert len(pts) == 8
        assert all(x == 5 for x, _ in pts)

    def test_diagonal_line(self):
        pts = bresenham_line(0, 0, 5, 5)
        assert len(pts) == 6
        assert pts[-1] == (5, 5)

    def test_single_point(self):
        assert bresenham_line(3, 3, 3, 3) == [(3, 3)]

    def test_reverse_direction(self):
        pts = bresenham_line(10, 10, 0, 0)
        assert pts[0] == (10, 10) and pts[-1] == (0, 0)

    def test_negative_coordinates(self):
        pts = bresenham_line(-5, -5, 0, 0)
        assert pts[0] == (-5, -5) and pts[-1] == (0, 0)


class TestMidpointLine:
    def test_horizontal(self):
        pts = midpoint_line(0, 0, 10, 0)
        assert len(pts) == 11 and pts[0] == (0, 0) and pts[-1] == (10, 0)

    def test_vertical(self):
        pts = midpoint_line(3, 0, 3, 8)
        assert len(pts) == 9 and all(x == 3 for x, _ in pts)

    def test_steep_slope(self):
        """|m| > 1 case (y is driving variable)."""
        pts = midpoint_line(0, 0, 2, 10)
        assert pts[0] == (0, 0) and pts[-1] == (2, 10)

    def test_single_point(self):
        assert midpoint_line(5, 5, 5, 5) == [(5, 5)]

    def test_negative_slope(self):
        pts = midpoint_line(0, 5, 5, 0)
        assert pts[0] == (0, 5) and pts[-1] == (5, 0)

    def test_bresenham_equivalence(self):
        for x1, y1, x2, y2 in [(0,0,7,3), (1,1,8,5), (10,10,2,3)]:
            b, m = bresenham_line(x1,y1,x2,y2), midpoint_line(x1,y1,x2,y2)
            assert b[0] == m[0] and b[-1] == m[-1]


class TestMidpointCircle:
    def test_radius_one(self):
        assert len(midpoint_circle(0, 0, 1)) > 0

    def test_zero_radius(self):
        assert midpoint_circle(0, 0, 0) == []

    def test_negative_radius(self):
        assert midpoint_circle(0, 0, -1) == []

    def test_center_nonzero(self):
        pts = midpoint_circle(100, 100, 5)
        assert len(pts) > 0
        for x, y in pts:
            d = math.sqrt((x-100)**2 + (y-100)**2)
            assert abs(d - 5) <= 6  # ponytail: pixel approximation

    def test_large_radius(self):
        assert len(midpoint_circle(0, 0, 50)) > 100


class TestMidpointEllipse:
    def test_invalid_radii(self):
        assert midpoint_ellipse(0, 0, 0, 5) == []
        assert midpoint_ellipse(0, 0, 5, 0) == []
        assert midpoint_ellipse(0, 0, -3, 4) == []

    def test_circle_as_ellipse(self):
        assert len(midpoint_ellipse(0, 0, 20, 20)) > 50

    def test_flat_ellipse(self):
        assert len(midpoint_ellipse(0, 0, 30, 10)) > 50


class TestMathToPixel:
    def test_origin(self):
        assert math_to_pixel(0, 0, 400, 300, 20) == (400, 300)

    def test_positive_x(self):
        assert math_to_pixel(5, 0, 400, 300, 20) == (500, 300)

    def test_positive_y_math_negative_pixel(self):
        assert math_to_pixel(0, 5, 400, 300, 20) == (400, 200)
