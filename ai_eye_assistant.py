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
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CAPTURE_INTERVAL = int(os.getenv('CAPTURE_INTERVAL', 2))  # Faster observations
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2-vision')
USE_SAY_COMMAND = os.getenv('USE_SAY_COMMAND', 'true').lower() == 'true'
ENABLE_TTS = os.getenv('ENABLE_TTS', 'true').lower() == 'true'

# Model check function removed for simpler startup

class AIEyeAssistant:
    def __init__(self, demo_mode=False):
        print("🤖 Initializing AI Eye Assistant...")

        self.demo_mode = demo_mode
        self.cap = None
        self.previous_analysis = None
        self.observation_count = 0
        self.activity_history = []  # Track recent activities for better predictions
        self.use_say_command = USE_SAY_COMMAND
        self.enable_tts = ENABLE_TTS
        self.tts_engine = None

        # Speech recognition setup
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.speech_queue = queue.Queue()
        self.listening = False

        print("🎤 Setting up speech recognition...")
        # Initialize speech recognition
        self.init_speech_recognition()

        # Start listening thread
        self.start_listening()

        # Show TTS status
        if self.enable_tts:
            tts_method = "macOS 'say' command" if self.use_say_command else "pyttsx3"
            print(f"🔊 Text-to-Speech enabled using {tts_method}")
        else:
            print("🔇 Text-to-Speech disabled")

        # Initialize TTS engine if needed
        if self.enable_tts and not self.use_say_command:
            try:
                self.tts_engine = pyttsx3.init()
            except Exception as e:
                print(f"⚠️  pyttsx3 initialization failed: {e}")
                print("Falling back to macOS 'say' command")
                self.use_say_command = True

        # Fun opening lines
        self.opening_lines = [
            "👁️ AI Eyes activated! I'm now your digital observer...",
            "🔍 Ready to see the world through AI vision!",
            "🤖 Your AI companion is watching and learning!",
            "📹 Webcam connected - Let's see what you're up to!",
        ]

        print("📹 Setting up camera...")
        if demo_mode:
            print("🎨 Running in DEMO mode - using test images instead of webcam")
        else:
            print(choice(self.opening_lines))

        print(f"📊 Analyzing every {CAPTURE_INTERVAL} seconds...")

        # Initialize camera only if not in demo mode
        if not demo_mode:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("❌ Error: Could not open webcam")
                print("💫 This could be due to:")
                print("   • Camera permission not granted")
                print("   • Camera is being used by another app")
                print("   • No camera available")
                print()
                print("🎨 Switching to demo mode...")
                self.demo_mode = True

        print("✅ AI Eye Assistant initialization complete!")
        print("🎯 Ready to observe and interact!")
        print("👁️  I'll continuously observe through the camera")
        print("🗣️  I'll listen for your voice and respond")
        print("💬 Try saying: 'Hello', 'What do you see?', 'How are you?'")
        print("⏹️  Press Ctrl+C to stop\n")
            
    def speak(self, text):
        """Speak the given text using the selected TTS engine"""
        if self.use_say_command:
            # Use macOS say command (non-blocking)
            subprocess.Popen(['say', text])
        elif self.tts_engine:
            # Use pyttsx3 (can be blocking, so run in a thread)
            def run_tts():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            tts_thread = threading.Thread(target=run_tts)
            tts_thread.start()
    
    def prepare_speech_text(self, analysis):
        """Extract and prepare key parts of analysis for speech"""
        try:
            # Remove emojis and format markers for cleaner speech
            import re
            
            # Extract sections
            lines = analysis.split('\n')
            scene = ""
            currently = ""
            next_action = ""
            notice = ""
            
            for line in lines:
                line = line.strip()
                if 'Scene:' in line:
                    scene = re.sub(r'[🎬🎭🎪🎯]', '', line.replace('Scene:', '').strip())
                elif 'Currently:' in line:
                    currently = re.sub(r'[👤👥👨👩]', '', line.replace('Currently:', '').strip())
                elif 'Next Action:' in line:
                    next_action = re.sub(r'[🔮✨🎯]', '', line.replace('Next Action:', '').strip())
                elif 'Notice:' in line or 'I Notice:' in line:
                    notice = re.sub(r'[💡🔍👀]', '', line.replace('I Notice:', '').replace('Notice:', '').strip())
            
            # Create a natural speech flow
            speech_parts = []
            
            if scene:
                speech_parts.append(f"I can see {scene.lower()}")
            
            if currently:
                speech_parts.append(f"You're currently {currently.lower()}")
            
            if next_action:
                speech_parts.append(f"I predict you'll {next_action.lower()}")
            
            # Combine into natural speech
            if speech_parts:
                return ". ".join(speech_parts) + "."
            else:
                return "I'm analyzing what I see."
                
        except Exception as e:
            print(f"⚠️  Speech preparation failed: {e}")
            return "Observation complete."
            
    def frame_to_image(self, frame):
        """Convert OpenCV frame to PIL Image"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_frame)
        
    def image_to_base64(self, image):
        """Convert PIL Image to base64 string for Ollama"""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def analyze_scene(self, image):
        """Send image to Ollama for analysis"""
        try:
            # More focused prompt for better predictions
            prompt = f"""
            You are observing through a webcam. Look at this image and give a quick analysis:
            
            🎬 Scene: [What do you see? Be specific about objects, lighting, setting]
            👤 Currently: [What is the person doing RIGHT NOW? Focus on hands, posture, eyes]
            🔮 Next Action: [Based on their current hand position, eye direction, and body language, what will they likely do in the next 10-30 seconds? Be realistic and specific]
            💡 I Notice: [One specific detail that stands out]
            
            Keep each section to 1-2 sentences. Focus on observable facts for better predictions.
            """
            
            # Convert image to base64
            image_b64 = self.image_to_base64(image)
            
            # Send to Ollama with faster settings
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
                images=[image_b64],
                options={
                    'temperature': 0.3,  # Lower temperature for more focused responses
                    'top_p': 0.8,        # Reduce randomness
                    'num_predict': 200,   # Limit response length for speed
                }
            )
            
            return response['response']
            
        except Exception as e:
            return f"❌ Analysis failed: {str(e)}"
    
    def create_demo_image(self, scenario_num):
        """Create demo images for testing"""
        demo_scenarios = [
            ("Person at desk with laptop", (100, 150, 200)),  # Blue-ish
            ("Coffee cup and notebook", (200, 150, 100)),     # Brown-ish
            ("Plant on windowsill", (100, 200, 100)),        # Green-ish
            ("Books on shelf", (150, 100, 200)),             # Purple-ish
            ("Kitchen with cooking utensils", (200, 200, 100)), # Yellow-ish
        ]
        
        scenario = demo_scenarios[scenario_num % len(demo_scenarios)]
        description, color = scenario
        
        # Create a simple colored image
        image = Image.new('RGB', (640, 480), color)
        
        # You could add more complex demo images here
        return image, description
    
    def run(self):
        """Main loop for the AI Eye Assistant"""
        try:
            while True:
                if self.demo_mode:
                    # Create demo image
                    image, demo_description = self.create_demo_image(self.observation_count)
                    print(f"🎨 Demo scenario: {demo_description}")
                else:
                    # Capture frame from webcam
                    ret, frame = self.cap.read()
                    if not ret:
                        print("❌ Failed to capture image")
                        break
                    
                    # Convert to PIL Image
                    image = self.frame_to_image(frame)
                
                # Get current time
                current_time = datetime.now().strftime("%H:%M:%S")
                
                print(f"\n{'='*60}")
                print(f"🕒 Observation #{self.observation_count + 1} at {current_time}")
                print(f"{'='*60}")
                
                # Analyze with AI
                analysis = self.analyze_scene(image)
                self.previous_analysis = analysis  # Store for speech context
                print(analysis)

                # Speak the analysis if TTS is enabled
                if self.enable_tts:
                    speech_text = self.prepare_speech_text(analysis)
                    if speech_text:
                        print(f"🎤 Speaking: {speech_text[:50]}...")
                        self.speak(speech_text)

                # Check for user speech input (process any pending speech)
                self.check_for_speech_input()

                self.observation_count += 1
                
                # Show webcam feed only if not in demo mode
                if not self.demo_mode:
                    cv2.imshow('AI Eye Assistant - Webcam Feed (Press Q to quit)', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("\n👀 Press Ctrl+C to stop the demo")
                
                # Wait before next analysis
                time.sleep(CAPTURE_INTERVAL)
                
        except KeyboardInterrupt:
            print("\n\n👋 AI Eyes shutting down... Thanks for letting me observe!")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.cleanup()
    
    def init_speech_recognition(self):
        """Initialize speech recognition with microphone calibration"""
        try:
            print("🎤 Initializing speech recognition...")
            # Adjust for ambient noise
            with self.microphone as source:
                print("🔊 Calibrating microphone for ambient noise... (this may take a moment)")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Speech recognition ready! You can speak to the AI anytime.")
        except Exception as e:
            print(f"⚠️  Speech recognition initialization failed: {e}")
            print("Speech input will not be available.")
    
    def start_listening(self):
        """Start the speech recognition thread"""
        def listen_continuously():
            self.listening = True
            while self.listening:
                try:
                    with self.microphone as source:
                        # Listen for audio with a timeout to prevent blocking
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Recognize speech in the background
                    text = self.recognizer.recognize_google(audio)
                    if text and len(text.strip()) > 0:
                        self.speech_queue.put(text)
                        print(f"\n🗣️  You said: '{text}'")
                        
                except sr.WaitTimeoutError:
                    # Normal timeout, continue listening
                    pass
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    pass
                except sr.RequestError as e:
                    print(f"⚠️  Speech recognition service error: {e}")
                    time.sleep(1)
                except Exception as e:
                    if self.listening:  # Only show error if still supposed to be listening
                        print(f"⚠️  Speech recognition error: {e}")
                    time.sleep(1)
        
        # Start listening thread
        listen_thread = threading.Thread(target=listen_continuously, daemon=True)
        listen_thread.start()
        print("🎧 Listening for your voice input in the background...")
    
    def process_speech_input(self, text):
        """Process speech input and generate conversational response"""
        try:
            # Create a conversational prompt with context from recent observations
            context = ""
            if self.previous_analysis:
                context = f"Recent observation: {self.previous_analysis[:200]}..."

            prompt = f"""
            You are an AI assistant with vision capabilities that has been observing the user through their webcam.
            You have made {self.observation_count} observations so far.

            {context}

            The user just said: "{text}"

            Respond naturally and conversationally. You can:
            - Answer questions about what you've been observing
            - Respond to greetings or casual conversation
            - Comment on what you currently see if asked
            - Reference your recent observations when relevant
            - Be helpful and friendly

            Keep your response concise (1-3 sentences) and natural. Don't be overly formal.
            """

            # Get response from the LLM (text-only, no image needed for conversation)
            response = ollama.generate(
                model=MODEL_NAME,
                prompt=prompt,
                options={
                    'temperature': 0.7,  # More natural for conversation
                    'top_p': 0.9,
                    'num_predict': 100,  # Keep responses concise
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
                
                print(f"\n💬 Processing your input: '{text}'")
                response = self.process_speech_input(text)
                
                print(f"🤖 AI Response: {response}")
                
                # Speak the response
                if self.enable_tts:
                    self.speak(response)
                    
        except queue.Empty:
            pass
        except Exception as e:
            print(f"⚠️  Error processing speech input: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        self.listening = False  # Stop the listening thread
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print(f"📊 Total observations made: {self.observation_count}")

if __name__ == "__main__":
    import sys

    # Check for demo mode argument
    demo_mode = len(sys.argv) > 1 and sys.argv[1] == '--demo'

    print("🚀 Starting AI Eye Assistant...")

    # Skip model check for now and start directly
    try:
        assistant = AIEyeAssistant(demo_mode=demo_mode)
        assistant.run()
    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        import traceback
        traceback.print_exc()

