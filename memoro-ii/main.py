print('Booting...')
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
import pyaudio
import wave
import numpy as np
import whisper
import warnings
from datetime import datetime
import tiktoken
from transformers import pipeline


# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
classifier = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
tokenizer = tiktoken.get_encoding('cl100k_base')
print('Booted!')

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


def get_OPENAI_API():
    """
    Loads the OpenAI API key from the environment variables.

    Returns:
    - str: The OpenAI API key.
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("OpenAI API key is not set. Please set the 'OPENAI_API_KEY' environment variable in your .env file.")
    return openai.api_key

def is_positive(text, classifier):
    # # Preprocess text if necessary
    # processed_text = text  # Assuming no specific preprocessing is required

    # # Use Transformers pipeline for sentiment analysis
    # result = classifier(processed_text)

    # # Extract the sentiment label from the result
    # sentiment_label = result[0]['label']
    # if sentiment_label == 'NEGATIVE':
    #     return False
    # else:
    #     return True
    uncertain_phrases = [
    "I'm not sure",
    "I don't know",
    "I can't find",
    "I don't have enough information",
    "This may not be correct",
    "Sorry, I don't understand",
    "I'm unable to answer that",
    "I don't have the answer",
    "I don't have that information",
    "I couldn't find an answer",
    "I couldn't find what you're looking for",
    "I couldn't find the information you need",
    "I couldn't locate an answer",
    "I'm sorry, but I don't have an answer for that",
    "Unfortunately, I don't have the answer",
    "That's outside my knowledge base",
    "I don't have enough data to answer that",
    "I'm not equipped to answer that",
    "I can't provide an answer to that",
    "I'm not sure how to answer that",
    "I don't have the answer right now",
    "That's beyond my current capabilities",
    "I couldn't locate the answer",
    "I don't have access to that information",
    "I'm afraid I don't know",
    "I wish I could help, but I don't know",
    "I don't have an answer for you",
    "I'm still learning, and I don't have that answer",
    "I apologize, but I don't know the answer",
    "That's a great question, but I don't know",
    "I'm unable"
]
    for phrase in uncertain_phrases:
        if phrase in text:
            return False
    return True
    
    
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

    # Load the Whisper model
    model = whisper.load_model("base")  
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
    file_path = os.path.join(os.getcwd(), 'buffer', 'short_term_buffer.txt')
    with open(file_path, 'a') as file:
        file.write(text)
        
    return 

def read_from_file(file_path):
    """
    Reads text from a file.

    Args:
    - file_path (str): The path of the file.

    Returns:
    - str: The read text.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def get_context():
    text = speech_to_text()
    context = f'\n\nTimestamp: {str(datetime.now())}\nConversation:\n{text}'
    write_to_file(context)

def get_prompt():
    query = speech_to_text()
    prompt = f'\n\nTimestamp: {str(datetime.now())}\nQuestion: {query}'
    write_to_file(prompt)
    short_buffer = os.path.join(os.getcwd(), 'buffer', 'short_term_buffer.txt')
    long_buffer = os.path.join(os.getcwd(), 'buffer', 'long_term_buffer.txt')
    for file in [short_buffer, long_buffer]:
        context = read_from_file(file)
        response = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Your name is Memoro and you are a memory assistant listening to my conversations. You are given context with timestamps for the different conversations I have had. You will respond to queries from a short term buffer (this stores recent and immediate conversations) and a long term buffer (this stores past conversations). Answer the question using the provided context. If the query is something which requires you to search both buffers, or the long term buffer give a negative response. After you answer the question, ask for a follow up question."},
                {"role": "user", "content": context},
                {"role": "user", "content": prompt}

            ]
        )
        text = response.choices[0].message.content
        if is_positive(text, classifier):
            break
        text_to_speech('Searching long term buffer...')
            
#     response = text + '\nIs there anything else I can help you with?'
    text_to_speech(text)
    response = f'\nAnswer: {text}\n' + '-'*10
    write_to_file(response)
    print(text)

def buffer_exceeded():
    short_buffer = os.path.join(os.getcwd(), 'buffer', 'short_term_buffer.txt')
    text = read_from_file(short_buffer)
    # Define the tokenizer for GPT-4o-mini using cl100k_base encoding
    tokenizer = tiktoken.get_encoding('cl100k_base')

    # Encode the context and count the tokens
    tokens = tokenizer.encode(text)
    num_tokens = len(tokens)
    if num_tokens > 2000:
        return True
    else:
        return False
    
def move_to_long_term_buffer():
    # Read the entire content of the short term buffer file
    short_term_buffer = os.path.join(os.getcwd(), 'buffer', 'short_term_buffer.txt')
    long_term_buffer = os.path.join(os.getcwd(), 'buffer', 'long_term_buffer.txt')
    with open(short_term_buffer, 'r', encoding='utf-8') as file:
        text = file.read()

    # Tokenize the text
    tokens = tokenizer.encode(text)

    # Split the tokens into two parts
    first_n_tokens = tokens[:2000]
    remaining_tokens = tokens[2000:]

    # Decode the first 2000 tokens and remaining tokens back to text
    first_n_text = tokenizer.decode(first_n_tokens)
    remaining_text = tokenizer.decode(remaining_tokens)

    # Write the first n tokens to the new file
    with open(long_term_buffer, 'a', encoding='utf-8') as file:
        file.write(first_n_text)

    # Update the original file with the remaining tokens
    with open(short_term_buffer, 'w', encoding='utf-8') as file:
        file.write(remaining_text)
        
def intro():
    file_path = os.path.join(os.getcwd(), 'audios','intro_prompt_voice.mp3')
    play_audio(file_path)

# intro()

while True:
    print('Entered loop')
    if buffer_exceeded():
        move_to_long_term_buffer()
    
    try:
        choice = input('Enter 1 to record and 2 to retrieve memories: ')
        while choice not in ['1','2']:
            choice = input('Enter a valid choice [1,2]: ')
        if choice == '1':
            get_context()
        else:
            get_prompt()
        print('-'*50)
        print('Interrupt the kernel to end the program')
    except KeyboardInterrupt:
        print("Thank you!")
        break
print('Exited loop')