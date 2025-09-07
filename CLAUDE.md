# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Chatterbox is Resemble AI's open-source multilingual text-to-speech (TTS) and voice conversion system. It's a production-grade TTS model supporting 23 languages with zero-shot voice cloning capabilities and emotion exaggeration control. The model uses a 0.5B Llama backbone and is trained on 0.5M hours of cleaned data.

## Architecture

### Core Components

1. **Main TTS Models** (`src/chatterbox/`):
   - `tts.py` - English TTS model (`ChatterboxTTS`)
   - `mtl_tts.py` - Multilingual TTS model (`ChatterboxMultilingualTTS`)
   - `vc.py` - Voice conversion model (`ChatterboxVC`)

2. **Model Architecture** (`src/chatterbox/models/`):
   - `s3gen/` - Core S3Gen model with transformer-based architecture
   - `s3tokenizer/` - S3 tokenizer implementation
   - `t3/` - T3 model components
   - `voice_encoder/` - Voice encoding components
   - `tokenizers/` - Various tokenizer implementations

3. **S3Gen Model Structure**:
   - Flow matching and diffusion components
   - HiFi-GAN vocoder
   - Transformer-based text encoder
   - F0 prediction for prosody control

## Development Commands

### Installation
```bash
# Install from PyPI
pip install chatterbox-tts

# Install from source
git clone https://github.com/resemble-ai/chatterbox.git
cd chatterbox
pip install -e .
```

### Running Examples
```bash
# English TTS example
python example_tts.py

# Voice conversion example
python example_vc.py

# Gradio web interface
python gradio_tts_app.py
python gradio_vc_app.py
python multilingual_app.py
```

### Testing
```bash
# Run basic functionality tests
python example_tts.py
python example_vc.py
```

## Key Features

### Multilingual Support
- Supports 23 languages with language codes: ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh
- Zero-shot cross-lingual voice cloning
- Language-specific prosody and accent handling

### Generation Parameters
- `exaggeration` (0.0-1.0): Controls emotion intensity (default: 0.5)
- `cfg_weight` (0.0-1.0): Classifier-free guidance weight (default: 0.5)
- `audio_prompt_path`: Path to reference audio for voice cloning

### Audio Processing
- Built-in watermarking using Resemble's PerTh watermarker
- Sample rate: 24kHz
- Audio format: WAV files

## Model Usage Patterns

### Basic TTS Generation
```python
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device="cuda")
wav = model.generate("Your text here")
```

### Multilingual TTS
```python
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
wav = model.generate("Votre texte ici", language_id="fr")
```

### Voice Conversion
```python
from chatterbox.vc import ChatterboxVC
model = ChatterboxVC.from_pretrained(device="cuda")
wav = model.convert_voice(source_audio_path, target_audio_path)
```

## Dependencies and Environment

### Core Dependencies
- **PyTorch 2.6.0** - Deep learning framework
- **Torchaudio 2.6.0** - Audio processing
- **Transformers 4.46.3** - Hugging Face transformers
- **Librosa 0.11.0** - Audio analysis
- **Diffusers 0.29.0** - Diffusion models
- **Gradio 5.44.1** - Web interface

### Specialized Dependencies
- **s3tokenizer** - Custom S3 tokenizer
- **resemble-perth** - Audio watermarking
- **conformer** - Conformer architecture
- **pkuseg** - Chinese segmentation
- **pykakasi** - Japanese romanization

## Development Notes

### Code Structure
- Main entry points are in `tts.py`, `mtl_tts.py`, and `vc.py`
- Model architectures are in `src/chatterbox/models/`
- Examples show proper device selection (CUDA/MPS/CPU)
- All models use `from_pretrained()` pattern for loading

### Audio Processing
- Models expect 24kHz audio input/output
- Built-in watermarking is applied to all generated audio
- Voice cloning works with short audio clips (3-10 seconds)

### Performance Considerations
- Models are optimized for inference speed
- Default settings work well for most use cases
- Lower `cfg_weight` for faster speech, higher for more stable output