from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Speech Recognition Flask App!'

@app.route('/recognize', methods=['POST'])
def recognize():
    recognizer = sr.Recognizer()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    audio_file = request.files['file']
    
    # Ensure the file is in audio format
    if audio_file and audio_file.filename.endswith('.wav'):
        audio = sr.AudioFile(audio_file)
        with audio as source:
            audio_data = recognizer.record(source)
        
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'error': 'Speech could not be recognized'})
        except sr.RequestError:
            return jsonify({'error': 'Could not request results from Google Speech Recognition service'})
    else:
        return jsonify({'error': 'Invalid file format. Please upload a WAV file.'})

if __name__ == "__main__":
    app.run(debug=True)
