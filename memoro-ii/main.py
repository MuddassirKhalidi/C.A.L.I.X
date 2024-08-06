print('Booting...')
import os
import openai
import faiss
import numpy as np
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import pyaudio
import wave
import numpy as np
import whisper
import warnings
from datetime import datetime
# import tiktoken
# from transformers import pipeline

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
dimension = 1536  # Dimension of the OpenAI embeddings
index = faiss.IndexFlatL2(dimension)
embedding_metadata = []

def list_audio_devices():
    """
    Lists all available audio input devices.

    Returns:
    - list: A list of tuples containing device index, name, max input channels, and default sample rate.
    """
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        devices.append((i, device_info['name']))
    p.terminate()
    return devices

def get_device_index_by_name(name): 
    """
    Finds the index of an audio device by its name.

    Args:
    - name (str): The name of the device.

    Returns:
    - int: The index of the device.
    
    Note: This is a helper function which will be used in getAudio().
    """
    devices = list_audio_devices()
    for index, device_name in devices:
        if name.lower() in device_name.lower():
            return index
    return None

device_list = list_audio_devices()
devices = []
for i, name in device_list:
    devices.append(name)
    print(name)
    
device = input('Choose a microphone device from the list: ')
while device not in devices:
    device = input('Choose a valid device: ')
    
def getAudio(device_name=device, chunk_size=1024, 
             format=pyaudio.paInt16, channels=1, rate=16000, silence_threshold=1000, silence_duration=5):
    """
    Records audio until a period of silence is detected and saves it to a file.

    Args:
    - output_filename (str): Name of the output WAV file.
    - device_name (str): Name of the input audio device.
    - chunk_size (int): Number of frames per buffer.
    - format: Audio format (e.g., pyaudio.paInt16).
    - channels (int): Number of audio channels.
    - rate (int): Sampling rate in Hz.
    - silence_threshold (int): Amplitude threshold for silence detection.
    - silence_duration (int): Duration of silence required to stop recording (in seconds).

    Returns:
    - str: The name of the saved audio file.
    
    Note: Start talking only when you see the message "Please start speaking. Recording..." 
    If your conversation/prompt is over, but Memoro continues to record, just interrupt it.
    """
    device_index = get_device_index_by_name(device_name)
    if device_index is None:
        raise ValueError(f"Device '{device_name}' not found.")

    # Variables to store audio frames and silence detection
    audio_frames = []
    silent_chunks = 0
    max_silent_chunks = int(rate / chunk_size * silence_duration)

    def is_silent(data, threshold=silence_threshold):
        """Returns 'True' if below the silence threshold."""
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

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    try:
        # Open stream
        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk_size,
                        stream_callback=callback,
                        input_device_index=device_index)

        print("Please start speaking. Recording...")
        stream.start_stream()

        # Keep the stream active while recording
        while stream.is_active():
            pass

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

    except KeyboardInterrupt: 
        # Handle keyboard interruption for noisy environments
        print("Recording interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        p.terminate()

    # Save the recorded audio to a file
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

def play_audio(file_path):
    """
    Plays an audio file.

    Args:
    - file_path (str): The path of the audio file.
    """
    # Play the sound file
    # Load the sound file
    data, fs = sf.read(file_path, dtype='float32')

    # Play the sound file
    sd.play(data, fs)
    sd.wait()  # Wait until file is done playing
    
def speech_to_text():
    """
    Converts recorded audio to text using Whisper model.

    Returns:
    - str: The transcribed text.
    """
    audio = getAudio()

    # Suppress the FP16 warning
    warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")

    try:
        # Load the Whisper model
        print('Loading whisper model...')
        model = whisper.load_model('tiny')
        print('Whisper model loaded successfully.')
    except Exception as e:
        print(f"Failed to load Whisper model: {e}")
        return ""
    '''
    Choose among tiny, base, small, medium, large models
    The higher the model, higher the accuracy. But more accuracy means 
    it will take a lot longer to transcribe the audio.
    '''

    print('Processing speech...')
    # Transcribe the audio file
    result = model.transcribe(audio)
    print('Transcribed!')
    text = result['text']
    print(text)
    return text

def text_to_speech(text):
    """
    Converts text to speech and plays the audio.

    Args:
    - text (str): The text to be converted to speech.
    """
    response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=text
    )
    response_path = os.path.join(os.getcwd(), 'audios', 'response_voice.mp3')  # Contains the audio you hear when Memoro responds
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response.stream_to_file(response_path)
    play_audio(response_path)

def write_to_file(text):
    """
    Writes the text to a file.

    Args:
    - text (str): The text to be written.

    Returns:
    - str: The file path.
    """
    delimiter = '-'*20
    input_text = f'{delimiter}\nTimestamp: {datetime.now()}\n{text}\n{delimiter}'
    with open('test.txt', 'a') as file:
        file.write(input_text)
    return 

def embed_text(text):
    response = openai.embeddings.create(
        input=text, 
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def load_vector_store():
    with open('test.txt', 'r') as file:
        content = file.read()
    
    # Split content into smaller chunks if necessary
    chunks = content.split('-'*20)  # Split by lines for simplicity; can use more sophisticated chunking
    
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        embedding_np = np.array(embedding).astype('float32')
        index.add(np.array([embedding_np]))
        embedding_metadata.append({'id': f'doc-{i}', 'text': chunk})

def update_vector_store(new_text):
    # Split new text into smaller chunks if necessary
    chunks = new_text.split('-'*20)  # Split by lines for simplicity; can use more sophisticated chunking
    
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        embedding_np = np.array(embedding).astype('float32')
        index.add(np.array([embedding_np]))
        embedding_metadata.append({'id': f'doc-{len(embedding_metadata)}', 'text': chunk})

def query_vector_store(query, top_k=10):
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
    # query = input('Enter your query: ')
    print('Speech to text done')
    write_to_file(query)
    return query

def listen():
    speech = speech_to_text()
    write_to_file(speech)
    return speech

def intro():
    file_path = os.path.join(os.getcwd(), 'audios','intro_prompt_voice.mp3')
    play_audio(file_path)

intro()
print('Loading vector store..')
load_vector_store()
print('Booted')
while True:
    
    try:
        query = get_query()
        update_vector_store(query)
        generate_response(query)
    except KeyboardInterrupt:
        break

# while True:
    
#     try:
#         choice = int(input('Enter 1 for listen() and 2 for get_query(): '))
#         if choice == 1:
#             conversation = listen()
#             update_vector_store(conversation)
#         else:
#             query = get_query()
#             update_vector_store(query)
#     except KeyboardInterrupt:
#         break


