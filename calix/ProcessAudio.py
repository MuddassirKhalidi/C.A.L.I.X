import os
import openai
from pydub import AudioSegment
import warnings
import shutil

class process_audio:
    def __init__(self):
        self.chunk_length_ms = 240000
        self.audio_dir = os.path.join('calix', 'audios', 'recorded_speech.wav') 
    
    def transcribe(self):
        chunks = self.split_audio()
        warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
        audio_files = self.save_chunks(chunks)
        full_text = ''
        for audio_file in audio_files:
            with open(audio_file, 'rb') as file:
                transcription = openai.audio.transcriptions.create(
                    model="whisper-1", 
                    file=file,
                    response_format="text",
                    language='en'
                )
            full_text += transcription
        shutil.rmtree(os.path.join('calix', 'audios', 'recorded_speech'))
        return full_text
    
    def save_chunks(self, chunks):
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_filename = os.path.join('calix', 'audios', 'recorded_speech', f"speech_part{i}.mp3")
            chunk.export(chunk_filename, format="mp3")
            chunk_files.append(chunk_filename)
        return chunk_files

    def split_audio(self):
        audio = AudioSegment.from_file(self.audio_dir)
        chunks = [audio[i:i+self.chunk_length_ms] for i in range(0, len(audio), self.chunk_length_ms)]
        print(f'Audio split into {len(chunks)} chunks')
        return chunks

