from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import warnings
from datetime import date
import json
from Audio_Recorder import AudioRecorder

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join('memoro-ii', '.env'))
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
dimension = 1536  # Dimension of the OpenAI embeddings
embedding_metadata = []

@app.route('/listen', methods=['GET'])
def listen():
    app.logger.info("Listen endpoint hit")
    recorder.start_recording()
    return jsonify({'message': 'Recording started'})

@app.route('/stop_listening', methods=['GET'])
def stop_listening():
    app.logger.info("Stop Listening endpoint hit")
    recorder.stop_recording()
    return jsonify({'message': 'Recording stopped'})


@app.route('/generate_response', methods=['GET'])
def generate_response_route():
    recorder.stop_recording()
    query = get_query()
    response = generate_response(query)
    return jsonify({'response': response})

def embed_text(text):
    response = openai.embeddings.create(
        input=text, 
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def write_to_file(text):
    with open(os.path.join('memoro-ii', 'store', 'context.txt'), 'a') as file:
        file.write(text)
    return 

def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response_path = os.path.join('memoro-ii','audios', 'response_voice.mp3')  # Contains the audio you hear when Memoro responds
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response.stream_to_file(response_path)
    play_audio(response_path)

def play_audio(file_path):
    data, fs = sf.read(file_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()  # Wait until file is done playing

def speech_to_text():
    warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
    with open(os.path.join('memoro-ii', 'audios', 'recorded_speech.wav'), "rb") as audio:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio,
            response_format="text",
            language='en'
        )
    print(transcription)
    return transcription

def load_vector_store(index):
    with open(os.path.join('memoro-ii','store','context.txt'), 'r') as file:
        chunks = file.read().split('-'*20)  # Split by lines for simplicity; can use more sophisticated chunking
    
    embeddings = []
    for chunk in chunks:

        embedding = embed_text(chunk)
        embeddings.append(embedding)
    
    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)
    for i, chunk in enumerate(chunks):
        embedding_metadata.append({'id': f'doc-{i}', 'text': chunk})

def save_embedding_metadata():
    with open(os.path.join('memoro-ii','store','embedding_metadata.json'), 'w') as f:
        json.dump(embedding_metadata, f)

def load_embedding_metadata():
    global embedding_metadata
    with open(os.path.join('memoro-ii','store','embedding_metadata.json'), 'r') as f:
        embedding_metadata = json.load(f)

def update_vector_store(new_text):
    chunks = new_text.split('.')  # Split by lines for simplicity; can use more sophisticated chunking
    
    embeddings = []
    for chunk in chunks:
        embedding = embed_text(chunk)
        embeddings.append(embedding)
    
    embeddings_np = np.array(embeddings).astype('float32')
    index.add(embeddings_np)
    for i, chunk in enumerate(chunks):
        embedding_metadata.append({'id': f'doc-{len(embedding_metadata)}', 'text': chunk})
    save_embedding_metadata()

def query_vector_store(query, top_k=50):
    query_embedding = embed_text(query)
    query_embedding_np = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_embedding_np, top_k)
    return [embedding_metadata[idx] for idx in indices[0]]

def generate_response(query):
    matches = query_vector_store(query)
    context = " ".join([match['text'] for match in matches])
    response = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Act like Jarvis from Iron Man. Your name is AIDA and you are a memory assistant \
                 listening to my conversations. You are capable of listening to my conversations and \
                 responding to details of historical conversations. Your response should be in English."},
                {"role": "user", "content": context},
                {"role": "user", "content": query}
            ]
        )
    answer = response.choices[0].message.content
    to_write = f'{date.today()}\nMemoro: {answer}'
    update_vector_store(to_write)
    write_to_file(to_write)
    print(answer)
    text_to_speech(answer)  
    return answer

def get_query():
    query = speech_to_text()
    to_write = f'{date.today()}\nUser: {query}'
    update_vector_store(to_write)
    write_to_file(to_write)
    return query

def get_conversation():
    speech = speech_to_text()
    update_vector_store(speech)
    write_to_file(speech)

def intro():
    file_path = os.path.join('memoro-ii', 'audios','intro.mp3')
    play_audio(file_path)

def init_vector_store():
    vector_store = os.path.join('memoro-ii','store','memoro.faiss')
    metadata_file = os.path.join('memoro-ii','store','embedding_metadata.json')

    # Check if the FAISS index file exists
    if os.path.exists(vector_store):
        print("Index file exists.")
        # Load the index
        index = faiss.read_index(vector_store)
        load_embedding_metadata()
        print("Index loaded successfully.")
    else:
        print("Index file does not exist.")
        # Create a new index
        dimension = 1536  # Example dimension, adjust accordingly
        index = faiss.IndexFlatL2(dimension)
        print("New index created.")
        # Save the new index
        faiss.write_index(index, vector_store)
        print("New index saved.")
        
        # Initialize empty embedding metadata
        global embedding_metadata
        embedding_metadata = []
        with open(metadata_file, 'w') as f:
            json.dump(embedding_metadata, f)
        print("New embedding metadata file created.")

    return index, vector_store


recorder = AudioRecorder()
index, vector_store = init_vector_store()
app.run(debug=True)