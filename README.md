# VisiAssist

VisiAssist is a multilingual AI-powered vision assistant designed to help visually impaired users by providing real-time object detection, text reading, and speech feedback in multiple languages. It leverages PyTorch, YOLOv8, EasyOCR, and speech recognition to enable hands-free interaction and accessibility.

---

## Features

- Real-time object detection with YOLOv8  
- Text recognition (OCR) from surroundings using EasyOCR  
- Voice command control for hands-free use  
- Supports multiple languages: English, Spanish, Hindi, French  
- Keyboard fallback: press `d` to detect objects/text, `q` to quit app  
- Logs all detections and readings with timestamps for review  

---

## Getting Started

### Prerequisites

- Python 3.8 or higher  
- A webcam or camera connected to your computer  
- Internet connection (for speech recognition and text-to-speech)  
- MacOS, Windows, or Linux environment  

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/VisiAssist.git
cd VisiAssist
