import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
import io
import base64
from ai_eye_assistant import AIEyeAssistant

class TestAIEyeAssistant(unittest.TestCase):
    @patch('ai_eye_assistant.cv2.VideoCapture')
    def setUp(self, mock_video_capture):
        # Mock the webcam
        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap
        
        # Suppress the opening message
        with patch('builtins.print'):
            self.assistant = AIEyeAssistant()
        
        # Create a simple black image for testing
        self.black_image = Image.new('RGB', (640, 480), (0, 0, 0))

    def test_image_to_base64(self):
        """Test conversion of image to base64 string"""
        b64_str = self.assistant.image_to_base64(self.black_image)
        decoded_img = base64.b64decode(b64_str)
        img = Image.open(io.BytesIO(decoded_img))
        self.assertEqual(img.size, (640, 480), "Image size should be 640x480")

    @patch('ai_eye_assistant.ollama.generate')
    def test_analyze_scene(self, mock_generate):
        """Test scene analysis with a mock response"""
        mock_generate.return_value = {'response': "Mock analysis result"}
        result = self.assistant.analyze_scene(self.black_image)
        self.assertEqual(result, "Mock analysis result", "Should return the mock analysis result")

    def tearDown(self):
        self.assistant.cleanup()

if __name__ == "__main__":
    unittest.main()

