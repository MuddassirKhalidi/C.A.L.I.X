import os
import openai
from pydub import AudioSegment
import warnings
import shutil

class ProcessAudio:
    def __init__(self):
        self.chunk_length_ms = 240000  # 4-minute chunks
        self.audio_dir = os.path.join('calix', 'audios', 'recorded_speech.wav') 
    
    def transcribe(self):
        """
        Transcribes an audio file by splitting it into chunks, processing each with OpenAI's Whisper API,
        and returning the full transcription text.
        """
        try:
            chunks = self.split_audio()
            warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
            
            audio_files = self.save_chunks(chunks)
            full_text = ''
            
            for audio_file in audio_files:
                with open(audio_file, 'rb') as file:
                    try:
                        transcription = openai.audio.transcriptions.create(
                            model="whisper-1", 
                            file=file,
                            response_format="text",
                            language='en'
                        )
                        full_text += transcription  # Append transcription result to the final text
                    except openai.error.OpenAIError as e:
                        print(f"Error during transcription: {e}")
                        continue  # Skip to the next chunk if there's an error
            
            # Clean up temporary files
            shutil.rmtree(os.path.join('calix', 'audios', 'recorded_speech'))
            return full_text

        except Exception as e:
            print(f"Error in transcription process: {e}")
            return ''
    
    def save_chunks(self, chunks):
        """
        Saves the audio chunks to temporary files and returns their paths.
        """
        chunk_files = []
        temp_dir = os.path.join('calix', 'audios', 'recorded_speech')
        
        # Create directory if it doesn't exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        for i, chunk in enumerate(chunks):
            chunk_filename = os.path.join(temp_dir, f"speech_part{i}.mp3")
            try:
                chunk.export(chunk_filename, format="mp3")
                chunk_files.append(chunk_filename)
            except Exception as e:
                print(f"Error saving chunk {i}: {e}")
                continue  # Continue saving the next chunk if there's an error
        
        return chunk_files

    def split_audio(self):
        """
        Splits the audio file into smaller chunks to avoid transcription timeouts.
        """
        try:
            audio = AudioSegment.from_file(self.audio_dir)
            chunks = [audio[i:i+self.chunk_length_ms] for i in range(0, len(audio), self.chunk_length_ms)]
            print(f'Audio split into {len(chunks)} chunks')
            return chunks
        except FileNotFoundError:
            print(f"Audio file not found at {self.audio_dir}")
            return []
        except Exception as e:
            print(f"Error splitting audio: {e}")
            return []
