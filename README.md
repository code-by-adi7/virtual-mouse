# 🖱️ Virtual Mouse — AI-Powered Hand Gesture Controller

> Control your computer mouse entirely with your hand gestures using a webcam — no physical mouse needed.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-orange)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9%2B-purple)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Gesture Controls Reference](#-gesture-controls-reference)
- [Tech Stack](#-tech-stack)
- [System Requirements](#-system-requirements)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [How It Works — Workflow](#-how-it-works--workflow)
- [Configuration & Sensitivity Tuning](#-configuration--sensitivity-tuning)
- [Troubleshooting](#-troubleshooting)
- [Contributors](#-contributors)

---

##  Overview

**Virtual Mouse** is a Python-based computer vision project that replaces the physical mouse with real-time hand gesture recognition. It uses your webcam to track your hand through **MediaPipe's 21-point hand landmark model**, interprets finger positions and distances to detect gestures, then maps those gestures to system-level mouse and keyboard actions via **PyAutoGUI**.

The system supports:
- Smooth cursor movement with two speed modes (normal and sniper/precision)
- Left click, drag-and-drop
- Scrolling (up and down)
- Right click
- System volume control
- Pause/Resume toggle

All gesture recognition runs locally in real time with no internet connection required.

---

## Features

| Feature | Description |
|---|---|
|  **Cursor Movement** | Move the mouse cursor by pointing your index finger |
|  **Sniper Mode** | Slow, precise cursor movement when index finger is close to thumb |
|  **Left Click** | Pinch index finger and thumb together and release |
|  **Drag & Drop** | Hold the pinch for 0.8 seconds to initiate drag; release to drop |
|  **Scroll** | Raise index + middle fingers; move hand up/down to scroll |
|  **Right Click** | Touch thumb tip to pinky tip |
|  **Volume Control** | Raise all four fingers; tilt wrist left/right to adjust volume |
|  **Pause / Resume** | Press `P` on keyboard to freeze/unfreeze gesture detection |
|  **Quit** | Press `Q` on keyboard to exit the program |

---

##  Gesture Controls Reference

This is the complete guide to every gesture the system recognizes. All gestures are performed with one hand in front of the webcam, inside the yellow bounding box visible on screen.

---

### 1.  Move Cursor
**How to do it:** Raise only your **index finger** (middle, ring, pinky folded down). Keep your thumb away from the index finger.

**What happens:** The cursor moves relative to where your index fingertip is within the detection zone (yellow box). The movement is smoothed so small jitters don't cause twitchy movement.

```
Hand shape:
  Index  ↑
  Middle ↓
  Ring   ↓
  Pinky  ↓
  Thumb  ← (away from index)
```

---

### 2. Sniper / Precision Mode
**How to do it:** Same as Move Cursor, but bring your **thumb close to your index finger** (within ~65 pixels on screen) without fully pinching.

**What happens:** Cursor movement slows down dramatically for pixel-precise positioning. A **yellow circle** appears on your fingertip to indicate Sniper Mode is active. Normal mode shows a **purple circle**.

---

### 3.  Left Click
**How to do it:** Raise your index finger, then quickly **pinch it to your thumb** and **release** (open the pinch).

**What happens:**
- As you pinch, a green line appears between fingertip and thumb.
- When you release (fingers separate beyond 35px), a left click fires at the current cursor position.

```
Pinch in  → green line shown, system waits
Release   → left click fires
```

---

### 4.  Drag & Drop
**How to do it:** Same as Left Click, but **hold the pinch for more than 0.8 seconds** before releasing.

**What happens:**
- Screen shows `"LOCKED"` while the hold timer counts down.
- After 0.8 seconds, screen shows `"DRAGGING"` and `mouseDown` fires — the cursor now drags whatever is under it.
- Move your hand while still pinched to drag the item across the screen.
- Release the pinch → `mouseUp` fires and the item is dropped.

```
Pinch → hold 0.8s → DRAG starts → move hand → release → DROP
```

---

### 5.  Scroll Up / Down
**How to do it:** Raise both your **index and middle fingers** together (all other fingers folded).

**What happens:**
- Hand in the **upper half** of the camera frame → scrolls **up**.
- Hand in the **lower half** of the camera frame → scrolls **down**.
- Screen shows `"SCROLL UP"` or `"SCROLL DOWN"` as feedback.

```
Two fingers up:
  Index  ↑
  Middle ↑
  Ring   ↓
  Pinky  ↓

Hand position:
  Upper half of frame → scroll up ↑
  Lower half of frame → scroll down ↓
```

---

### 6.  Right Click
**How to do it:** Touch your **thumb tip to your pinky tip** (bring them close together, within 20px on screen).

**What happens:** A right-click fires at the current cursor position. A 0.5-second cooldown prevents multiple accidental right-clicks. A red circle appears on the pinky tip as visual feedback.

---

### 7. 🔊 Volume Up / Down
**How to do it:** Raise **all four fingers** (index, middle, ring, pinky) with your thumb tucked in, then **tilt your wrist**.

**What happens:**
- Wrist tilted so the angle between wrist and middle knuckle is **< 50°** → presses `Volume Up`.
- Wrist tilted so the angle is **> 130°** → presses `Volume Down`.
- A 0.25-second cooldown prevents rapid-fire key presses.

---

### 8.  Pause / Resume
**How to do it:** Press the **`P` key** on your physical keyboard.

**What happens:** The system freezes all gesture detection. The webcam feed still shows but displays `"SYSTEM PAUSED"` in red. Press `P` again to resume.

---

### 9.  Quit
**How to do it:** Press the **`Q` key** on your physical keyboard.

**What happens:** The webcam feed closes and the program exits cleanly.

---

##  Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| **Python** | 3.8+ | Core runtime language |
| **OpenCV** (`cv2`) | 4.x | Webcam capture, image rendering, FPS display |
| **MediaPipe** | 0.10+ | Real-time 21-point hand landmark detection |
| **PyAutoGUI** | 0.9+ | Controlling system mouse, keyboard, and scroll |
| **NumPy** | 1.x | Coordinate interpolation (mapping webcam frame to screen) |
| **math** | built-in | Distance calculations (Euclidean), angle detection |
| **time** | built-in | Drag hold timer, cooldown timers |

### Why these libraries?

- **MediaPipe** is chosen because it provides fast, accurate hand landmark detection in real time without needing GPU hardware. Its pre-trained model detects 21 landmarks per hand at 30+ FPS on a standard laptop webcam.
- **PyAutoGUI** is cross-platform (Windows, macOS, Linux) and provides direct OS-level mouse and keyboard control without requiring elevated permissions.
- **OpenCV** handles the low-level webcam frame reading and also renders the live debug overlay (bounding box, fingertip circles, status text, FPS counter).

---

##  System Requirements

### Hardware
- A working **webcam** (built-in laptop camera or USB webcam — minimum 480p, 30 FPS recommended)
- A **CPU** capable of real-time inference (most modern laptops/desktops work fine; no GPU required)

### Software
- **Python 3.8 or higher** (Python 3.10/3.11 recommended)
- **pip** (Python package manager, included with Python)
- **Operating System:** Windows 10/11, macOS 10.14+, or Ubuntu 20.04+

### Permissions
- The webcam must be accessible (not blocked by OS privacy settings)
- PyAutoGUI requires permission to control the mouse/keyboard (may need Accessibility permissions on macOS)

---

## Installation & Setup

Follow every step below exactly. Do not skip any step.

---

### Step 1 — Clone the Repository

Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run:

```bash
git clone https://github.com/code-by-adi7/virtual-mouse.git
```

Then navigate into the project folder:

```bash
cd virtual-mouse
```

---

### Step 2 — Verify Python is Installed

Run this command to check your Python version:

```bash
python --version
```

**Expected output (example):**
```
Python 3.11.4
```

If you see `Python 2.x` or get an error, install Python 3.8+ from [https://www.python.org/downloads/](https://www.python.org/downloads/).

> **Windows users:** During Python installation, check the box that says **"Add Python to PATH"** before clicking Install.

---

### Step 3 — (Recommended) Create a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your system Python.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

After activation, your terminal prompt will show `(venv)` at the beginning.

---

### Step 4 — Install All Dependencies

With the virtual environment active, install all required packages:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

This installs:
- `opencv-python` — OpenCV for webcam and image processing
- `mediapipe` — Google's hand landmark detection
- `pyautogui` — mouse/keyboard automation
- `numpy` — numerical array operations

**Wait for all packages to finish downloading and installing.** This may take 1–3 minutes depending on your internet speed.

**Verify installation** by running:

```bash
pip list
```

You should see `opencv-python`, `mediapipe`, `pyautogui`, and `numpy` listed with their versions.

---

### Step 5 — (macOS only) Grant Accessibility Permissions

PyAutoGUI needs permission to control your mouse and keyboard on macOS.

1. Open **System Preferences → Privacy & Security → Accessibility**
2. Click the **lock icon** at the bottom and enter your password
3. Click the **`+`** button and add your **Terminal** app (or whichever terminal you use: iTerm2, VS Code, etc.)
4. Make sure the checkbox next to it is **checked**

If you skip this step, the mouse will not move when you run the program.

---

### Step 6 — (macOS only) Grant Camera Permissions

When you run the program for the first time, macOS may prompt for webcam access. Click **Allow**. If you accidentally clicked Deny:

1. Open **System Preferences → Privacy & Security → Camera**
2. Enable access for your terminal application

---

## ▶️ How to Run

Make sure your virtual environment is active (you see `(venv)` in the terminal). Then run:

```bash
python prjfnl.py
```

**What you will see:**

1. The terminal prints:
   ```
   System Ready. Press 'P' to PAUSE/RESUME.
   ```

2. A window titled **"AI Mouse by Adi,mithun and saabi"** opens showing your webcam feed in real time.

3. A **yellow rectangle** appears in the center of the frame — this is the **detection zone**. Move your hand inside this box to control the cursor.

4. The **FPS counter** appears in the top-left corner of the window.

5. Raise your index finger inside the yellow box — the cursor should start moving.

**To stop the program:** Press the `Q` key while the webcam window is focused, or press `Ctrl+C` in the terminal.

---

## ⚙️ How It Works — Workflow

Below is the complete step-by-step flow of what happens every frame:

```
┌─────────────────────────────────────────────────────┐
│                  PROGRAM STARTS                     │
│  • Webcam opens at 640×480                          │
│  • MediaPipe Hands model initializes                │
│  • Screen resolution fetched via PyAutoGUI          │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              MAIN LOOP (every frame)                │
│                                                     │
│  1. Read frame from webcam                          │
│  2. Flip frame horizontally (mirror view)           │
│  3. Check if system is PAUSED                       │
│     → If paused: show "SYSTEM PAUSED" text, skip   │
│     → If not paused: continue below                 │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           HAND DETECTION (MediaPipe)                │
│                                                     │
│  4. Convert frame BGR → RGB                         │
│  5. Pass frame to MediaPipe Hands.process()         │
│  6. MediaPipe returns 21 landmarks per hand         │
│     (pixel coordinates for each joint)              │
│  7. Draw skeleton overlay on the frame              │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          LANDMARK EXTRACTION                        │
│                                                     │
│  8. Extract key landmark positions:                 │
│     • Landmark  4 = Thumb tip                       │
│     • Landmark  8 = Index fingertip                 │
│     • Landmark 20 = Pinky tip                       │
│  9. Detect which fingers are raised (0 or 1)        │
│     by comparing Y-coordinates of tip vs DIP joint  │
│ 10. Calculate Euclidean distances:                  │
│     • dist_index = distance(thumb, index tip)       │
│     • dist_pinky = distance(thumb, pinky tip)       │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          GESTURE DECISION TREE                      │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ IF index up AND middle down:                 │   │
│  │   → MOVE / CLICK / DRAG mode                 │   │
│  │                                              │   │
│  │   IF dist_index < 20 (pinched):              │   │
│  │     Start pinch timer                        │   │
│  │     IF held > 0.8s → DRAG (mouseDown)        │   │
│  │     ELSE → wait for release                  │   │
│  │                                              │   │
│  │   IF dist_index > 35 (released):             │   │
│  │     IF was dragging → mouseUp (drop)         │   │
│  │     ELSE → left click                        │   │
│  │                                              │   │
│  │   IF not pinching:                           │   │
│  │     IF dist_index < 65 → SNIPER MOVE (slow) │   │
│  │     ELSE → NORMAL MOVE (fast)               │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ IF index AND middle both up:                 │   │
│  │   → SCROLL mode                              │   │
│  │   IF index Y < (frame height/2 - 50) → up   │   │
│  │   IF index Y > (frame height/2 + 50) → down │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ IF dist_pinky < 20 (thumb meets pinky):      │   │
│  │   → RIGHT CLICK (with 0.5s cooldown)         │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ IF all 4 fingers up (index,mid,ring,pinky):  │   │
│  │   → VOLUME CONTROL mode                      │   │
│  │   Calculate wrist tilt angle                 │   │
│  │   angle < 50  → Volume Up key               │   │
│  │   angle > 130 → Volume Down key             │   │
│  └──────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          COORDINATE MAPPING & SMOOTHING             │
│                                                     │
│ 11. Map index finger position from webcam space     │
│     to full screen space using np.interp():         │
│     webcam zone (frameR_X → wCam-frameR_X)          │
│     maps to screen (0 → screen width)               │
│                                                     │
│ 12. Apply smoothing to avoid jitter:                │
│     newPos = prevPos + (targetPos - prevPos) / k    │
│     k=3  → fast, responsive movement                │
│     k=30 → slow, precise movement (sniper mode)     │
│                                                     │
│ 13. Call pyautogui.moveTo(x, y) to move cursor      │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│          RENDER & KEY HANDLING                      │
│                                                     │
│ 14. Draw FPS counter on frame                       │
│ 15. Display frame in OpenCV window                  │
│ 16. Read keyboard input:                            │
│     Q → break loop, exit                            │
│     P → toggle pause state                          │
│ 17. Loop back to Step 1                             │
└─────────────────────────────────────────────────────┘
```

---

## 🎚️ Configuration & Sensitivity Tuning

All tunable settings are defined as constants at the top of `prjfnl.py`. You can edit these to customize the feel:

```python
wCam, hCam = 640, 480       # Webcam resolution (width × height)
frameR_X = 200              # Detection zone horizontal margin (pixels)
frameR_Y = 150              # Detection zone vertical margin (pixels)

smooth_fast = 3             # Cursor smoothing in normal mode (lower = more responsive)
smooth_slow = 30            # Cursor smoothing in sniper mode (higher = smoother/slower)

sniper_trigger_dist = 65    # Pixel distance that triggers sniper mode
clk_dst = 20                # Pixel distance to register a pinch (click start)
rls_dst = 35                # Pixel distance to register a release (click fire)
drag_delay = 0.8            # Seconds of held pinch before drag starts
scroll_speed = 20           # Number of scroll units per gesture event
```

### Tuning Tips

| Problem | Recommended Fix |
|---|---|
| Cursor moves too fast | Increase `smooth_fast` (e.g., `5`) |
| Cursor is too jittery | Increase `smooth_fast` further (e.g., `7`) |
| Cursor too sluggish in normal mode | Decrease `smooth_fast` (e.g., `2`) |
| Clicks fire accidentally | Increase `clk_dst` (e.g., `25`) |
| Drag triggers too quickly | Increase `drag_delay` (e.g., `1.2`) |
| Detection zone too small/large | Decrease/increase `frameR_X` and `frameR_Y` |
| Scroll too fast | Decrease `scroll_speed` (e.g., `10`) |

---

## 🔧 Troubleshooting

###  Webcam window doesn't open / "Error: could not read frame"
- Make sure no other application is using the webcam (Zoom, Teams, etc.)
- Check that your webcam is connected and recognized by the OS
- Try changing the webcam index: in `prjfnl.py`, change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if you have multiple cameras

###  Hand is detected but cursor doesn't move (macOS)
- You haven't granted Accessibility permissions to Terminal. See [Step 5](#step-5--macos-only-grant-accessibility-permissions) above.

###  `ModuleNotFoundError: No module named 'cv2'`
- The virtual environment is not activated, or installation failed.
- Activate the venv and re-run `pip install opencv-python`

###  `ModuleNotFoundError: No module named 'mediapipe'`
- Run: `pip install mediapipe`
- If you get an error about Python version, MediaPipe requires Python 3.8–3.12.

###  Hand not detected / detection is unreliable
- Improve lighting — make sure your hand is well-lit and not backlit
- Use a plain, non-cluttered background
- Keep your hand within the yellow detection rectangle
- Ensure your hand is fully visible and not too far from or too close to the camera

### FPS is very low (< 10 FPS)
- Close other running applications to free CPU resources
- Reduce webcam resolution: change `wCam, hCam = 640, 480` to `wCam, hCam = 320, 240`
- Ensure you're running Python with the virtualenv (system Python can be slower)

###  PyAutoGUI raises `FailSafeException`
- This is disabled in the code (`pyg.FAILSAFE = False`), but if you modify the file, ensure this line is present.

---

## 👨‍💻 Contributors

This project was built by:


| **Adithya** | Core development, gesture engine, MediaPipe integration |


---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <strong>Built using Python, OpenCV, and MediaPipe</strong>
</div>
