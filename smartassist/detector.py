"""Face landmark detection and Eye Aspect Ratio (EAR) helpers."""
import os
import sys
import urllib.request

import numpy as np

from smartassist import config


def ensure_model() -> None:
    """Download the Face Landmarker model if not present."""
    if os.path.isfile(config.MODEL_PATH):
        return
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    print("Downloading Face Landmarker model (one-time, requires internet)...")
    try:
        urllib.request.urlretrieve(config.MODEL_URL, config.MODEL_PATH)
        print("Download complete.")
    except OSError as e:
        print(f"Could not download model: {e}")
        print("See README for manual download. Then run again.")
        sys.exit(1)


def create_face_landmarker():
    """Create and return a MediaPipe FaceLandmarker instance."""
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core import base_options as mp_base_options

    ensure_model()
    options = vision.FaceLandmarkerOptions(
        base_options=mp_base_options.BaseOptions(model_asset_path=config.MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    return vision.FaceLandmarker.create_from_options(options)


def euclidean_distance(p1, p2) -> float:
    """Distance between two points with .x and .y attributes."""
    return float(np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2))


def eye_aspect_ratio(landmarks, eye_indices: list) -> float:
    """Compute Eye Aspect Ratio for blink detection."""
    a = euclidean_distance(landmarks[eye_indices[1]], landmarks[eye_indices[5]])
    b = euclidean_distance(landmarks[eye_indices[2]], landmarks[eye_indices[4]])
    c = euclidean_distance(landmarks[eye_indices[0]], landmarks[eye_indices[3]])
    return (a + b) / (2.0 * c) if c else 0.0
