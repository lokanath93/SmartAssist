"""Tests for smartassist.detector."""
import pytest

from smartassist.detector import euclidean_distance, eye_aspect_ratio
from smartassist import config
from tests.conftest import MockLandmark


def test_euclidean_distance_same_point():
    p = MockLandmark(0.5, 0.5)
    assert euclidean_distance(p, p) == 0.0


def test_euclidean_distance_horizontal():
    a = MockLandmark(0.0, 0.0)
    b = MockLandmark(3.0, 0.0)
    assert euclidean_distance(a, b) == 3.0


def test_euclidean_distance_vertical():
    a = MockLandmark(0.0, 0.0)
    b = MockLandmark(0.0, 4.0)
    assert euclidean_distance(a, b) == 4.0


def test_euclidean_distance_diagonal():
    a = MockLandmark(0.0, 0.0)
    b = MockLandmark(3.0, 4.0)
    assert abs(euclidean_distance(a, b) - 5.0) < 1e-6


def test_eye_aspect_ratio_returns_float(mock_landmark_list):
    ear = eye_aspect_ratio(mock_landmark_list, config.LEFT_EYE_INDICES)
    assert isinstance(ear, (float, int))
    assert ear >= 0


def test_eye_aspect_ratio_zero_denominator():
    # All same point -> C = 0, should return 0.0 (guarded in implementation)
    landmarks = [MockLandmark(0.5, 0.5) for _ in range(400)]
    ear = eye_aspect_ratio(landmarks, config.LEFT_EYE_INDICES)
    assert ear == 0.0


def test_eye_aspect_ratio_both_eyes_non_negative(mock_landmark_list, closed_eye_landmarks):
    """EAR is non-negative for both open and closed eye fixtures."""
    ear_open = eye_aspect_ratio(mock_landmark_list, config.LEFT_EYE_INDICES)
    ear_closed = eye_aspect_ratio(closed_eye_landmarks, config.LEFT_EYE_INDICES)
    assert ear_open >= 0 and ear_closed >= 0
