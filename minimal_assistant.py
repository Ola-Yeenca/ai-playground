#!/usr/bin/env python3
"""
Minimal working version of AI Eye Assistant for testing
"""
import os
import time
import base64
import subprocess
import threading
import queue
from datetime import datetime
from PIL import Image
import io
import ollama
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2-vision:latest')
ENABLE_TTS = os.getenv('ENABLE_TTS', 'true').lower() == 'true'

class MinimalAIAssistant:
    def __init__(self):
        print("🤖 Initializing Minimal AI Assistant...")
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speech_queue = queue.Queue()
        self.listening = False
        
        # Initialize speech recognition
        self.init_speech_recognition()
        
        # Start listening thread
        self.start_listening()
        
        print("✅ Minimal AI Assistant ready!")
    
    def speak(self, text):
        """Speak the given text using macOS say command"""
        if ENABLE_TTS:
            subprocess.Popen(['say', text])
    
    def init_speech_recognition(self):
        """Initialize speech recognition with microphone calibration"""
        try:
            print("🎤 Initializing speech recognition...")
            with self.microphone as source:
                print("🔊 Calibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Speech recognition ready!")
        except Exception as e:
            print(f"⚠️  Speech recognition initialization failed: {e}")
    
    def start_listening(self):
        """Start the speech recognition thread"""
        def listen_continuously():
            self.listening = True
            while self.listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    text = self.recognizer.recognize_google(audio)
                    if text and len(text.strip()) > 0:
                        self.speech_queue.put(text)
                        print(f"\n🗣️  You said: '{text}'")
                        
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"⚠️  Speech recognition service error: {e}")
                    time.sleep(1)
                except Exception as e:
                    if self.listening:
                        print(f"⚠️  Speech recognition error: {e}")
                    time.sleep(1)
        
        listen_thread = threading.Thread(target=listen_continuously, daemon=True)
        listen_thread.start()
        print("🎧 Listening for your voice input...")
    
    def process_speech_input(self, text):
        """Process speech input and generate response"""
        try:
            prompt = f"""
            You are a helpful AI assistant. The user just said: "{text}"
            Respond naturally and conversationally in 1-2 sentences.
            """
            
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'num_predict': 50,
                }
            )
            
            return response.get('response', "I'm not sure how to respond to that.")
            
        except Exception as e:
            return f"Sorry, I had trouble processing what you said: {e}"
    
    def check_for_speech_input(self):
        """Check for and process any speech input"""
        try:
            while not self.speech_queue.empty():
                text = self.speech_queue.get_nowait()
                
                print(f"\n💬 Processing: '{text}'")
                response = self.process_speech_input(text)
                
                print(f"🤖 AI Response: {response}")
                self.speak(response)
                    
        except queue.Empty:
            pass
        except Exception as e:
            print(f"⚠️  Error processing speech: {e}")
    
    def run(self):
        """Main loop"""
        print("\n🎯 Minimal AI Assistant is running!")
        print("💬 Try saying something to test the speech recognition...")
        print("⏹️  Press Ctrl+C to stop\n")
        
        try:
            observation_count = 0
            while True:
                # Check for speech input
                self.check_for_speech_input()
                
                # Simple periodic message
                if observation_count % 10 == 0:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"⏰ {current_time} - I'm listening... (observation #{observation_count})")
                
                observation_count += 1
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down... Thanks for testing!")
        finally:
            self.listening = False

if __name__ == "__main__":
    assistant = MinimalAIAssistant()
    assistant.run()
