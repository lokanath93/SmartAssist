"""
SmartAssist - Head-controlled mouse with blink-to-click and voice typing.
Runs on Windows, macOS, and Linux. Requires a webcam; microphone is optional.
"""
import os
import sys
import time
import threading
import urllib.request

import cv2
import numpy as np
import pyautogui
import speech_recognition as sr

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options as mp_base_options
from mediapipe.tasks.python.vision.core.image import Image, ImageFormat

# ---------- Config (works on any laptop) ----------
# Camera index: 0 = default webcam. Use 1, 2, ... if you have multiple cameras.
CAMERA_INDEX = int(os.environ.get("SMARTASSIST_CAMERA", "0"))
# Set to "0" to disable voice commands (e.g. if no microphone).
VOICE_ENABLED = os.environ.get("SMARTASSIST_VOICE", "1").strip().lower() not in ("0", "false", "no")

# Paths (cross-platform: Windows, macOS, Linux)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "face_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

pyautogui.FAILSAFE = True

# Download Face Landmarker model if not present (one-time, requires internet)
if not os.path.isfile(MODEL_PATH):
    os.makedirs(MODEL_DIR, exist_ok=True)
    print("Downloading Face Landmarker model (one-time, requires internet)...")
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Download complete.")
    except OSError as e:
        print(f"Could not download model: {e}")
        print("See README for manual download. Then run again.")
        sys.exit(1)

# Face Landmarker setup (MediaPipe Tasks API)
base_options = vision.FaceLandmarkerOptions(
    base_options=mp_base_options.BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)
face_landmarker = vision.FaceLandmarker.create_from_options(base_options)

# Camera: try configured index first, then 0, then 1 (for different laptops)
cap = None
tried = set()
for idx in [CAMERA_INDEX, 0, 1]:
    if idx in tried:
        continue
    tried.add(idx)
    if cap is not None:
        cap.release()
    cap = cv2.VideoCapture(idx)
    if cap.isOpened():
        if idx != CAMERA_INDEX:
            print(f"Using camera index {idx}.")
        break
if cap is None or not cap.isOpened():
    if cap is not None:
        cap.release()
    print("Error: No camera found. Connect a webcam and try again.")
    sys.exit(1)

screen_width, screen_height = pyautogui.size()

# Mouse smoothing filter
SMOOTHING_FACTOR = 0.2
prev_mouse_x, prev_mouse_y = screen_width // 2, screen_height // 2

# Eye Aspect Ratio (EAR) calculation
def euclidean_distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def eye_aspect_ratio(landmarks, eye_indices):
    A = euclidean_distance(landmarks[eye_indices[1]], landmarks[eye_indices[5]])
    B = euclidean_distance(landmarks[eye_indices[2]], landmarks[eye_indices[4]])
    C = euclidean_distance(landmarks[eye_indices[0]], landmarks[eye_indices[3]])
    ear = (A + B) / (2.0 * C)
    return ear


# Eye landmark indices (MediaPipe Face Landmarker 478 points - same topology as legacy for these)
LEFT_EYE_INDICES = [362, 385, 387, 263, 373, 380]
RIGHT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
EAR_THRESHOLD = 0.25
BLINK_COOLDOWN = 0.2

last_blink_time = 0
blink_count = 0
last_click_time = 0

def listen_for_commands():
    global last_click_time
    try:
        r = sr.Recognizer()
        mic = sr.Microphone()
    except Exception as e:
        print(f"Microphone not available: {e}. Voice commands disabled.")
        return
    with mic as source:
        try:
            r.adjust_for_ambient_noise(source)
        except Exception as e:
            print(f"Could not calibrate microphone: {e}. Voice commands disabled.")
            return
        print("Listening for voice commands (say 'type <text>' to type)...")
        while True:
            try:
                audio = r.listen(source, timeout=5)
                command = r.recognize_google(audio).lower()
                print(f"Heard: {command}")
                if "type" in command:
                    phrase_to_type = command.split("type", 1)[1].strip()
                    if phrase_to_type:
                        pyautogui.write(phrase_to_type)
                        print(f"Typed: {phrase_to_type}")
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Speech API error: {e}")
            except Exception as e:
                print(f"Voice error: {e}")


# Start voice command thread only if enabled and mic available
if VOICE_ENABLED:
    voice_thread = threading.Thread(target=listen_for_commands, daemon=True)
    voice_thread.start()
else:
    print("Voice commands disabled (SMARTASSIST_VOICE=0).")

print("Starting head tracking and blink detection...")

frame_timestamp_ms = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip for selfie view, convert BGR to RGB
    image_rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # MediaPipe Image expects RGB (SRGB format), contiguous array
    mp_image = Image(image_format=ImageFormat.SRGB, data=image_rgb)

    results = face_landmarker.detect_for_video(mp_image, frame_timestamp_ms)
    frame_timestamp_ms += 33  # ~30 fps

    # Draw on BGR for display
    image_draw = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if results.face_landmarks:
        for landmark_list in results.face_landmarks:
            # Head tracking (nose tip = index 4)
            nose_tip = landmark_list[4]
            mouse_x = int(nose_tip.x * screen_width)
            mouse_y = int(nose_tip.y * screen_height)
            mouse_x = max(0, min(screen_width - 1, mouse_x))
            mouse_y = max(0, min(screen_height - 1, mouse_y))

            smooth_mouse_x = int(prev_mouse_x + (mouse_x - prev_mouse_x) * SMOOTHING_FACTOR)
            smooth_mouse_y = int(prev_mouse_y + (mouse_y - prev_mouse_y) * SMOOTHING_FACTOR)

            pyautogui.moveTo(smooth_mouse_x, smooth_mouse_y)
            prev_mouse_x, prev_mouse_y = smooth_mouse_x, smooth_mouse_y

            # Double blink to click
            left_ear = eye_aspect_ratio(landmark_list, LEFT_EYE_INDICES)
            right_ear = eye_aspect_ratio(landmark_list, RIGHT_EYE_INDICES)
            avg_ear = (left_ear + right_ear) / 2

            current_time = time.time()
            if avg_ear < EAR_THRESHOLD and (current_time - last_blink_time) > BLINK_COOLDOWN:
                blink_count += 1
                last_blink_time = current_time
                print(f"Blink detected! Count: {blink_count}")

                if blink_count == 1:
                    last_click_time = current_time
                elif blink_count == 2 and (current_time - last_click_time) < 0.5:
                    pyautogui.click()
                    print("Double blink detected! Clicked.")
                    blink_count = 0
                elif blink_count == 2 and (current_time - last_click_time) >= 0.5:
                    blink_count = 1
                    last_click_time = current_time
            elif (
                avg_ear >= EAR_THRESHOLD
                and (current_time - last_blink_time) > BLINK_COOLDOWN
                and blink_count == 1
                and (current_time - last_click_time) >= 0.5
            ):
                blink_count = 0

            # Draw face contours
            vision.drawing_utils.draw_landmarks(
                image=image_draw,
                landmark_list=landmark_list,
                connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
                landmark_drawing_spec=vision.drawing_utils.DrawingSpec(color=(224, 224, 224), thickness=1, circle_radius=1),
                connection_drawing_spec=vision.drawing_utils.DrawingSpec(color=(224, 224, 224), thickness=1, circle_radius=1),
            )

    cv2.imshow("Head Mouse", image_draw)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
print("Script stopped.")
