"""Pytest fixtures: mock landmarks and helpers."""
import pytest


class MockLandmark:
    """Minimal landmark with .x, .y for EAR and nose."""

    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z


@pytest.fixture
def mock_landmark_list():
    """List of 478 mock landmarks. Only indices used for EAR and nose are set."""
    landmarks = [MockLandmark(0.0, 0.0) for _ in range(478)]
    # Nose tip (index 4)
    landmarks[4] = MockLandmark(0.5, 0.4)
    # Left eye (indices 362, 385, 387, 263, 373, 380) - open eye: vertical smaller than horizontal
    for i in [362, 385, 387, 263, 373, 380]:
        landmarks[i] = MockLandmark(0.3 + (i % 10) * 0.01, 0.35 + (i % 7) * 0.01)
    landmarks[362].x, landmarks[362].y = 0.30, 0.35
    landmarks[385].x, landmarks[385].y = 0.31, 0.34
    landmarks[387].x, landmarks[387].y = 0.32, 0.35
    landmarks[263].x, landmarks[263].y = 0.33, 0.35
    landmarks[373].x, landmarks[373].y = 0.31, 0.36
    landmarks[380].x, landmarks[380].y = 0.32, 0.36
    # Right eye (33, 160, 158, 133, 153, 144)
    landmarks[33].x, landmarks[33].y = 0.38, 0.35
    landmarks[160].x, landmarks[160].y = 0.39, 0.34
    landmarks[158].x, landmarks[158].y = 0.40, 0.35
    landmarks[133].x, landmarks[133].y = 0.41, 0.35
    landmarks[153].x, landmarks[153].y = 0.39, 0.36
    landmarks[144].x, landmarks[144].y = 0.40, 0.36
    return landmarks


@pytest.fixture
def closed_eye_landmarks(mock_landmark_list):
    """Same as mock_landmark_list but left eye more closed (smaller vertical)."""
    lst = mock_landmark_list
    # Make vertical distance smaller -> lower EAR
    lst[385].y = 0.352
    lst[387].y = 0.353
    lst[373].y = 0.354
    lst[380].y = 0.355
    return lst
