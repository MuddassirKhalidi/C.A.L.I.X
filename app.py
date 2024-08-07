from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
import pyaudio
import wave
import warnings
from datetime import datetime
import soundfile as sf
import sounddevice as sd

app = Flask(__name__)
CORS(app)

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

dimension = 1536  # Dimension of the OpenAI embeddings
index = faiss.IndexFlatL2(dimension)
embedding_metadata = []

def list_audio_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        devices.append((i, device_info['name']))
    p.terminate()
    return devices

def get_device_index_by_name(name):
    devices = list_audio_devices()
    for index, device_name in devices:
        if name.lower() in device_name.lower():
            return index
    return None

def getAudio(device_name, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000, silence_threshold=1000, silence_duration=5):
    device_index = get_device_index_by_name(device_name)
    if device_index is None:
        raise ValueError(f"Device '{device_name}' not found.")

    audio_frames = []
    silent_chunks = 0
    max_silent_chunks = int(rate / chunk_size * silence_duration)

    def is_silent(data, threshold=silence_threshold):
        max_amplitude = np.max(np.abs(data))
        return max_amplitude < threshold

    def callback(in_data, frame_count, time_info, status):
        nonlocal silent_chunks, audio_frames
        audio_frames.append(in_data)
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        if is_silent(audio_data):
            silent_chunks += 1
        else:
            silent_chunks = 0
        if silent_chunks > max_silent_chunks:
            return (None, pyaudio.paComplete)
        return (in_data, pyaudio.paContinue)

    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk_size,
                        stream_callback=callback,
                        input_device_index=device_index)

        print("Please start speaking. Recording...")
        stream.start_stream()

        while stream.is_active():
            pass

        stream.stop_stream()
        stream.close()

    except KeyboardInterrupt:
        print("Recording interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        p.terminate()

    output_filename = os.path.join(os.getcwd(), 'audios', 'recorded_speech.wav')
    try:
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(audio_frames))
    except Exception as e:
        print(f"Failed to save audio file: {e}")

    return output_filename

def play_audio(file_path):
    data, fs = sf.read(file_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()

def speech_to_text():
    getAudio(device_name=device)
    audio_file = os.path.join(os.getcwd(), 'audios', 'recorded_speech.wav')

    warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")

    print('Processing speech...')
    audio = open(audio_file, "rb")
    transcription = openai.Audio.transcriptions.create(
        model="whisper-1",
        file=audio,
        response_format="text"
    )
    print(transcription)
    return transcription

def text_to_speech(text):
    response = openai.Audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response_path = os.path.join(os.getcwd(), 'audios', 'response_voice.mp3')
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response.stream_to_file(response_path)
    play_audio(response_path)

def write_to_file(text):
    delimiter = '-' * 20
    input_text = f'{delimiter}\nTimestamp: {datetime.now()}\n{text}\n{delimiter}'
    with open('context.txt', 'a') as file:
        file.write(input_text)
    return

def embed_text(text):
    response = openai.Embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def load_vector_store():
    with open('context.txt', 'r') as file:
        content = file.read()

    chunks = content.split('-' * 20)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        embedding_np = np.array(embedding).astype('float32')
        index.add(np.array([embedding_np]))
        embedding_metadata.append({'id': f'doc-{i}', 'text': chunk})

def update_vector_store(new_text):
    chunks = new_text.split('-' * 20)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        embedding_np = np.array(embedding).astype('float32')
        index.add(np.array([embedding_np]))
        embedding_metadata.append({'id': f'doc-{len(embedding_metadata)}', 'text': chunk})

def query_vector_store(query, top_k=50):
    query_embedding = embed_text(query)
    query_embedding_np = np.array([query_embedding]).astype('float32')
    distances, indices = index.search(query_embedding_np, top_k)
    return [embedding_metadata[idx] for idx in indices[0]]

def generate_response(query):
    matches = query_vector_store(query)
    context = " ".join([match['text'] for match in matches])
    print(context)
    response = openai.Chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content": "Your name is Memoro and you are a memory assistant listening to my conversations."},
            {"role": "user", "content": context},
            {"role": "user", "content": query}
        ]
    )
    answer = response.choices[0].message.content
    write_to_file(answer)
    print(answer)
    text_to_speech(answer)

def get_query():
    query = speech_to_text()
    print('Speech to text done')
    write_to_file(query)
    return query

@app.route('/start-recording', methods=['POST'])
def start_recording():
    device = request.json['device']
    getAudio(device)
    return jsonify({"message": "Recording started"}), 200

@app.route('/ask-question', methods=['POST'])
def ask_question():
    query = get_query()
    update_vector_store(query)
    generate_response(query)
    return send_file(os.path.join(os.getcwd(), 'audios', 'response_voice.mp3'), mimetype='audio/mp3')

if __name__ == '__main__':
    print('Loading vector store..')
    load_vector_store()
    print('Booted')
    app.run(debug=True)
