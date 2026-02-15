"""Tests for smartassist.controller."""
from unittest.mock import MagicMock, patch

import pytest

from smartassist.controller import MouseController
from smartassist import config
from tests.conftest import MockLandmark, mock_landmark_list

# In CI/headless, pyautogui.size() may return (0,0). Use a fixed size for tests.
FAKE_SIZE = (1920, 1080)


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
def test_controller_screen_size(mock_size):
    c = MouseController()
    assert c.screen_width == 1920 and c.screen_height == 1080


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
def test_clamp_to_screen_inside(mock_size):
    c = MouseController()
    x, y = c.clamp_to_screen(100, 200)
    assert x == 100 and y == 200


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
def test_clamp_to_screen_negative(mock_size):
    c = MouseController()
    x, y = c.clamp_to_screen(-10, -20)
    assert x == 0 and y == 0


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
def test_clamp_to_screen_over_bounds(mock_size):
    c = MouseController()
    x, y = c.clamp_to_screen(c.screen_width + 100, c.screen_height + 100)
    assert x == c.screen_width - 1 and y == c.screen_height - 1


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
def test_landmarks_to_mouse_returns_two_ints(mock_size, mock_landmark_list):
    c = MouseController()
    nose = mock_landmark_list[config.NOSE_TIP_INDEX]
    x, y = c.landmarks_to_mouse(nose)
    assert isinstance(x, int) and isinstance(y, int)
    assert 0 <= x < c.screen_width and 0 <= y < c.screen_height


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
@patch("smartassist.controller.pyautogui")
def test_update_moves_mouse(mock_pyautogui, mock_size, mock_landmark_list):
    c = MouseController()
    c.update(mock_landmark_list)
    mock_pyautogui.moveTo.assert_called_once()
    args = mock_pyautogui.moveTo.call_args[0]
    assert len(args) == 2
    assert 0 <= args[0] < c.screen_width and 0 <= args[1] < c.screen_height


@patch("smartassist.controller.pyautogui.size", return_value=FAKE_SIZE)
@patch("smartassist.controller.pyautogui")
def test_update_returns_bool(mock_pyautogui, mock_size, mock_landmark_list):
    """update() returns True when a click was triggered, else False."""
    c = MouseController()
    result = c.update(mock_landmark_list)
    assert isinstance(result, bool)
