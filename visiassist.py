import cv2
import torch
import easyocr
import datetime
import speech_recognition as sr
import time
from gtts import gTTS
import os
import sys
from ultralytics import YOLO

# Default language
current_lang = 'en'

# Language map
lang_map = {
    'english': 'en',
    'spanish': 'es',
    'hindi': 'hi',
    'french': 'fr'
}

# Initialize YOLO and speech recognizer
model = YOLO('yolov8n.pt')
recognizer = sr.Recognizer()

# Cache for EasyOCR readers
ocr_readers = {}

def get_reader(lang_code):
    if lang_code not in ocr_readers:
        print(f"🔤 Initializing OCR for: {lang_code}")
        ocr_readers[lang_code] = easyocr.Reader([lang_code])
    return ocr_readers[lang_code]

# Logging
def log_event(objects, text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        if objects:
            f.write(f"[{timestamp}] Objects: {', '.join(objects)}\n")
        if text:
            f.write(f"[{timestamp}] Text: {text}\n")

# TTS using gTTS
def speak(text, lang_code):
    if not text:
        return
    tts = gTTS(text=text, lang=lang_code)
    tts.save("temp.mp3")
    os.system("afplay temp.mp3")  # macOS only — for Windows use playsound instead

# Detect and announce
def detect_and_announce():
    global current_lang
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("❌ Camera failed.")
        return

    # Show frame
    cv2.imshow("Camera", frame)
    cv2.waitKey(1)

    # Object detection
    results = model(frame)
    labels = results[0].names
    detected = [labels[int(c)] for c in results[0].boxes.cls]

    # OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    reader = get_reader(current_lang)
    text = ' '.join([t[1] for t in reader.readtext(gray)])

    # Message to speak
    message = ""
    if detected:
        message += "I see: " + ', '.join(detected) + ". "
    if text:
        message += "I read: " + text

    print("🔊", message if message else "Nothing detected.")
    speak(message if message else "Nothing detected", current_lang)
    log_event(detected, text)

    cv2.waitKey(1000)
    cap.release()
    cv2.destroyAllWindows()

# Voice command listening
def listen_for_voice():
    global current_lang
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ You said: {command}")

            if "what is this" in command:
                detect_and_announce()
            elif "exit" in command:
                speak("Goodbye", current_lang)
                cv2.destroyAllWindows()
                sys.exit()
            elif "switch to" in command:
                for name in lang_map:
                    if name in command:
                        current_lang = lang_map[name]
                        speak(f"Language switched to {name}", current_lang)
                        print(f"🌐 Language changed to: {current_lang}")
                        return
                speak("Language not recognized", current_lang)
    except sr.UnknownValueError:
        print("❌ Could not understand.")
    except sr.WaitTimeoutError:
        pass
    except sr.RequestError:
        print("⚠️ Speech recognition error.")

# Keyboard fallback
def listen_for_keys_cv():
    key = cv2.waitKey(1) & 0xFF
    if key == ord('d'):
        detect_and_announce()
    elif key == ord('q'):
        speak("Goodbye", current_lang)
        cv2.destroyAllWindows()
        sys.exit()

# Main loop
if __name__ == "__main__":
    print("🟢 Running. Say 'what is this' or 'switch to Hindi/Spanish/etc'. Press 'd' to detect or 'q' to quit.")
    while True:
        listen_for_voice()
        listen_for_keys_cv()
        time.sleep(0.1)

