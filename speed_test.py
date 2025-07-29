#!/usr/bin/env python3
"""
Quick speed test for AI Eye Assistant improvements
"""
import time
from PIL import Image
import base64
import io
import ollama

def speed_test():
    """Test the speed of image analysis"""
    print("🚀 Testing AI analysis speed improvements...")
    
    # Create test image
    test_image = Image.new('RGB', (640, 480), (100, 150, 200))
    buffered = io.BytesIO()
    test_image.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    
    # Test prompt (improved version)
    prompt = """
    You are observing through a webcam. Look at this image and give a quick analysis:
    
    🎬 Scene: [What do you see? Be specific about objects, lighting, setting]
    👤 Currently: [What is the person doing RIGHT NOW? Focus on hands, posture, eyes]
    🔮 Next Action: [Based on their current hand position, eye direction, and body language, what will they likely do in the next 10-30 seconds? Be realistic and specific]
    💡 I Notice: [One specific detail that stands out]
    
    Keep each section to 1-2 sentences. Focus on observable facts for better predictions.
    """
    
    # Time the analysis
    start_time = time.time()
    
    try:
        response = ollama.generate(
            model='llama3.2-vision',
            prompt=prompt,
            images=[img_b64],
            options={
                'temperature': 0.3,
                'top_p': 0.8,
                'num_predict': 200,
            }
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Analysis completed in {duration:.2f} seconds")
        print("\n📋 Sample Response:")
        print(response['response'])
        
        if duration < 3:
            print("\n🎯 Speed improvement successful! Analysis under 3 seconds.")
        else:
            print(f"\n⚠️  Analysis took {duration:.2f}s - may need further optimization")
            
    except Exception as e:
        print(f"❌ Speed test failed: {e}")

if __name__ == "__main__":
    speed_test()
