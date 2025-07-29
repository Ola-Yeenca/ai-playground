#!/usr/bin/env python3
"""
Simple smoke test for Ollama connectivity and model availability
"""
import ollama
from PIL import Image
import base64
import io

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        models = ollama.list()
        print("✅ Ollama is running!")
        
        # Check if models exist and extract names
        if 'models' in models and models['models']:
            model_names = []
            for model in models['models']:
                if isinstance(model, dict) and 'name' in model:
                    model_names.append(model['name'])
                elif isinstance(model, str):
                    model_names.append(model)
            print(f"📦 Available models: {model_names}")
        else:
            print("⚠️  No models found")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

def test_vision_model():
    """Test the vision model with a simple image"""
    try:
        # Create a simple test image
        test_image = Image.new('RGB', (100, 100), (255, 0, 0))  # Red square
        
        # Convert to base64
        buffered = io.BytesIO()
        test_image.save(buffered, format="JPEG")
        img_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Test the model
        response = ollama.generate(
            model='llama3.2-vision',
            prompt='What color is this image? Just say the color.',
            images=[img_b64]
        )
        
        result = response['response'].lower()
        print(f"✅ Vision model works! Response: {result}")
        
        # Check if it mentions red (it's a red image)
        if 'red' in result:
            print("🎯 Model correctly identified the red color!")
            return True
        else:
            print("⚠️  Model response doesn't mention red, but it's working")
            return True
            
    except Exception as e:
        print(f"❌ Vision model test failed: {e}")
        return False

def main():
    print("🧪 Testing AI Eye Assistant components...\n")
    
    # Test 1: Ollama connection
    print("1. Testing Ollama connection...")
    ollama_ok = test_ollama_connection()
    
    # Test 2: Vision model
    if ollama_ok:
        print("\n2. Testing vision model...")
        vision_ok = test_vision_model()
    else:
        vision_ok = False
    
    print("\n" + "="*50)
    if ollama_ok and vision_ok:
        print("🎉 All tests passed! AI Eye Assistant is ready to run!")
        print("To start: python ai_eye_assistant.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
    print("="*50)

if __name__ == "__main__":
    main()
