from flask import Flask, request, send_file, send_from_directory
import whisper
from TTS.api import TTS
import tempfile
import subprocess
import os
import time

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Load Whisper and TTS once
whisper_model = whisper.load_model("base")
tts_engine = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
        start_time = time.time()
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as webm_temp:
            audio_file.save(webm_temp.name)
            step1 = time.time()
            print(f"[LOG] Audio saved: {step1 - start_time:.2f}s")

            wav_path = convert_webm_to_wav(webm_temp.name)
            step2 = time.time()
            print(f"[LOG] WebM to WAV: {step2 - step1:.2f}s")

            text = transcribe_audio(wav_path)
            step3 = time.time()
            print(f"[LOG] Transcription: {step3 - step2:.2f}s")

            response = generate_response(text)
            step4 = time.time()
            print(f"[LOG] Response generation: {step4 - step3:.2f}s")

            mp3_path = synthesize_speech(response)
            step5 = time.time()
            print(f"[LOG] Speech synthesis: {step5 - step4:.2f}s")

            print(f"[LOG] Total processing time: {step5 - start_time:.2f}s")

            return send_file(mp3_path, mimetype='audio/mpeg')
    except Exception as e:
        app.logger.error("Error processing audio: %s", str(e))
        return str(e), 500

def convert_webm_to_wav(input_path):
    # Add stopwatch
    
    output_path = tempfile.mktemp(suffix=".wav")
    subprocess.run(['ffmpeg', '-y', '-i', input_path, output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def transcribe_audio(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result['text']

def generate_response(text):
    return f"You said: {text}"

def synthesize_speech(text):
    output_path = tempfile.mktemp(suffix=".wav")
    tts_engine.tts_to_file(text=text, file_path=output_path)
    return output_path

if __name__ == '__main__':
    app.run(debug=True)