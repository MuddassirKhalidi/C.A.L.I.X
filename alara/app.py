from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from Audio_Recorder import AudioRecorder
from memory import VectorStore
from alara import ALARA

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join('.env'))

@app.route('/listen', methods=['GET'])
def listen():
    app.logger.info("Listen endpoint hit")
    recorder.start_recording()
    return jsonify({'message': 'Recording started'})

@app.route('/stop', methods=['GET'])
def stop_listening():
    app.logger.info("Stop Listening endpoint hit")
    recorder.stop_recording()
    aida.get_conversation()
    return jsonify({'message': 'Recording stopped'})

@app.route('/respond', methods=['GET'])
def generate_response_route():
    recorder.stop_recording()
    query = aida.get_query()
    response = aida.generate_response(query)
    return jsonify({'query': query, 'response': response, 'status': 'completed'})

recorder = AudioRecorder()
store = VectorStore()
aida = ALARA(store)

app.run(debug=True)