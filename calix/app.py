from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from Audio_Recorder import AudioRecorder
from memory import VectorStore
from calix import Calix

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join('.env'))

# Initialize necessary components
recorder = AudioRecorder()
store = VectorStore()
calix = Calix(store)

@app.route('/listen', methods=['GET'])
def listen():
    """
    Endpoint to start recording audio using the AudioRecorder.
    Logs when the recording starts.
    Returns:
        A JSON message indicating the recording has started.
    """
    try:
        app.logger.info("Listen endpoint hit")
        recorder.start_recording()
        return jsonify({'message': 'Recording started'})
    except Exception as e:
        app.logger.error(f"Error starting recording: {e}")
        return jsonify({'error': 'Failed to start recording'}), 500


@app.route('/stop', methods=['GET'])
def stop_listening():
    """
    Endpoint to stop recording audio.
    After stopping the recording, the conversation is processed.
    Logs when the recording is stopped.
    Returns:
        A JSON message indicating the recording has been stopped and the process is completed.
    """
    try:
        app.logger.info("Stop Listening endpoint hit")
        recorder.stop_recording()
        calix.get_conversation()
        return jsonify({'message': 'Recording stopped', 'status': 'completed'})
    except Exception as e:
        app.logger.error(f"Error stopping recording or processing conversation: {e}")
        return jsonify({'error': 'Failed to stop recording and process conversation'}), 500


@app.route('/respond', methods=['GET'])
def generate_response_route():
    """
    Endpoint to generate a response based on the recorded conversation.
    Stops the recording if active, retrieves the query, and generates a response.
    Returns:
        A JSON object containing the query, response, and status.
    """
    try:
        recorder.stop_recording()  # Ensure the recording is stopped
        query = calix.get_query()  # Retrieve the query from the conversation
        response = calix.generate_response(query)  # Generate a response based on the query
        return jsonify({'query': query, 'response': response, 'status': 'completed'})
    except Exception as e:
        app.logger.error(f"Error generating response: {e}")
        return jsonify({'error': 'Failed to generate response'}), 500


# Run the Flask application
if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.error(f"Error running the Flask app: {e}")
