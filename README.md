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

---

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

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

- **First run:** The app will download the Face Landmarker model (~10 MB) once. Keep the internet on.
- A window will open showing your face. Move your head to move the cursor; **double-blink** to click.
- Press **ESC** to exit.

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
| **PyAudio / microphone errors on Linux** | Install portaudio: `sudo apt install portaudio19-dev` (Debian/Ubuntu) then `pip install pyaudio`. |

## Requirements (from requirements.txt)

- **opencv-python** – camera and display
- **mediapipe** – face landmark detection (0.10+)
- **pyautogui** – mouse movement and typing
- **SpeechRecognition** – voice recognition
- **pyaudio** – microphone (optional if voice disabled)
- **numpy** – numerical operations

## Pushing to GitHub (for maintainers)

If you have a local copy and want to push to [github.com/lokanath93](https://github.com/lokanath93):

1. **Create the repo on GitHub** (one-time)  
   - Go to [https://github.com/new](https://github.com/new)  
   - Repository name: `SmartAssist`  
   - Do **not** add a README, .gitignore, or license (they already exist locally)  
   - Click **Create repository**

2. **Commit and push from your machine** (in a terminal, from the project folder):

   ```bash
   cd /path/to/SmartAssist

   git add .gitignore README.md requirements.txt main.py push_to_github.sh
   git commit -m "Initial commit: SmartAssist head mouse blink click voice typing"

   git remote add origin https://github.com/lokanath93/SmartAssist.git
   git branch -M main
   git push -u origin main
   ```

   Or run the script (macOS/Linux): `./push_to_github.sh`

   Use your GitHub username and a [personal access token](https://github.com/settings/tokens) (or SSH key) when prompted for password.

## License

Use and modify as you like. MediaPipe models are subject to [Google’s terms](https://ai.google.dev/terms).
