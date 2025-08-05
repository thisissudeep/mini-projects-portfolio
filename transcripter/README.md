# Real-Time Speech Transcriber

A simple real-time speech-to-text converter using Python and the `speech_recognition` library. This script captures your voice via microphone and prints the transcribed text on the console.

## How it works

- Captures microphone input in real-time.
- Uses Google Web Speech API for transcription.
- Continuously listens and prints recognized speech.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/speech-transcriber.git
cd speech-transcriber
```

### 2. Run the script:

```bash
python transcriber.py
```

You'll see:

```
------------------------------ Please Speak -----------------------------------
```

Start speaking clearly into the mic. The recognized speech will be printed in real-time.

---

## Output Example

```
------------------------------ Please Speak -----------------------------------
Hello, how are you?
I'm testing this speech recognition.
```

---
