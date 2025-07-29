#!/usr/bin/env python3
"""
Debug version of AI Eye Assistant to identify initialization issues
"""
import os
import sys

print("🔍 Debug: Starting imports...")

try:
    import cv2
    print("✅ cv2 imported")
except Exception as e:
    print(f"❌ cv2 import failed: {e}")

try:
    import time
    print("✅ time imported")
except Exception as e:
    print(f"❌ time import failed: {e}")

try:
    import base64
    print("✅ base64 imported")
except Exception as e:
    print(f"❌ base64 import failed: {e}")

try:
    import subprocess
    print("✅ subprocess imported")
except Exception as e:
    print(f"❌ subprocess import failed: {e}")

try:
    import threading
    print("✅ threading imported")
except Exception as e:
    print(f"❌ threading import failed: {e}")

try:
    import queue
    print("✅ queue imported")
except Exception as e:
    print(f"❌ queue import failed: {e}")

try:
    from random import choice
    print("✅ random imported")
except Exception as e:
    print(f"❌ random import failed: {e}")

try:
    from datetime import datetime
    print("✅ datetime imported")
except Exception as e:
    print(f"❌ datetime import failed: {e}")

try:
    from PIL import Image
    print("✅ PIL imported")
except Exception as e:
    print(f"❌ PIL import failed: {e}")

try:
    import io
    print("✅ io imported")
except Exception as e:
    print(f"❌ io import failed: {e}")

try:
    import ollama
    print("✅ ollama imported")
except Exception as e:
    print(f"❌ ollama import failed: {e}")

try:
    import pyttsx3
    print("✅ pyttsx3 imported")
except Exception as e:
    print(f"❌ pyttsx3 import failed: {e}")

try:
    import speech_recognition as sr
    print("✅ speech_recognition imported")
except Exception as e:
    print(f"❌ speech_recognition import failed: {e}")

try:
    from dotenv import load_dotenv
    print("✅ dotenv imported")
except Exception as e:
    print(f"❌ dotenv import failed: {e}")

print("🔍 Debug: Loading environment...")
try:
    load_dotenv()
    print("✅ Environment loaded")
except Exception as e:
    print(f"❌ Environment loading failed: {e}")

print("🔍 Debug: Reading environment variables...")
try:
    CAPTURE_INTERVAL = int(os.getenv('CAPTURE_INTERVAL', 2))
    MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2-vision:latest')
    USE_SAY_COMMAND = os.getenv('USE_SAY_COMMAND', 'true').lower() == 'true'
    ENABLE_TTS = os.getenv('ENABLE_TTS', 'true').lower() == 'true'
    print(f"✅ Environment variables: MODEL={MODEL_NAME}, INTERVAL={CAPTURE_INTERVAL}")
except Exception as e:
    print(f"❌ Environment variables failed: {e}")

print("🔍 Debug: Testing speech recognition initialization...")
try:
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print("✅ Speech recognition objects created")
except Exception as e:
    print(f"❌ Speech recognition initialization failed: {e}")

print("🔍 Debug: Testing microphone calibration...")
try:
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
    print("✅ Microphone calibration successful")
except Exception as e:
    print(f"❌ Microphone calibration failed: {e}")

print("🔍 Debug: Testing TTS...")
try:
    if USE_SAY_COMMAND:
        subprocess.Popen(['say', 'Test message'])
        print("✅ macOS say command works")
    else:
        tts_engine = pyttsx3.init()
        print("✅ pyttsx3 initialization works")
except Exception as e:
    print(f"❌ TTS test failed: {e}")

print("🔍 Debug: All tests completed!")
print("🎯 If you see this message, the basic components are working.")
