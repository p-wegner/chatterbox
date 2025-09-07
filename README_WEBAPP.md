# Chatterbox Voice TTS Web App

A simple web application that allows users to record audio samples and use Chatterbox to synthesize text with the recorded voice as reference.

## Features

- **Audio Recording**: Record voice samples directly in your browser
- **Voice Cloning**: Use recorded audio as reference for TTS generation
- **Text-to-Speech**: Generate natural-sounding speech with custom voice
- **Parameter Control**: Adjust exaggeration and temperature settings
- **Audio Output**: Play and download generated TTS audio

## Quick Start

1. **Install dependencies using Poetry**:
   ```bash
   poetry install
   ```

2. **Run the application**:
   ```bash
   poetry run python voice_tts_app.py
   ```

3. **Open your browser**:
   Navigate to `http://localhost:5000`

Alternatively, you can install dependencies directly:
```bash
pip install chatterbox-tts flask
python voice_tts_app.py
```

## Usage

1. **Record Audio**: Click "Start Recording" and speak for 3-10 seconds
2. **Enter Text**: Type the text you want to synthesize (max 300 characters)
3. **Adjust Settings**: Modify exaggeration and temperature if desired
4. **Generate TTS**: Click "Generate TTS" to create audio with your voice
5. **Download**: Save the generated audio file

## Requirements

- Python 3.10+
- Modern web browser with microphone access
- Chatterbox TTS library (automatically installed)
- Poetry (recommended) or pip for dependency management

## Browser Support

- Chrome 66+
- Firefox 60+
- Safari 14+
- Edge 79+

## Technical Details

- **Backend**: Flask web framework
- **Frontend**: HTML5, CSS3, vanilla JavaScript
- **Audio**: Web Audio API, MediaRecorder API
- **TTS**: Chatterbox TTS library
- **Audio Format**: WAV (24kHz)

## Project Structure

```
voice_tts_app.py          # Main Flask application
templates/
  └── index.html         # Main web interface
static/
  ├── css/
  │   └── style.css      # Application styles
  └── js/
      └── app.js         # Frontend JavaScript
uploads/                 # Temporary audio file storage
pyproject.toml          # Poetry project configuration
poetry.lock             # Poetry lock file
requirements.txt         # Pip-compatible dependencies
README_WEBAPP.md        # Web app documentation
INSTALLATION_GUIDE.md   # Detailed installation guide
```

## Troubleshooting

### Microphone Access
- Ensure your browser has microphone permissions
- Check that your microphone is properly connected
- Try refreshing the page if microphone access fails

### TTS Generation Issues
- Make sure you have recorded audio and entered text
- Check that the audio recording is clear and at least 3 seconds long
- Verify that your system meets the requirements for Chatterbox TTS

### Performance
- TTS generation may take 10-30 seconds depending on your hardware
- GPU acceleration is recommended for better performance
- Close other applications if experiencing slow performance

## Development

This project is part of the Chatterbox TTS ecosystem. See the main documentation for more details about the TTS model and its capabilities.