from flask import Flask, request, send_file
from gtts import gTTS  # For text-to-speech
import speech_recognition as sr  # For speech-to-text
import subprocess  # To run ffmpeg for audio conversion
import tempfile  # For temporary file handling
import os  # For file deletion
import pyttsx3  # For text-to-speech engine

app = Flask(__name__)

tts_engine = None

# Initialize once
def init_tts_engine():
    global tts_engine
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 150)
    voices = tts_engine.getProperty('voices')
    tts_engine.setProperty('voice', voices[0].id)  # Optional: choose a specific voice
    return tts_engine


@app.route('/')
def index():
    # Serve the frontend HTML page
    return open('index.html').read()

@app.route('/process_audio', methods=['POST'])
def process_audio():
    try:
            
        # Step 1: Receive the audio file sent from the browser (WebM format)
        audio = request.files['audio']
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as webm_file:
            audio.save(webm_file.name)  # Save WebM file to disk

        # Step 2: Convert WebM to MP3 using ffmpeg
        mp3_path = tempfile.mktemp(suffix='.mp3')  # Create path for converted MP3 file
        # subprocess.run([
        #     'ffmpeg', '-y', '-i', webm_file.name, mp3_path
        # ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Suppress ffmpeg output

        subprocess.run([
            'ffmpeg', '-y', '-i', webm_file.name,
            '-ac', '1',
            '-ar', '16000',
            '-f', 'wav',
            mp3_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


        # Step 3: Transcribe the MP3 audio using speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(mp3_path) as source:
            audio_data = recognizer.record(source)  # Load the audio file
            text = recognizer.recognize_google(audio_data)  # Transcribe to text
            print(f"Transcribed text: {text}")

        # Step 4: Convert transcribed text to speech using gTTS
        # response_tts = gTTS(f"You said: {text}")
        wav_path = tempfile.mktemp(suffix='.wav')  # Path for TTS audio response
        # response_tts.save(mp3_path)  # Save TTS audio to disk
        init_tts_engine()  # Ensure TTS engine is initialized
        tts_engine.save_to_file(f"You said: {text}", wav_path)
        tts_engine.runAndWait()
        print(f"Generated wav file: {wav_path}")
        # log wav file size
        print(f"WAV file size: {os.path.getsize(wav_path)} bytes")  

        # Step 5: Clean up temporary files
        # os.remove(webm_file.name)
        # os.remove(mp3_path)

        # Step 6: Send the generated audio (WAV) back to the browser
        print(f"Sending WAV file: {wav_path}")
        return send_file(wav_path, mimetype='audio/wav')
    except Exception as e:
        # log error with stack trace
        import traceback
        traceback.print_exc()
        print(f"Error processing audio: {e}")
        return "Error processing audio", 500

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)
