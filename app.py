from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Speech Recognition Flask App!'

@app.route('/recognize', methods=['POST'])
def recognize():
    recognizer = sr.Recognizer()
    audio_file = request.files['file']
    audio = sr.AudioFile(audio_file)
    with audio as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({'text': text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech not recognized'})
    except sr.RequestError:
        return jsonify({'error': 'API not available'})

if __name__ == "__main__":
    app.run(debug=True)
