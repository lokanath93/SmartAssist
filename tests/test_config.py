"""Tests for smartassist.config."""
import os

import pytest

from smartassist import config


def test_script_dir_is_absolute():
    assert os.path.isabs(config.SCRIPT_DIR)


def test_model_path_under_script_dir():
    assert config.MODEL_PATH.startswith(config.SCRIPT_DIR)
    assert config.MODEL_PATH.endswith("face_landmarker.task")


def test_model_url_is_https():
    assert config.MODEL_URL.startswith("https://")


def test_get_camera_index_default(monkeypatch):
    monkeypatch.delenv("SMARTASSIST_CAMERA", raising=False)
    assert config.get_camera_index() == 0


def test_get_camera_index_from_env(monkeypatch):
    monkeypatch.setenv("SMARTASSIST_CAMERA", "2")
    assert config.get_camera_index() == 2


def test_is_voice_enabled_default(monkeypatch):
    monkeypatch.delenv("SMARTASSIST_VOICE", raising=False)
    assert config.is_voice_enabled() is True


def test_is_voice_enabled_0(monkeypatch):
    monkeypatch.setenv("SMARTASSIST_VOICE", "0")
    assert config.is_voice_enabled() is False


def test_is_voice_enabled_false(monkeypatch):
    monkeypatch.setenv("SMARTASSIST_VOICE", "false")
    assert config.is_voice_enabled() is False


def test_ear_constants_positive():
    assert config.EAR_THRESHOLD > 0
    assert config.BLINK_COOLDOWN > 0
    assert config.DOUBLE_BLINK_MAX_INTERVAL > 0


def test_eye_indices_length():
    assert len(config.LEFT_EYE_INDICES) == 6
    assert len(config.RIGHT_EYE_INDICES) == 6
