#!/usr/bin/env python3
"""
Quick test for the new Text-to-Speech functionality
"""
import platform
import subprocess

def test_tts():
    """Test both macOS 'say' command and pyttsx3"""
    print("🎤 Testing Text-to-Speech functionality...\n")
    
    # Test 1: macOS 'say' command
    if platform.system() == "Darwin":
        print("1. Testing macOS 'say' command...")
        try:
            subprocess.run(["say", "This is a test of the macOS say command"], check=True)
            print("✅ 'say' command works!")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"❌ 'say' command failed: {e}")
    else:
        print("Skipping macOS 'say' command test (not on macOS)")
        
    # Test 2: pyttsx3 library
    print("\n2. Testing pyttsx3 library...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say("This is a test of the pyttsx3 library")
        engine.runAndWait()
        print("✅ pyttsx3 works!")
    except Exception as e:
        print(f"❌ pyttsx3 failed: {e}")
        
    print("\n🎉 TTS test complete! You can configure TTS in the .env file")
    print("   - ENABLE_TTS: true/false (default: true)")
    print("   - USE_SAY_COMMAND: true/false (default: true)")

if __name__ == "__main__":
    test_tts()
