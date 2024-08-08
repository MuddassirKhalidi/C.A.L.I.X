import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import pyaudio
import wave
import warnings
from datetime import datetime
import json

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
dimension = 1536  # Dimension of the OpenAI embeddings
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

device_list = list_audio_devices()
devices = [name for i, name in device_list]
for name in devices:
    print(name)

device = input('Choose a microphone device from the list: ')
while device not in devices:
    device = input('Choose a valid device: ')

def embed_text(text):
    response = openai.embeddings.create(
        input=text, 
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def write_to_file(text):
    delimiter = '-'*20
    input_text = f'{delimiter}\nTimestamp: {datetime.now()}\n{text}\n{delimiter}'
    with open('context.txt', 'a') as file:
        file.write(input_text)
    return 

def text_to_speech(text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response_path = os.path.join(os.getcwd(), 'audios', 'response_voice.mp3')  # Contains the audio you hear when Memoro responds
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response.stream_to_file(response_path)
    play_audio(response_path)

def play_audio(file_path):
    data, fs = sf.read(file_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()  # Wait until file is done playing

def speech_to_text():
    getAudio()
    audio_file = os.path.join(os.getcwd(), 'audios', 'recorded_speech.wav')

    warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")

    print('Processing speech...')
    with open(audio_file, "rb") as audio:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio,
            response_format="text"
        )
    print(transcription)
    return transcription

def getAudio(device_name=device, chunk_size=1024, 
             format=pyaudio.paInt16, channels=1, rate=16000, silence_threshold=1000, silence_duration=5):
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

    output_filename = os.path.join(os.getcwd(), 'audios','recorded_speech.wav')
    try:
        with wave.open(output_filename, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)
            wf.writeframes(b''.join(audio_frames))
    except Exception as e:
        print(f"Failed to save audio file: {e}")

    return output_filename

def load_vector_store():
    with open('context.txt', 'r') as file:
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
    with open('embedding_metadata.json', 'w') as f:
        json.dump(embedding_metadata, f)

def load_embedding_metadata():
    global embedding_metadata
    if os.path.exists('embedding_metadata.json'):
        with open('embedding_metadata.json', 'r') as f:
            embedding_metadata = json.load(f)

def update_vector_store(new_text):
    chunks = new_text.split('-'*20)  # Split by lines for simplicity; can use more sophisticated chunking
    
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
            model='gpt-4',
            messages=[
                {"role": "system", "content": "Your name is Memoro and you are a memory assistant listening to my conversations. Your response should be in the same language as the question. If the context is in a different language, translate it to the language of the question."},
                {"role": "user", "content": context},
                {"role": "user", "content": query}
            ]
        )
    answer = response.choices[0].message.content
    update_vector_store(answer)
    write_to_file(answer)
    print(answer)
    text_to_speech(answer)  

def get_query():
    query = speech_to_text()
    write_to_file(query)
    return query

def listen():
    speech = speech_to_text()
    update_vector_store(speech)
    write_to_file(speech)
    return speech

def intro():
    file_path = os.path.join(os.getcwd(), 'audios','intro_prompt_voice.mp3')
    play_audio(file_path)


vector_store = 'memoro.faiss'
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
    print('Loading vector store...')
    load_vector_store()
    # Save the new index
    faiss.write_index(index, vector_store)
    print("New index saved.")

print('Booted')
intro()
while True:
    try:
        query = get_query()
        update_vector_store(query)
        generate_response(query)
    except KeyboardInterrupt:
        faiss.write_index(index, vector_store)
        break
