import os
import openai
import faiss
import numpy as np
import sounddevice as sd
import soundfile as sf
import pyaudio
import wave
from dotenv import load_dotenv
from datetime import datetime
import warnings

# Load environment variables from .env file
load_dotenv()
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

dimension = 1536  # Dimension of the OpenAI embeddings
index = faiss.IndexFlatL2(dimension)
embedding_metadata = []

def list_audio_devices():
    p = pyaudio.PyAudio()
    devices = [(i, p.get_device_info_by_index(i)['name']) for i in range(p.get_device_count())]
    p.terminate()
    return devices

def get_device_index_by_name(name):
    for index, device_name in list_audio_devices():
        if name.lower() in device_name.lower():
            return index
    return None

def get_audio(device_name, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000, silence_threshold=1000, silence_duration=5):
    device_index = get_device_index_by_name(device_name)
    if device_index is None:
        raise ValueError(f"Device '{device_name}' not found.")

    audio_frames = []
    silent_chunks = 0
    max_silent_chunks = int(rate / chunk_size * silence_duration)

    def is_silent(data):
        return np.max(np.abs(data)) < silence_threshold

    def callback(in_data, frame_count, time_info, status):
        nonlocal silent_chunks, audio_frames
        audio_frames.append(in_data)
        if is_silent(np.frombuffer(in_data, dtype=np.int16)):
            silent_chunks += 1
        else:
            silent_chunks = 0
        if silent_chunks > max_silent_chunks:
            return (None, pyaudio.paComplete)
        return (in_data, pyaudio.paContinue)

    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size, stream_callback=callback, input_device_index=device_index)
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
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(audio_frames))
    return output_filename

def play_audio(file_path):
    data, fs = sf.read(file_path, dtype='float32')
    sd.play(data, fs)
    sd.wait()

def speech_to_text():
    audio_file = get_audio(device)
    warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
    print('Processing speech...')
    with open(audio_file, "rb") as audio:
        transcription = openai.Audio.transcriptions.create(model="whisper-1", file=audio, response_format="text")
    return transcription.get("text", "")

def text_to_speech(text):
    response = openai.Audio.speech.create(model="tts-1", voice="onyx", input=text)
    response_path = os.path.join(os.getcwd(), 'audios', 'response_voice.mp3')
    response.stream_to_file(response_path)
    play_audio(response_path)

def write_to_file(text):
    delimiter = '-' * 20
    input_text = f'{delimiter}\nTimestamp: {datetime.now()}\n{text}\n{delimiter}'
    with open('context.txt', 'a') as file:
        file.write(input_text)

def embed_text(text):
    response = openai.Embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

def load_vector_store():
    if not os.path.exists('context.txt'):
        return
    with open('context.txt', 'r') as file:
        content = file.read()
    chunks = content.split('-' * 20)
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        index.add(np.array([embedding], dtype='float32'))
        embedding_metadata.append({'id': f'doc-{i}', 'text': chunk})

def update_vector_store(new_text):
    chunks = new_text.split('-' * 20)
    for chunk in chunks:
        embedding = embed_text(chunk)
        index.add(np.array([embedding], dtype='float32'))
        embedding_metadata.append({'id': f'doc-{len(embedding_metadata)}', 'text': chunk})

def query_vector_store(query, top_k=50):
    query_embedding = embed_text(query)
    distances, indices = index.search(np.array([query_embedding], dtype='float32'), top_k)
    return [embedding_metadata[idx] for idx in indices[0]]

def generate_response(query):
    matches = query_vector_store(query)
    context = " ".join([match['text'] for match in matches])
    response = openai.Chat.completions.create(model='gpt-4o-mini', messages=[
        {"role": "system", "content": "Your name is Memoro and you are a memory assistant listening to my conversations."},
        {"role": "user", "content": context},
        {"role": "user", "content": query}
    ])
    answer = response.choices[0].message.content
    write_to_file(answer)
    text_to_speech(answer)

def get_query():
    query = speech_to_text()
    write_to_file(query)
    return query

def intro():
    play_audio(os.path.join(os.getcwd(), 'audios', 'intro_prompt_voice.mp3'))

print('Loading vector store...')
load_vector_store()
print('Booted')
intro()

device_list = list_audio_devices()
for i, name in device_list:
    print(name)

device = input('Choose a microphone device from the list: ')
while device not in [name for _, name in device_list]:
    device = input('Choose a valid device: ')

while True:
    try:
        query = get_query()
        update_vector_store(query)
        generate_response(query)
    except KeyboardInterrupt:
        break
