from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
import torch
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Device detection and model setup
if torch.cuda.is_available():
    DEVICE = "cuda"
    print(f"CUDA detected, using device: {DEVICE}")
elif torch.backends.mps.is_available():
    DEVICE = "mps"
    print(f"Apple Silicon detected, using device: {DEVICE}")
else:
    DEVICE = "cpu"
    print(f"No GPU detected, using device: {DEVICE}")

# Supported languages
SUPPORTED_LANGUAGES = {
    'ar': 'Arabic',
    'da': 'Danish', 
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'fi': 'Finnish',
    'fr': 'French',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ms': 'Malay',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'tr': 'Turkish',
    'zh': 'Chinese'
}

# Global model instances
english_model = None
multilingual_model = None

def load_english_model():
    global english_model
    if english_model is None:
        print("Loading Chatterbox English TTS model...")
        try:
            english_model = ChatterboxTTS.from_pretrained(DEVICE)
        except RuntimeError as e:
            if "CUDA device" in str(e) and not torch.cuda.is_available():
                print("CUDA not available, falling back to CPU...")
                english_model = ChatterboxTTS.from_pretrained("cpu")
            else:
                raise e
        print("English model loaded successfully!")
    return english_model

def load_multilingual_model():
    global multilingual_model
    if multilingual_model is None:
        print("Loading Chatterbox Multilingual TTS model...")
        try:
            multilingual_model = ChatterboxMultilingualTTS.from_pretrained(DEVICE)
        except RuntimeError as e:
            if "CUDA device" in str(e) and not torch.cuda.is_available():
                print("CUDA not available, falling back to CPU...")
                multilingual_model = ChatterboxMultilingualTTS.from_pretrained("cpu")
            else:
                raise e
        print("Multilingual model loaded successfully!")
    return multilingual_model

@app.route('/')
def index():
    return render_template('index.html', supported_languages=SUPPORTED_LANGUAGES)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "device": DEVICE,
        "chatterbox_available": True,
        "supported_languages": SUPPORTED_LANGUAGES
    })

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/generate', methods=['POST'])
def generate_tts():
    try:
        
        # Check if all required fields are present
        if 'audio' not in request.files or 'text' not in request.form:
            return jsonify({"error": "Audio file and text are required"}), 400
        
        audio_file = request.files['audio']
        text = request.form['text']
        language = request.form.get('language', 'en')
        exaggeration = float(request.form.get('exaggeration', 0.5))
        temperature = float(request.form.get('temperature', 0.8))
        
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400
        
        if not text.strip():
            return jsonify({"error": "Text is required"}), 400
        
        # Save audio file temporarily
        filename = secure_filename(audio_file.filename)
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(audio_path)
        
        # Load appropriate model based on language
        if language == 'en':
            model = load_english_model()
            wav = model.generate(
                text=text,
                audio_prompt_path=audio_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=0.5,
                min_p=0.05,
                top_p=1.0,
                repetition_penalty=1.2
            )
        else:
            model = load_multilingual_model()
            wav = model.generate(
                text=text,
                language_id=language,
                audio_prompt_path=audio_path,
                exaggeration=exaggeration,
                temperature=temperature,
                cfg_weight=0.5,
                min_p=0.05,
                top_p=1.0,
                repetition_penalty=1.2
            )
        
        # Convert to bytes
        import io
        import torchaudio
        
        buffer = io.BytesIO()
        torchaudio.save(buffer, wav, model.sr, format='wav')
        buffer.seek(0)
        
        # Clean up temporary file
        os.remove(audio_path)
        
        return send_file(
            buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='chatterbox_tts.wav'
        )
        
    except Exception as e:
        print(f"Error generating TTS: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Voice TTS Web App...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)