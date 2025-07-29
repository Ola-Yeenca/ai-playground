#!/usr/bin/env python3
"""
Simple camera test
"""
import cv2
import time

def test_camera():
    print("🔍 Testing camera access...")
    
    try:
        # Try to open camera
        cap = cv2.VideoCapture(0)
        print(f"📹 Camera opened: {cap.isOpened()}")
        
        if cap.isOpened():
            # Give camera time to initialize
            time.sleep(2)
            
            # Try to read a frame
            ret, frame = cap.read()
            print(f"📸 Frame captured: {ret}")
            
            if ret and frame is not None:
                print(f"✅ Camera working! Frame shape: {frame.shape}")
                
                # Show frame for 3 seconds
                cv2.imshow('Camera Test', frame)
                print("👁️  Showing camera feed for 3 seconds...")
                cv2.waitKey(3000)
                cv2.destroyAllWindows()
            else:
                print("❌ Camera opened but couldn't capture frame")
            
            cap.release()
        else:
            print("❌ Could not open camera")
            
    except Exception as e:
        print(f"❌ Camera test failed: {e}")

if __name__ == "__main__":
    test_camera()
