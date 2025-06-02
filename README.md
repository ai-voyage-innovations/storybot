#Storybot
A simple voice-based chatbot web app using Python and HTML.

## Features
- Voice input via browser
- Whisper-based speech-to-text
- Simple response generation
- Coqui TTS for voice reply

## Setup
```bash
git clone https://github.com/your-username/storybot
cd storybot
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Pushing changes
GIT_SSH_COMMAND='ssh -i /$GIT_HOME/my' git push origin main

## Run
```bash
python backend/app.py
```
Open `http://localhost:5000` in browser.

---
Uses [Whisper](https://github.com/openai/whisper) and [Coqui TTS](https://github.com/coqui-ai/TTS).


---

## ✨ Features

- 🎤 Voice input from the browser.
- 🔁 Audio is sent to the backend and transcribed.
- 💬 Backend generates a text response.
- 🗣️ Response is converted back to speech and returned to the browser.
- 🔊 Browser plays the chatbot's spoken reply.

---

## 💡 Tech Stack

### 📦 Frontend (Client)

- `HTML`, `CSS`, `JavaScript`
- `MediaRecorder API` – to capture microphone input.
- `Fetch API` – to send/receive audio.
- `Audio` – to play TTS response.

### 🧠 Backend (Python)

| Purpose                | Tool/Library                   | Description |
|------------------------|--------------------------------|-------------|
| Web server             | `Flask`                        | REST API for audio processing |
| Audio conversion       | `ffmpeg`                       | Converts `.webm` to `.wav` |
| Transcription (STT)    | `Whisper` / `faster-whisper`  | Converts speech to text |
| Response generation    | Rule-based or `OpenAI GPT`     | Generates reply text |
| Text-to-speech (TTS)   | `TTS` (`coqui-ai/TTS`)         | Converts text to speech |
| Temp file handling     | `tempfile`, `os`               | Manage intermediate files |

---

## 🔁 Audio Flow

```text
🎤 Mic Input (webm/ogg)
       ↓
[ Flask Server ]
       ↓
Convert to WAV (ffmpeg)
       ↓
Transcribe (Whisper)
       ↓
Generate Response (Text)
       ↓
TTS (→ wav or mp3)
       ↓
⬆ Send back audio to client
       ↓
🔊 Client plays response
