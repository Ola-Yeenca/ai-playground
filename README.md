# 🤖 AI Eye Assistant

Your personal AI companion that uses your webcam as its eyes to understand your environment, analyze what you're doing, and predict your next actions using **local AI models** via Ollama. Now with **🎤 Speech Recognition & Text-to-Speech** for full voice interaction!

## 🌟 Features

- **Real-time Environment Analysis**: AI observes your workspace through your webcam
- **Activity Recognition**: Understands what you're currently doing
- **Behavior Prediction**: Attempts to predict your next actions based on context
- **Conversational AI**: Provides engaging, friendly commentary about your activities
- **🎤 Text-to-Speech Narration**: AI speaks its observations out loud
- **🗣️ Speech Recognition**: Listen for voice commands and questions (NEW!)
- **💬 Conversational AI**: Responds to speech with visual context (NEW!)
- **Live Webcam Feed**: Optional visual feedback of what the AI is seeing
- **Demo Mode**: Test without webcam using generated scenarios
- **🧵 Multi-threaded**: Vision and speech work simultaneously

## 🔧️ Setup

### 1. Install Ollama (if not already installed)
```bash
brew install ollama
```

### 2. Download the Vision Model
```bash
ollama pull llama3.2-vision
```

### 3. Run the Assistant
```bash
# Activate the virtual environment
source ai-eye-env/bin/activate

# Run the AI Eye Assistant with Speech Recognition
python ai_eye_speech_assistant.py

# Or run the original version (vision only)
python ai_eye_assistant.py
```

### 4. Test TTS (Optional)
```bash
# Test the text-to-speech functionality
python test_tts.py
```

## 🎮 Usage

- The AI will start analyzing your environment every 2 seconds by default
- 🎤 **AI narrates observations** using text-to-speech (can be disabled)
- 🗣️ **Talk to the AI** - it listens continuously for your voice
- A webcam window will appear showing what the AI sees
- Press **Q** in the webcam window to quit
- Or press **Ctrl+C** in the terminal to stop

### 💬 Voice Commands to Try:
- "Hello" - Start a conversation
- "What do you see?" - Ask about current observations
- "Describe what's happening" - Get detailed scene analysis
- "Tell me more" - Get additional details
- Any natural conversation - AI responds with visual context!

## ⚙️ Configuration

Edit the `.env` file to customize:
- `MODEL_NAME`: Ollama model to use (default: llama3.2-vision)
- `CAPTURE_INTERVAL`: How often to analyze (in seconds, default: 2)
- `ENABLE_TTS`: Enable/disable text-to-speech (default: true)
- `USE_SAY_COMMAND`: Use macOS 'say' vs pyttsx3 (default: true)

## 📋 What the AI Observes

The AI Eye Assistant will tell you:
- 🎬 **Scene**: What's happening in your environment
- 👤 **Currently**: What you appear to be doing
- 🔮 **Next Action**: Predictions about what you might do next
- 💡 **I Notice**: Interesting details it spots

## 🔒 Privacy

- **✅ Fully Local Processing**: Images are processed locally via Ollama - no data sent to external APIs!
- No images are permanently stored on your device
- Camera access can be revoked by quitting the application
- All processing happens on your machine for maximum privacy

## 🎤 Text-to-Speech Options

1. **macOS 'say' Command** (default): Fast, built-in, high-quality
2. **pyttsx3**: Cross-platform Python TTS library (fallback)

Configure in `.env`:
```
ENABLE_TTS=true          # Enable/disable TTS
USE_SAY_COMMAND=true     # Use 'say' vs pyttsx3
```

## 🚀 Ideas for Enhancement

- ✅ ~~Add voice narration using text-to-speech~~ **DONE!**
- Create activity logging and daily summaries
- Add gesture recognition for commands
- Implement mood tracking over time
- Add different voice personalities
- Voice command controls ("pause", "faster", etc.)

## 🐛 Troubleshooting

**Camera not working?**
- Make sure no other apps are using your webcam
- Check camera permissions in System Preferences > Security & Privacy
- Try demo mode: modify the script to use `AIEyeAssistant(demo_mode=True)`

**Ollama/Model errors?**
- Ensure Ollama is installed: `brew install ollama`
- Download the model: `ollama pull llama3.2-vision`
- Check if Ollama is running: `ollama list`

**TTS not working?**
- Run `python test_tts.py` to diagnose TTS issues
- Try switching between 'say' and pyttsx3 in `.env`
- On macOS, ensure 'say' command works: `say "test"`

**Dependencies issues?**
- Make sure you're in the virtual environment: `source ai-eye-env/bin/activate`
- Reinstall packages: `pip install -r requirements.txt`

Enjoy your AI companion! 🤖👁️
