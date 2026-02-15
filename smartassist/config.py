"""Configuration: paths, environment, and constants."""
import os

# Paths (cross-platform): project root = parent of smartassist package
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(SCRIPT_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "face_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

# Environment
def get_camera_index() -> int:
    return int(os.environ.get("SMARTASSIST_CAMERA", "0"))


def is_voice_enabled() -> bool:
    val = os.environ.get("SMARTASSIST_VOICE", "1").strip().lower()
    return val not in ("0", "false", "no")


# Blink / mouse
SMOOTHING_FACTOR = 0.2
EAR_THRESHOLD = 0.25
BLINK_COOLDOWN = 0.2
DOUBLE_BLINK_MAX_INTERVAL = 0.5

# Eye landmark indices (MediaPipe Face Landmarker 478 points)
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
NOSE_TIP_INDEX = 4

# Frame timing (~30 fps)
FRAME_DT_MS = 33
