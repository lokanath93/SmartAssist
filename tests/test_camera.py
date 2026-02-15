"""Tests for smartassist.camera."""
from unittest.mock import MagicMock, patch

import pytest


@patch("smartassist.camera.cv2.VideoCapture")
def test_open_camera_uses_index_from_config(mock_capture):
    mock_capture.return_value.isOpened.return_value = True
    with patch("smartassist.camera.config.get_camera_index", return_value=0):
        from smartassist.camera import open_camera

        cap = open_camera()
        assert cap is not None
        mock_capture.assert_called()


def test_read_frame_rgb_returns_tuple():
    """read_frame_rgb returns (success, image)."""
    from smartassist.camera import read_frame_rgb

    mock_cap = MagicMock()
    mock_cap.read.return_value = (False, None)
    success, img = read_frame_rgb(mock_cap)
    assert success is False
    assert img is None
