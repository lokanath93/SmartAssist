# SmartAssist

Head-controlled mouse with **blink-to-click** and **voice typing**. Use your face to move the cursor and double-blink to click. Say *"type hello world"* to type text. Works on **Windows, macOS, and Linux** on any laptop with a webcam.

## Features

- **Head tracking** – Move the mouse by moving your head (nose direction).
- **Double-blink to click** – Two quick blinks trigger a left click.
- **Voice typing** – Say *"type &lt;text&gt;"* to type that text (e.g. *"type Hello world"*).

## Prerequisites

- **Python 3.9+** (3.10 or 3.11 recommended)
- **Webcam** (built-in or USB)
- **Microphone** (optional; required only for voice typing)
- **Internet** (only for first run, to download the face model)

## Repository

- **GitHub:** [https://github.com/lokanath93/SmartAssist](https://github.com/lokanath93/SmartAssist)  
  Clone with: `git clone https://github.com/lokanath93/SmartAssist.git`

## Project structure

```
SmartAssist/
├── main.py                 # Entry point: run the app
├── requirements.txt        # All dependencies (one install for all features)
├── requirements-dev.txt    # Dev dependencies (pytest)
├── README.md
├── smartassist/            # Main package
│   ├── __init__.py
│   ├── config.py           # Paths, env vars, constants
│   ├── detector.py         # Face landmarker model, EAR helpers
│   ├── camera.py           # Camera open, frame read
│   ├── controller.py       # Mouse + blink state (head → cursor, double-blink → click)
│   ├── voice.py            # Voice command thread ("type …")
│   └── app.py              # Main loop: capture, detect, control, display
├── tests/
│   ├── conftest.py         # Pytest fixtures (mock landmarks)
│   ├── test_config.py
│   ├── test_detector.py
│   ├── test_controller.py
│   ├── test_voice.py
│   └── test_camera.py
└── models/                 # Face Landmarker model (downloaded on first run)
```

## Quick start (any laptop)

### 1. Clone or download the project

```bash
git clone https://github.com/lokanath93/SmartAssist.git
cd SmartAssist
```

Or download and extract the project folder.

### 2. Create a virtual environment (recommended)

**Windows (Command Prompt or PowerShell):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies (one command for all features)

```bash
pip install -r requirements.txt
```

**If PyAudio fails on macOS** (e.g. “failed to build wheel for pyaudio”): install PortAudio first, then run the same command again:

```bash
brew install portaudio
pip install -r requirements.txt
```

**On Linux** (Debian/Ubuntu), if PyAudio fails: `sudo apt install portaudio19-dev` then `pip install -r requirements.txt` again.

### 4. Run the app

```bash
python main.py
```

- **First run:** The app will download the Face Landmarker model (~10 MB) once. Keep the internet on.
- A window will open showing your face. Move your head to move the cursor; **double-blink** to click.
- Press **ESC** to exit.

### 5. Run tests (optional)

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Tests cover config, detector (EAR math), controller (mouse/clamp/blink), voice command parsing, and camera helpers. No webcam or microphone is required to run tests.

## Usage

| Action            | How to do it                    |
|-------------------|---------------------------------|
| Move cursor       | Move your head (nose direction)|
| Click             | Double-blink quickly            |
| Type with voice   | Say *"type &lt;your text&gt;"*  |
| Quit              | Press **ESC**                   |

- Face the webcam in good light for best tracking.
- For voice: speak clearly; Google Speech is used (internet needed for voice).

## Configuration (optional)

You can set these **environment variables** before running:

| Variable               | Default | Description |
|------------------------|---------|-------------|
| `SMARTASSIST_CAMERA`   | `0`     | Camera index (0 = default webcam). Use `1` or `2` if the wrong camera opens. |
| `SMARTASSIST_VOICE`    | `1`     | Set to `0` to disable voice commands (e.g. if you have no microphone). |

**Examples:**

**Windows (Command Prompt):**
```cmd
set SMARTASSIST_CAMERA=1
python main.py
```

**Windows (PowerShell):**
```powershell
$env:SMARTASSIST_CAMERA=1; python main.py
```

**macOS / Linux:**
```bash
SMARTASSIST_CAMERA=1 python main.py
# or
export SMARTASSIST_VOICE=0
python main.py
```

## Manual model download (offline / restricted network)

If the app cannot download the model (e.g. no internet or firewall), download it manually:

1. Get the model file:  
   [face_landmarker.task](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task)

2. Create a `models` folder inside the SmartAssist project and save the file as:
   ```
   SmartAssist/models/face_landmarker.task
   ```

3. Run `python main.py` again. The app will use this file and will not try to download.

## Troubleshooting

| Problem | What to try |
|--------|--------------|
| **"No camera found"** | Connect a webcam, close other apps using the camera, or try `SMARTASSIST_CAMERA=1` (or `2`). |
| **"Could not download model"** | Check internet; or use [manual model download](#manual-model-download-offline--restricted-network) and run again. |
| **Cursor doesn’t move** | Ensure your face is clearly visible and well lit; look at the camera. |
| **Double-blink not clicking** | Blink twice quickly (within about 0.5 s). Adjust distance from the camera if needed. |
| **Voice not working** | Check microphone permissions and that you’re online (Google Speech). Disable with `SMARTASSIST_VOICE=0` if you don’t need it. |
| **Wrong camera opens** | Set `SMARTASSIST_CAMERA=1` (or another index) before running. |
| **PyAudio / microphone errors on Linux** | `sudo apt install portaudio19-dev` (Debian/Ubuntu), then `pip install -r requirements.txt` again. |
| **Failed to build wheel for pyaudio (macOS)** | Run `brew install portaudio`, then `pip install -r requirements.txt` again. |

## Requirements (all in requirements.txt)

opencv-python, mediapipe, numpy, pyautogui, SpeechRecognition, pyaudio — one install for head tracking, blink-to-click, and voice typing.

## License

Use and modify as you like. MediaPipe models are subject to [Google’s terms](https://ai.google.dev/terms).
