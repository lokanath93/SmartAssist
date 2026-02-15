"""Camera open and frame reading."""
import sys

import cv2

from smartassist import config


def open_camera(camera_index: int = None):
    """Open first available camera. Tries camera_index, then 0, then 1."""
    idx = camera_index if camera_index is not None else config.get_camera_index()
    cap = None
    tried = set()
    for i in [idx, 0, 1]:
        if i in tried:
            continue
        tried.add(i)
        if cap is not None:
            cap.release()
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            if i != idx:
                print(f"Using camera index {i}.")
            return cap
    if cap is not None:
        cap.release()
    print("Error: No camera found. Connect a webcam and try again.")
    sys.exit(1)


def read_frame_rgb(cap):
    """Read one frame; return (success, rgb_image). Image is flipped for selfie view."""
    success, image = cap.read()
    if not success:
        return False, None
    rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    return True, rgb
