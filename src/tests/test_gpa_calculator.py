import pytest
from gpa_calculator import calculate_gpa


def test_single_course_returns_its_grade_points():
    assert calculate_gpa([{'grade': 'A', 'credits': 4}]) == 4.0


def test_gpa_is_weighted_by_credits():
    enrollments = [
        {'grade': 'A', 'credits': 4},
        {'grade': 'B', 'credits': 3},
    ]
    assert calculate_gpa(enrollments) == pytest.approx((4.0 * 4 + 3.0 * 3) / 7)


def test_missing_and_unknown_grades_are_ignored():
    enrollments = [
        {'grade': 'A', 'credits': 4},
        {'grade': None, 'credits': 3},
        {'grade': 'Z', 'credits': 3},
    ]
    assert calculate_gpa(enrollments) == 4.0


def test_no_graded_courses_returns_zero():
    assert calculate_gpa([]) == 0
