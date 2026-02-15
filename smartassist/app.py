"""Main application loop: camera, face detection, mouse control, display."""
import sys

import cv2

from smartassist import config
from smartassist.camera import open_camera, read_frame_rgb
from smartassist.controller import MouseController
from smartassist.detector import create_face_landmarker
from smartassist.voice import start_voice_thread


def run():
    """Run the SmartAssist app until ESC."""
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.vision.core.image import Image, ImageFormat

    landmarker = create_face_landmarker()
    cap = open_camera()
    controller = MouseController()
    start_voice_thread(config.is_voice_enabled())

    frame_ts_ms = 0
    print("Starting head tracking and blink detection...")

    try:
        while cap.isOpened():
            success, image_rgb = read_frame_rgb(cap)
            if not success:
                print("Ignoring empty camera frame.")
                continue

            mp_image = Image(image_format=ImageFormat.SRGB, data=image_rgb)
            results = landmarker.detect_for_video(mp_image, frame_ts_ms)
            frame_ts_ms += config.FRAME_DT_MS

            image_draw = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            if results.face_landmarks:
                for landmark_list in results.face_landmarks:
                    controller.update(landmark_list)
                    vision.drawing_utils.draw_landmarks(
                        image=image_draw,
                        landmark_list=landmark_list,
                        connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
                        landmark_drawing_spec=vision.drawing_utils.DrawingSpec(
                            color=(224, 224, 224), thickness=1, circle_radius=1
                        ),
                        connection_drawing_spec=vision.drawing_utils.DrawingSpec(
                            color=(224, 224, 224), thickness=1, circle_radius=1
                        ),
                    )

            cv2.imshow("Head Mouse", image_draw)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    print("Script stopped.")


if __name__ == "__main__":
    run()
    sys.exit(0)
