from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
from werkzeug.utils import secure_filename
import torch
from chatterbox.tts import ChatterboxTTS

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Device detection and model setup
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Running on device: {DEVICE}")

# Global model instance
model = None

def load_model():
    global model
    if model is None:
        print("Loading Chatterbox TTS model...")
        model = ChatterboxTTS.from_pretrained(DEVICE)
        print("Model loaded successfully!")
    return model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "device": DEVICE,
        "chatterbox_available": True
    })

@app.route('/generate', methods=['POST'])
def generate_tts():
    try:
        
        # Check if all required fields are present
        if 'audio' not in request.files or 'text' not in request.form:
            return jsonify({"error": "Audio file and text are required"}), 400
        
        audio_file = request.files['audio']
        text = request.form['text']
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
        
        # Load model if not already loaded
        model = load_model()
        
        # Generate TTS
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