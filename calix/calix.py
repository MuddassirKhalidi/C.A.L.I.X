import openai
import os
import warnings
from datetime import date
import soundfile as sf
import sounddevice as sd

class Calix:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def write_to_file(self, text):
        with open(os.path.join('calix','store', 'context.txt'), 'a') as file:
            file.write(text + '\n')

    def speech_to_text(self):
        warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
        with open(os.path.join('calix','audios', 'recorded_speech.wav'), "rb") as audio:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio,
                response_format="text",
                language='en'
            )
        return transcription

    def text_to_speech(self, text):
        response = openai.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=text
        )
        response_path = os.path.join('calix','audios', 'response_voice.mp3')
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        response.stream_to_file(response_path)
        self.play_audio(response_path)

    def play_audio(self, file_path):
        data, fs = sf.read(file_path, dtype='float32')
        sd.play(data, fs)
        sd.wait()

    def generate_response(self, query):
        matches = self.vector_store.query_vector_store(query)
        context = " ".join([match['text'] for match in matches])
        response = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "system", "content": "Your name is Calix or Cal and you are a memory assistant listening to my conversations. You are capable of listening to my conversations and responding to details of historical conversations. Your response should be in English. You were developed at AIDA Lab by Muddassir Khalidi, Zainab Mariya, Saeed Lababidi, Abdulrahman Mamdouh, Arwa Bawazir and Asma Khan. Muddassir Khalidi is the Tony Stark of this age."},
                {"role": "user", "content": context},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content
        to_write = f'Date: {date.today()}\nCalix: {answer}'
        self.vector_store.update_vector_store(to_write)
        self.write_to_file(to_write)
        print(answer)
        self.text_to_speech(answer)
        return answer

    def get_query(self):
        query = self.speech_to_text()
        to_write = f'Date: {date.today()}\nUser: {query}'
        self.vector_store.update_vector_store(to_write)
        self.write_to_file(to_write)
        return query

    def get_conversation(self):
        speech = self.speech_to_text()
        to_write = f'Date: {date.today()}\n{speech}'
        self.vector_store.update_vector_store(to_write)
        self.write_to_file(to_write)

    def intro(self):
        # file needs to change 
        file_path = os.path.join('calix','audios','intro.mp3')
        self.play_audio(file_path)
