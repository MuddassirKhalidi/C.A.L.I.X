import openai
import os
import warnings
from datetime import datetime
import soundfile as sf
import sounddevice as sd
from ProcessAudio import ProcessAudio

class Calix:
    def __init__(self, vector_store):
        """
        Initialize Calix with a vector store for memory management.
        """
        self.vector_store = vector_store

    def write_to_file(self, text):
        """
        Write a given text to the context file.
        """
        try:
            with open(os.path.join('calix', 'store', 'context.txt'), 'a') as file:
                file.write(text + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")

    def speech_to_text(self):
        """
        Convert recorded speech audio to text using OpenAI's Whisper model.
        """
        try:
            warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
            with open(os.path.join('calix', 'audios', 'recorded_speech.wav'), "rb") as audio:
                transcription = openai.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio,
                    response_format="text",
                    language='en'
                )
            return transcription
        except Exception as e:
            print(f"Error during speech-to-text: {e}")
            return ""

    def text_to_speech(self, text):
        """
        Convert a given text to speech using OpenAI's text-to-speech API and play it.
        """
        try:
            response = openai.audio.speech.create(
                model="tts-1",
                voice="onyx",
                input=text
            )
            response_path = os.path.join('calix', 'audios', 'response_voice.mp3')
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            response.stream_to_file(response_path)
            self.play_audio(response_path)
        except Exception as e:
            print(f"Error during text-to-speech: {e}")

    def play_audio(self, file_path):
        """
        Play an audio file using sounddevice and soundfile.
        """
        try:
            data, fs = sf.read(file_path, dtype='float32')
            sd.play(data, fs)
            sd.wait()
        except Exception as e:
            print(f"Error playing audio: {e}")

    def generate_response(self, query):
        """
        Generate a response based on the input query, using the vector store to provide context.
        """
        try:
            matches = self.vector_store.query_vector_store(query)
            context = " ".join(set([match['text'] for match in matches]))
            
            response = openai.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {"role": "system", "content": "Your name is Calix, a memory assistant listening to conversations..."},
                    {"role": "user", "content": context},
                    {"role": "user", "content": query}
                ]
            )
            answer = response.choices[0].message.content
            to_write = f'Date: {datetime.now()}\nCalix: {answer}'
            self.vector_store.update_vector_store(to_write)
            self.write_to_file(to_write)
            print(answer)
            self.text_to_speech(answer)
            return answer
        except Exception as e:
            print(f"Error generating response: {e}")
            return ""

    def get_query(self):
        """
        Get a query by converting the recorded speech to text.
        """
        try:
            query = self.speech_to_text()
            to_write = f'Date: {datetime.now()}\nUser: {query}'
            self.vector_store.update_vector_store(to_write)
            self.write_to_file(to_write)
            return query
        except Exception as e:
            print(f"Error getting query: {e}")
            return ""

    def get_conversation(self):
        """
        Process and transcribe a recorded conversation.
        """
        try:
            speech = audio_processor.transcribe()
            to_write = f'Date: {datetime.now()}\n{speech}'
            self.vector_store.update_vector_store(to_write)
            self.write_to_file(to_write)
        except Exception as e:
            print(f"Error processing conversation: {e}")

    def intro(self):
        """
        Play an introductory audio file.
        """
        try:
            file_path = os.path.join('calix', 'audios', 'intro.mp3')
            self.play_audio(file_path)
        except Exception as e:
            print(f"Error playing intro: {e}")

# Initialize the audio processor
audio_processor = ProcessAudio()
