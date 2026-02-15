"""Voice command thread: listen for 'type <text>' and type via pyautogui."""
import threading
from typing import Optional

import pyautogui
import speech_recognition as sr


def parse_type_command(command: str) -> Optional[str]:
    """If command contains 'type', return the phrase to type; else None."""
    if "type" not in command:
        return None
    phrase = command.split("type", 1)[1].strip()
    return phrase if phrase else None


def _listen_loop():
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
                phrase = parse_type_command(command)
                if phrase:
                    pyautogui.write(phrase)
                    print(f"Typed: {phrase}")
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(f"Speech API error: {e}")
            except Exception as e:
                print(f"Voice error: {e}")


def start_voice_thread(enabled: bool = True) -> None:
    """Start the voice command listener in a daemon thread if enabled."""
    if not enabled:
        print("Voice commands disabled (SMARTASSIST_VOICE=0).")
        return
    t = threading.Thread(target=_listen_loop, daemon=True)
    t.start()
