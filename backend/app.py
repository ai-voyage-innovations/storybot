from flask import Flask, request, send_file, send_from_directory
import whisper
from TTS.api import TTS
import tempfile
import subprocess
import os
import time
import uuid
from Logger import AppLogger

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Load Whisper and TTS once
whisper_model = whisper.load_model("small.en")

# tts_engine = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
tts_engine = TTS(model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    logger = AppLogger("AudioProcessing", id=str(uuid.uuid4()))
    try:
        start_time = time.time()
        audio_file = request.files['audio']
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as webm_temp:
            audio_file.save(webm_temp.name)
            step1 = time.time()
            logger.info(f"Audio saved: {step1 - start_time:.2f}s")

            wav_path = convert_webm_to_wav(webm_temp.name)
            step2 = time.time()
            logger.info(f"WebM to WAV: {step2 - step1:.2f}s")

            text = transcribe_audio(wav_path)
            step3 = time.time()
            logger.info(f"Transcription: {step3 - step2:.2f}s")

            response = generate_response(text)
            step4 = time.time()
            logger.info(f"Response generation: {step4 - step3:.2f}s")

            mp3_path = synthesize_speech(response)
            step5 = time.time()
            logger.info(f"Speech synthesis: {step5 - step4:.2f}s")

            logger.info(f"TOTAL PROCESSING TIME: {step5 - start_time:.2f}s")

            return send_file(mp3_path, mimetype='audio/mpeg')
    except Exception as e:
        logger.error("ERROR PROCESSING INPUT: %s", str(e))
        return str(e), 500

def convert_webm_to_wav(input_path):    
    output_path = tempfile.mktemp(suffix=".wav")
    subprocess.run(['ffmpeg', '-y', '-i', input_path, output_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

def transcribe_audio(audio_path):
    # result = whisper_model.transcribe(audio_path)
    result = whisper_model.transcribe(audio_path, beam_size=1, fp16=False, language='en')
    return result['text']

def generate_response(text):
    return f"You said: {text}"

def synthesize_speech(text):
    output_path = tempfile.mktemp(suffix=".wav")
    tts_engine.tts_to_file(text=text, file_path=output_path)
    return output_path

if __name__ == '__main__':
    app.run(debug=True)