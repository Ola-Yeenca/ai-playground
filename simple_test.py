#!/usr/bin/env python3
"""
Simple test of the speech recognition functionality
"""
import time
import threading
import queue
import speech_recognition as sr
import subprocess

def test_speech_recognition():
    """Test speech recognition in a simple way"""
    print("🎤 Testing Speech Recognition...")
    
    # Initialize speech recognition
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    speech_queue = queue.Queue()
    listening = True
    
    def listen_continuously():
        nonlocal listening
        print("🎧 Starting to listen...")
        while listening:
            try:
                with microphone as source:
                    print("🔊 Listening... (say something)")
                    # Listen for audio with a timeout
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                
                # Recognize speech
                text = recognizer.recognize_google(audio)
                if text and len(text.strip()) > 0:
                    speech_queue.put(text)
                    print(f"✅ You said: '{text}'")
                    
                    # Respond with TTS
                    response = f"I heard you say: {text}"
                    print(f"🤖 Responding: {response}")
                    subprocess.Popen(['say', response])
                    
            except sr.WaitTimeoutError:
                print("⏰ Timeout - no speech detected")
            except sr.UnknownValueError:
                print("❓ Could not understand audio")
            except sr.RequestError as e:
                print(f"⚠️  Speech service error: {e}")
            except Exception as e:
                print(f"❌ Error: {e}")
                time.sleep(1)
    
    # Calibrate microphone
    try:
        print("🔊 Calibrating microphone...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone calibrated")
    except Exception as e:
        print(f"⚠️  Calibration failed: {e}")
    
    # Start listening thread
    listen_thread = threading.Thread(target=listen_continuously, daemon=True)
    listen_thread.start()
    
    # Run for 30 seconds
    print("🎯 Test will run for 30 seconds. Try saying something!")
    try:
        time.sleep(30)
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    
    listening = False
    print("🏁 Test completed")

if __name__ == "__main__":
    test_speech_recognition()
