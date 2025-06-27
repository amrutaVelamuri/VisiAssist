# VisiAssist

VisiAssist is a multilingual AI-powered vision assistant designed for visually impaired users. It provides real-time object detection, optical character recognition (OCR), and speech feedback in multiple languages. The application uses PyTorch, YOLOv8, EasyOCR, and voice recognition to enable hands-free interaction and accessibility.

## Features

- Real-time object detection using YOLOv8
- Text reading from the environment using EasyOCR
- Voice-activated interaction
- Multilingual support (English, Spanish, Hindi, French)
- Keyboard fallback: press `d` to detect, `q` to quit
- Automatic event logging with timestamps

## Quickstart

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/VisiAssist.git
cd VisiAssist
pip install -r requirements.txt
python visiassist.py
