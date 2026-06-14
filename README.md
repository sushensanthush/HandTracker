# Webcam Hand Tracking App
<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?style=for-the-badge)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-red?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-Personal%20Use%20Only-black?style=for-the-badge)


A real-time hand tracking application built with Python, OpenCV, MediaPipe, and Tkinter.

This project detects and tracks hands through a webcam feed, visualizes finger landmarks, identifies left and right hands, and includes an optional Mystic Mode that generates animated sacred geometry mandalas centered on the palm.

---

## Features

- Real-time hand tracking
- Multi-hand detection (up to 4 hands)
- Finger landmark visualization
- Finger labeling
- Left and right hand identification
- Dynamic landmark scaling
- Mystic Mode with animated Tao Mandala rendering
- Responsive Tkinter graphical interface
- Cross-platform compatibility

---

## Technologies

- Python 3
- OpenCV
- MediaPipe Tasks API
- NumPy
- Pillow (PIL)
- Tkinter

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/sushensanthush/webcam-hand-tracking-app.git
cd webcam-hand-tracking-app
```

### Install Dependencies

```bash
pip install opencv-python mediapipe pillow numpy
```

### Download the Required Model

Place the following file in the project directory:

```text
hand_landmarker.task
```

---

## Project Structure

```text
webcam-hand-tracking-app/
│
├── main.py
├── hand_landmarker.task
├── README.md
└── screenshots/
```

---

## Usage

Run the application using:

```bash
python main.py
```

---

## Controls

| Control | Description |
|----------|-------------|
| Enable Hand Tracking | Enable or disable hand tracking |
| Mystic Mode | Enable sacred geometry visual effects |
| Exit | Close the application |

---

## Mystic Mode

Mystic Mode generates animated sacred geometry patterns around the detected palm in real time.

Features include:

- Rotating circular structures
- Dynamic geometric formations
- Animated glyph rings
- Particle effects
- Real-time scaling based on hand position and finger spread

---

## Screenshots

### Standard Tracking Mode

Add a screenshot here:

```text
screenshots/standard-mode.png
```

### Mystic Mode

Add a screenshot here:

```text
screenshots/mystic-mode.png
```

---

## Requirements

- Python 3.9 or later
- Webcam
- Windows, Linux, or macOS

---

## License

### Personal Use Only

Copyright © 2026 Sushen Santhush

This software is provided for personal and non-commercial use only.

Permission is granted to use and modify this software for personal purposes.

The following actions are prohibited without prior written permission from the author:

- Commercial use
- Redistribution
- Selling or sublicensing
- Inclusion in commercial products or services

This software is provided "as is" without warranty of any kind.

All rights reserved.

---

## Author

**Sushen Santhush**

GitHub: https://github.com/sushensanthush
