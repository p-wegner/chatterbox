# Installation Guide for Chatterbox Voice TTS Web App

## Current Status
✅ **Web Interface**: Working (Flask app running in demo mode)
⚠️ **Chatterbox TTS**: Needs dependency installation

## Quick Start (Demo Mode)
The web app is currently running in demo mode at `http://localhost:5000`. You can:
- Test the audio recording interface
- Upload audio files
- See the UI functionality
- Test form validation

## Full Installation Steps

### Option 1: Install from PyPI (Recommended)
```bash
# Install Chatterbox TTS
pip install chatterbox-tts

# Restart the web app
python voice_tts_app.py
```

### Option 2: Install from Source
```bash
# Install build dependencies
pip install setuptools wheel

# Install Chatterbox from source
pip install -e .

# Restart the web app
python voice_tts_app.py
```

### Option 3: Manual Dependency Installation
If you encounter build issues, try installing dependencies manually:

```bash
# Install core dependencies
pip install numpy==1.25.2
pip install torch==2.6.0 torchaudio==2.6.0
pip install transformers==4.46.3
pip install diffusers==0.29.0
pip install librosa==0.11.0
pip install gradio==5.44.1

# Install specialized dependencies
pip install s3tokenizer
pip install resemble-perth==1.0.1
pip install conformer==0.3.2
pip install safetensors==0.5.3
pip install pkuseg==0.0.25
pip install pykakasi==2.3.0

# Install from source
pip install -e .
```

## Troubleshooting

### Build Issues
If you encounter "Cannot import 'setuptools.build_meta'" errors:
```bash
pip install --upgrade setuptools wheel
pip install --upgrade pip
```

### NumPy Issues
If NumPy installation fails:
```bash
pip install numpy==1.25.2 --force-reinstall
```

### Permission Issues
If you get permission errors:
```bash
pip install --user chatterbox-tts
```

## Verification

Once installed, the web app will show:
- "Chatterbox TTS is available" in the health check
- Full TTS generation functionality
- Voice cloning capabilities

Test with:
```bash
curl http://localhost:5000/health
```

Should return:
```json
{
  "status": "healthy",
  "device": "cpu",
  "chatterbox_available": true
}
```

## Web App Features

### Recording Interface
- 🎤 **Record Audio**: Click "Start Recording" to capture voice
- ⏹️ **Stop Recording**: Click when finished (3-10 seconds recommended)
- 📁 **File Upload**: Alternative to recording
- 🔊 **Preview**: Listen to recorded audio before generation

### Text Input
- 📝 **Text Area**: Enter text to synthesize (max 300 characters)
- 🔢 **Character Counter**: Shows remaining characters
- ✅ **Validation**: Ensures text is not empty

### Parameter Controls
- 🎭 **Exaggeration**: Control emotion intensity (0.25-2.0)
- 🌡️ **Temperature**: Control randomness (0.05-5.0)
- 🔄 **Reset**: Return to default settings

### Generation & Output
- 🎵 **Generate TTS**: Create audio with voice cloning
- 💾 **Download**: Save generated audio
- 🔊 **Playback**: Listen to results

## Browser Requirements
- Chrome 66+
- Firefox 60+
- Safari 14+
- Edge 79+

## Next Steps
1. Open `http://localhost:5000` in your browser
2. Test the recording interface
3. Install Chatterbox dependencies using one of the methods above
4. Restart the app and test full TTS functionality