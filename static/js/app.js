// Chatterbox Voice TTS App JavaScript

class VoiceTTSApp {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.recordedBlob = null;
        this.isRecording = false;
        this.recordingStartTime = null;
        this.recordingTimer = null;
        this.recordingInterval = null;
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupAudioRecording();
    }

    initializeElements() {
        // Recording elements
        this.recordBtn = document.getElementById('recordBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.recordedAudio = document.getElementById('recordedAudio');
        this.audioFile = document.getElementById('audioFile');
        this.recordingStatus = document.getElementById('recordingStatus');
        this.recordingTimer = document.getElementById('recordingTimer');

        // Text input elements
        this.textInput = document.getElementById('textInput');
        this.charCount = document.getElementById('charCount');

        // Control elements
        this.exaggeration = document.getElementById('exaggeration');
        this.exaggerationValue = document.getElementById('exaggerationValue');
        this.temperature = document.getElementById('temperature');
        this.temperatureValue = document.getElementById('temperatureValue');
        this.resetBtn = document.getElementById('resetBtn');

        // Generation elements
        this.generateBtn = document.getElementById('generateBtn');
        this.generationStatus = document.getElementById('generationStatus');

        // Output elements
        this.outputAudio = document.getElementById('outputAudio');
        this.downloadBtn = document.getElementById('downloadBtn');
    }

    setupEventListeners() {
        // Recording events
        this.recordBtn.addEventListener('click', () => this.startRecording());
        this.stopBtn.addEventListener('click', () => this.stopRecording());
        this.audioFile.addEventListener('change', (e) => this.handleFileUpload(e));

        // Text input events
        this.textInput.addEventListener('input', () => this.updateCharCount());
        this.textInput.addEventListener('input', () => this.updateGenerateButton());

        // Control events
        this.exaggeration.addEventListener('input', () => this.updateExaggerationValue());
        this.temperature.addEventListener('input', () => this.updateTemperatureValue());
        this.resetBtn.addEventListener('click', () => this.resetSettings());

        // Generation events
        this.generateBtn.addEventListener('click', () => this.generateTTS());
        this.downloadBtn.addEventListener('click', () => this.downloadAudio());
    }

    async setupAudioRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            
            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.recordedBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.audioChunks = [];
                this.displayRecordedAudio();
            };

            this.showStatus('recordingStatus', 'Microphone access granted!', 'success');
        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.showStatus('recordingStatus', 'Error accessing microphone. Please check permissions.', 'error');
            this.recordBtn.disabled = true;
        }
    }

    startRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'inactive') {
            this.audioChunks = [];
            this.mediaRecorder.start();
            this.isRecording = true;
            this.recordingStartTime = Date.now();
            
            this.recordBtn.disabled = true;
            this.stopBtn.disabled = false;
            this.generateBtn.disabled = true;
            
            this.recordBtn.classList.add('recording');
            this.showStatus('recordingStatus', 'Recording... Speak now!', 'recording');
            
            this.startRecordingTimer();
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
            this.mediaRecorder.stop();
            this.isRecording = false;
            
            this.recordBtn.disabled = false;
            this.stopBtn.disabled = true;
            
            this.recordBtn.classList.remove('recording');
            this.showStatus('recordingStatus', 'Recording stopped!', 'success');
            
            this.stopRecordingTimer();
            this.updateGenerateButton();
        }
    }

    startRecordingTimer() {
        this.recordingInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.recordingStartTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            this.recordingTimer.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }

    stopRecordingTimer() {
        if (this.recordingInterval) {
            clearInterval(this.recordingInterval);
            this.recordingInterval = null;
        }
    }

    displayRecordedAudio() {
        const audioUrl = URL.createObjectURL(this.recordedBlob);
        this.recordedAudio.src = audioUrl;
        this.recordedAudio.style.display = 'block';
        
        this.showStatus('recordingStatus', 'Recording ready! You can now generate TTS.', 'success');
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
            if (file.type.startsWith('audio/')) {
                this.recordedBlob = file;
                const audioUrl = URL.createObjectURL(file);
                this.recordedAudio.src = audioUrl;
                this.recordedAudio.style.display = 'block';
                
                this.showStatus('recordingStatus', 'Audio file loaded!', 'success');
                this.updateGenerateButton();
            } else {
                this.showStatus('recordingStatus', 'Please select a valid audio file.', 'error');
            }
        }
    }

    updateCharCount() {
        const count = this.textInput.value.length;
        this.charCount.textContent = count;
        
        if (count > 250) {
            this.charCount.parentElement.classList.add('warning');
        } else {
            this.charCount.parentElement.classList.remove('warning');
        }
        
        this.updateGenerateButton();
    }

    updateExaggerationValue() {
        this.exaggerationValue.textContent = this.exaggeration.value;
    }

    updateTemperatureValue() {
        this.temperatureValue.textContent = this.temperature.value;
    }

    resetSettings() {
        this.exaggeration.value = 0.5;
        this.temperature.value = 0.8;
        this.updateExaggerationValue();
        this.updateTemperatureValue();
    }

    updateGenerateButton() {
        const hasAudio = this.recordedBlob !== null;
        const hasText = this.textInput.value.trim().length > 0;
        
        this.generateBtn.disabled = !(hasAudio && hasText);
    }

    async generateTTS() {
        if (!this.recordedBlob || !this.textInput.value.trim()) {
            this.showStatus('generationStatus', 'Please record audio and enter text first.', 'error');
            return;
        }

        this.generateBtn.disabled = true;
        this.showStatus('generationStatus', '<div class="loading"></div> Generating TTS...', 'info');

        try {
            const formData = new FormData();
            formData.append('audio', this.recordedBlob);
            formData.append('text', this.textInput.value);
            formData.append('exaggeration', this.exaggeration.value);
            formData.append('temperature', this.temperature.value);

            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Generation failed');
            }

            const blob = await response.blob();
            const audioUrl = URL.createObjectURL(blob);
            
            this.outputAudio.src = audioUrl;
            this.outputAudio.style.display = 'block';
            this.downloadBtn.style.display = 'inline-block';
            
            this.showStatus('generationStatus', 'TTS generated successfully!', 'success');
        } catch (error) {
            console.error('Error generating TTS:', error);
            this.showStatus('generationStatus', `Error: ${error.message}`, 'error');
        } finally {
            this.generateBtn.disabled = false;
            this.updateGenerateButton();
        }
    }

    downloadAudio() {
        if (this.outputAudio.src) {
            const a = document.createElement('a');
            a.href = this.outputAudio.src;
            a.download = 'chatterbox_tts.wav';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    }

    showStatus(elementId, message, type) {
        const statusElement = document.getElementById(elementId);
        statusElement.innerHTML = message;
        statusElement.className = `status ${type}`;
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VoiceTTSApp();
});