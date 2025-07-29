#!/usr/bin/env python3
"""
Simple test script for the AI Eye Assistant
"""
import os
import ollama
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.2-vision:latest')

def test_model():
    """Test if the model is working"""
    try:
        print(f"Testing model: {MODEL_NAME}")
        
        # Test with a simple text prompt
        response = ollama.generate(
            model=MODEL_NAME,
            prompt="Hello! Can you respond to this test message?",
            options={
                'temperature': 0.7,
                'num_predict': 50,
            }
        )
        
        print(f"✅ Model test successful!")
        print(f"Response: {response.get('response', 'No response')}")
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition import"""
    try:
        import speech_recognition as sr
        print("✅ SpeechRecognition imported successfully")
        
        # Test microphone access
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        print("✅ Microphone access successful")
        return True
        
    except Exception as e:
        print(f"❌ Speech recognition test failed: {e}")
        return False

def test_tts():
    """Test text-to-speech"""
    try:
        import pyttsx3
        print("✅ pyttsx3 imported successfully")
        
        # Test macOS say command
        import subprocess
        result = subprocess.run(['which', 'say'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ macOS 'say' command available")
        else:
            print("⚠️  macOS 'say' command not found")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AI Eye Assistant Components")
    print("=" * 50)
    
    # Test all components
    model_ok = test_model()
    speech_ok = test_speech_recognition()
    tts_ok = test_tts()
    
    print("\n" + "=" * 50)
    if model_ok and speech_ok and tts_ok:
        print("✅ All tests passed! Ready to run the full assistant.")
    else:
        print("❌ Some tests failed. Check the errors above.")
