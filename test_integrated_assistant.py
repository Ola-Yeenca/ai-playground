#!/usr/bin/env python3
"""
Test the integrated AI Eye + Speech Assistant
"""
import time
from ai_eye_speech_assistant import AIEyeSpeechAssistant

def test_integrated_assistant():
    print("🧪 Testing Integrated AI Eye + Speech Assistant")
    print("=" * 50)
    
    # Create assistant
    assistant = AIEyeSpeechAssistant(demo_mode=True)
    
    print("\n🎯 Running 3 observation cycles...")
    
    try:
        for i in range(3):
            print(f"\n--- Cycle {i+1} ---")
            
            # Get demo image
            image, demo_description = assistant.create_demo_image(i)
            print(f"🎨 Demo: {demo_description}")
            
            # Analyze scene
            print("🔍 Analyzing scene...")
            analysis = assistant.analyze_scene(image)
            assistant.previous_analysis = analysis
            print("📝 Analysis:")
            print(analysis)
            
            # Test speech processing
            print("\n🗣️  Testing speech processing...")
            test_phrases = ["Hello", "What do you see?", "Tell me more"]
            test_phrase = test_phrases[i % len(test_phrases)]
            
            print(f"🎤 Simulating user saying: '{test_phrase}'")
            response = assistant.process_speech_input(test_phrase)
            print(f"🤖 AI Response: {response}")
            
            # Test TTS
            if assistant.enable_tts:
                speech_text = assistant.prepare_speech_text(analysis)
                print(f"🎤 TTS: {speech_text[:50]}...")
                assistant.speak(speech_text)
            
            assistant.observation_count += 1
            
            if i < 2:  # Don't sleep after last iteration
                print("⏳ Waiting 2 seconds...")
                time.sleep(2)
        
        print(f"\n✅ Test completed! Total observations: {assistant.observation_count}")
        print("🎯 The integrated assistant is working correctly!")
        
    except KeyboardInterrupt:
        print("\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
    finally:
        assistant.cleanup()

if __name__ == "__main__":
    test_integrated_assistant()
