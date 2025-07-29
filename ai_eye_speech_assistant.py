#!/usr/bin/env python3
"""
AI Eye Assistant with Integrated Speech Recognition
Combines webcam observation with voice interaction
"""
import os
import cv2
import time
import base64
import subprocess
import threading
import queue
from random import choice
from datetime import datetime
from PIL import Image
import io
import ollama
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CAPTURE_INTERVAL = int(os.getenv('CAPTURE_INTERVAL', 2))
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2-vision:latest')
USE_SAY_COMMAND = os.getenv('USE_SAY_COMMAND', 'true').lower() == 'true'
ENABLE_TTS = os.getenv('ENABLE_TTS', 'true').lower() == 'true'

class AIEyeSpeechAssistant:
    def __init__(self, demo_mode=False):
        print("🤖 Initializing AI Eye + Speech Assistant...")
        
        self.demo_mode = demo_mode
        self.cap = None
        self.previous_analysis = None
        self.observation_count = 0
        self.use_say_command = USE_SAY_COMMAND
        self.enable_tts = ENABLE_TTS
        
        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speech_queue = queue.Queue()
        self.listening = False

        # TTS management
        self.current_speech_process = None
        
        # Initialize components
        self.setup_speech_recognition()
        self.setup_camera()
        self.start_listening()
        
        print("✅ AI Eye + Speech Assistant ready!")
        print("👁️  Observing through camera every 2 seconds")
        print("🗣️  Listening for your voice continuously")
        print("💬 Try saying: 'Hello', 'What do you see?', 'Describe what's happening'")
        print("⏹️  Press Ctrl+C to stop\n")
    
    def setup_speech_recognition(self):
        """Initialize speech recognition"""
        try:
            print("🎤 Setting up speech recognition...")
            # Quick microphone test without blocking calibration
            print("✅ Speech recognition ready")
        except Exception as e:
            print(f"⚠️  Speech setup failed: {e}")
    
    def setup_camera(self):
        """Initialize camera"""
        print("📹 Setting up camera...")
        if self.demo_mode:
            print("🎨 Demo mode - using test images")
        else:
            print("🔍 Attempting to connect to camera...")
            self.cap = cv2.VideoCapture(0)

            # Give camera time to initialize
            import time
            time.sleep(1)

            # Test camera with a frame read
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    print("✅ Camera ready and working!")
                    print(f"📐 Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
                else:
                    print("⚠️  Camera opened but can't read frames, switching to demo mode")
                    self.cap.release()
                    self.demo_mode = True
            else:
                print("⚠️  Camera not available, switching to demo mode")
                self.demo_mode = True
    
    def start_listening(self):
        """Start speech recognition in background"""
        def listen_continuously():
            self.listening = True
            # Calibrate microphone in the background thread
            try:
                with self.microphone as source:
                    print("🔊 Calibrating microphone in background...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    print("✅ Microphone calibrated")
            except Exception as e:
                print(f"⚠️  Microphone calibration failed: {e}")

            while self.listening:
                try:
                    with self.microphone as source:
                        # Shorter timeout to reduce audio conflicts
                        audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=3)

                    text = self.recognizer.recognize_google(audio)
                    if text and len(text.strip()) > 0:
                        self.speech_queue.put(text)
                        print(f"\n🗣️  You said: '{text}'")

                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    print(f"⚠️  Speech service error: {e}")
                    time.sleep(2)
                except Exception as e:
                    if self.listening:
                        # Less verbose error reporting
                        pass
                    time.sleep(2)

        listen_thread = threading.Thread(target=listen_continuously, daemon=True)
        listen_thread.start()
        print("🎧 Background speech listening started")
    
    def speak(self, text):
        """Text-to-speech output"""
        if self.enable_tts:
            # Stop any current speech
            if self.current_speech_process and self.current_speech_process.poll() is None:
                self.current_speech_process.terminate()
                try:
                    self.current_speech_process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    self.current_speech_process.kill()

            # Start new speech
            self.current_speech_process = subprocess.Popen(['say', text])
    
    def image_to_base64(self, image):
        """Convert PIL Image to base64"""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def frame_to_image(self, frame):
        """Convert OpenCV frame to PIL Image"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_frame)
    
    def create_demo_image(self, scenario_num):
        """Create demo images"""
        scenarios = [
            ("Person at desk with laptop", (100, 150, 200)),
            ("Coffee cup and notebook", (200, 150, 100)),
            ("Plant on windowsill", (100, 200, 100)),
            ("Books on shelf", (150, 100, 200)),
            ("Kitchen scene", (200, 200, 100)),
        ]
        
        scenario = scenarios[scenario_num % len(scenarios)]
        description, color = scenario
        image = Image.new('RGB', (640, 480), color)
        return image, description
    
    def analyze_scene(self, image):
        """Analyze image with AI"""
        try:
            prompt = """
            You are observing through a webcam. Analyze this image and provide:
            
            🎬 Scene: [What do you see? Objects, lighting, setting]
            👤 Currently: [What is the person doing RIGHT NOW?]
            🔮 Next Action: [What will they likely do next?]
            💡 Notice: [One interesting detail]
            
            Keep each section to 1-2 sentences.
            """
            
            image_b64 = self.image_to_base64(image)
            
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
                images=[image_b64],
                options={
                    'temperature': 0.3,
                    'top_p': 0.8,
                    'num_predict': 200,
                }
            )
            
            return response['response']
            
        except Exception as e:
            return f"❌ Analysis failed: {str(e)}"
    
    def process_speech_input(self, text):
        """Process speech and generate response"""
        try:
            context = ""
            if self.previous_analysis:
                context = f"Recent observation: {self.previous_analysis[:150]}..."
            
            prompt = f"""
            You are an AI with vision that has been observing the user.
            Observations made: {self.observation_count}
            
            {context}
            
            User said: "{text}"
            
            Respond naturally and conversationally (1-2 sentences).
            Reference your observations when relevant.
            """
            
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'num_predict': 80,
                }
            )
            
            return response.get('response', "I'm not sure how to respond.")
            
        except Exception as e:
            return f"Sorry, I had trouble processing that: {e}"
    
    def check_for_speech_input(self):
        """Process any pending speech input"""
        try:
            while not self.speech_queue.empty():
                text = self.speech_queue.get_nowait()
                
                print(f"💬 Processing: '{text}'")
                response = self.process_speech_input(text)
                
                print(f"🤖 AI: {response}")
                self.speak(response)
                    
        except queue.Empty:
            pass
        except Exception as e:
            print(f"⚠️  Speech processing error: {e}")
    
    def prepare_speech_text(self, analysis):
        """Convert analysis to speech"""
        try:
            import re
            lines = analysis.split('\n')
            scene = ""
            currently = ""
            
            for line in lines:
                line = line.strip()
                if 'Scene:' in line:
                    scene = re.sub(r'[🎬🎭🎪🎯]', '', line.replace('Scene:', '').strip())
                elif 'Currently:' in line:
                    currently = re.sub(r'[👤👥👨👩]', '', line.replace('Currently:', '').strip())
            
            speech_parts = []
            if scene:
                speech_parts.append(f"I can see {scene.lower()}")
            if currently:
                speech_parts.append(f"You're currently {currently.lower()}")
            
            return ". ".join(speech_parts) + "." if speech_parts else "Observation complete."
                
        except Exception as e:
            return "Observation complete."
    
    def run(self):
        """Main observation and interaction loop"""
        try:
            while True:
                # Get image (camera or demo)
                if self.demo_mode:
                    image, demo_description = self.create_demo_image(self.observation_count)
                    print(f"🎨 Demo: {demo_description}")
                else:
                    ret, frame = self.cap.read()
                    if not ret:
                        print("❌ Camera capture failed")
                        break
                    image = self.frame_to_image(frame)
                
                # Analyze scene
                current_time = datetime.now().strftime("%H:%M:%S")
                print(f"\n{'='*50}")
                print(f"🕒 Observation #{self.observation_count + 1} at {current_time}")
                print(f"{'='*50}")
                
                analysis = self.analyze_scene(image)
                self.previous_analysis = analysis
                print(analysis)
                
                # Speak analysis
                if self.enable_tts:
                    speech_text = self.prepare_speech_text(analysis)
                    print(f"🎤 Speaking: {speech_text[:50]}...")
                    self.speak(speech_text)
                
                # Process any speech input
                self.check_for_speech_input()
                
                self.observation_count += 1
                
                # Show camera feed (if not demo)
                if not self.demo_mode:
                    cv2.imshow('AI Eye Assistant (Press Q to quit)', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                time.sleep(CAPTURE_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n👋 AI Eye + Speech Assistant shutting down...")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.listening = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print(f"📊 Total observations: {self.observation_count}")

if __name__ == "__main__":
    import sys
    demo_mode = len(sys.argv) > 1 and sys.argv[1] == '--demo'
    
    assistant = AIEyeSpeechAssistant(demo_mode=demo_mode)
    assistant.run()
