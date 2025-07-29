#!/usr/bin/env python3
"""
Test the camera-enabled assistant initialization
"""
import time
from ai_eye_speech_assistant import AIEyeSpeechAssistant

def test_camera_assistant():
    print("🧪 Testing Camera-Enabled AI Eye + Speech Assistant")
    print("=" * 60)
    
    try:
        # Create assistant WITHOUT demo mode (should use camera)
        print("🚀 Creating assistant with camera...")
        assistant = AIEyeSpeechAssistant(demo_mode=False)
        
        print(f"\n📊 Assistant Status:")
        print(f"   Demo Mode: {assistant.demo_mode}")
        print(f"   Camera: {'Available' if assistant.cap else 'Not Available'}")
        print(f"   TTS Enabled: {assistant.enable_tts}")
        
        if not assistant.demo_mode and assistant.cap:
            print("\n📸 Testing camera capture...")
            ret, frame = assistant.cap.read()
            if ret:
                print(f"✅ Camera capture successful! Frame: {frame.shape}")
                
                # Test one analysis
                print("\n🔍 Testing scene analysis...")
                image = assistant.frame_to_image(frame)
                analysis = assistant.analyze_scene(image)
                print("📝 Analysis:")
                print(analysis[:200] + "..." if len(analysis) > 200 else analysis)
                
                # Test TTS
                print("\n🎤 Testing TTS...")
                speech_text = assistant.prepare_speech_text(analysis)
                print(f"Speech text: {speech_text[:100]}...")
                assistant.speak("Camera test successful!")
                
            else:
                print("❌ Camera capture failed")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'assistant' in locals():
            assistant.cleanup()

if __name__ == "__main__":
    test_camera_assistant()
