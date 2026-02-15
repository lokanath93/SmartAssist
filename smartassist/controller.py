"""Mouse and blink state: head tracking and double-blink click."""
import time
from typing import List, Tuple

import pyautogui

from smartassist import config
from smartassist.detector import eye_aspect_ratio


class MouseController:
    """Tracks mouse position from head and triggers click on double-blink."""

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = self.screen_width // 2
        self.prev_y = self.screen_height // 2
        self.blink_count = 0
        self.last_blink_time = 0.0
        self.last_click_time = 0.0
        pyautogui.FAILSAFE = True

    def clamp_to_screen(self, x: int, y: int) -> Tuple[int, int]:
        """Clamp coordinates to screen bounds."""
        x = max(0, min(self.screen_width - 1, x))
        y = max(0, min(self.screen_height - 1, y))
        return x, y

    def landmarks_to_mouse(self, nose_tip) -> Tuple[int, int]:
        """Convert nose landmark (0–1) to smoothed screen coordinates."""
        x = int(nose_tip.x * self.screen_width)
        y = int(nose_tip.y * self.screen_height)
        x, y = self.clamp_to_screen(x, y)
        smooth_x = int(self.prev_x + (x - self.prev_x) * config.SMOOTHING_FACTOR)
        smooth_y = int(self.prev_y + (y - self.prev_y) * config.SMOOTHING_FACTOR)
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y

    def update(self, landmark_list: List) -> bool:
        """
        Update mouse from face landmarks. Move cursor; maybe trigger click on double-blink.
        Returns True if a click was triggered.
        """
        nose_tip = landmark_list[config.NOSE_TIP_INDEX]
        x, y = self.landmarks_to_mouse(nose_tip)
        pyautogui.moveTo(x, y)

        left_ear = eye_aspect_ratio(landmark_list, config.LEFT_EYE_INDICES)
        right_ear = eye_aspect_ratio(landmark_list, config.RIGHT_EYE_INDICES)
        avg_ear = (left_ear + right_ear) / 2
        now = time.time()

        clicked = False
        if avg_ear < config.EAR_THRESHOLD and (now - self.last_blink_time) > config.BLINK_COOLDOWN:
            self.blink_count += 1
            self.last_blink_time = now
            if self.blink_count == 1:
                self.last_click_time = now
            elif self.blink_count == 2 and (now - self.last_click_time) < config.DOUBLE_BLINK_MAX_INTERVAL:
                pyautogui.click()
                clicked = True
                self.blink_count = 0
            elif self.blink_count == 2 and (now - self.last_click_time) >= config.DOUBLE_BLINK_MAX_INTERVAL:
                self.blink_count = 1
                self.last_click_time = now
        elif (
            avg_ear >= config.EAR_THRESHOLD
            and (now - self.last_blink_time) > config.BLINK_COOLDOWN
            and self.blink_count == 1
            and (now - self.last_click_time) >= config.DOUBLE_BLINK_MAX_INTERVAL
        ):
            self.blink_count = 0
        return clicked
