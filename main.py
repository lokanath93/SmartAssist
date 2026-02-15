"""
SmartAssist - Head-controlled mouse with blink-to-click and voice typing.
Entry point: run the app (requires webcam; microphone optional).
"""
import sys

from smartassist.app import run

if __name__ == "__main__":
    run()
    sys.exit(0)
