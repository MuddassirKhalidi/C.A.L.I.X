import pyaudio
import wave
import numpy as np
import os

class AudioRecorder:
    def __init__(self, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000, silence_threshold=1000, silence_duration=5):
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        self.rate = rate
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.audio_frames = []
        self.silent_chunks = 0
        self.max_silent_chunks = int(rate / chunk_size * silence_duration)
        self.recording = False
        self.stream = None
        self.p = pyaudio.PyAudio()

    def is_silent(self, data):
        max_amplitude = np.max(np.abs(data))
        return max_amplitude < self.silence_threshold

    def callback(self, in_data, frame_count, time_info, status):
        if not self.recording:
            return (None, pyaudio.paComplete)
        self.audio_frames.append(in_data)
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        if self.is_silent(audio_data):
            self.silent_chunks += 1
        else:
            self.silent_chunks = 0
        if self.silent_chunks > self.max_silent_chunks:
            return (None, pyaudio.paComplete)
        return (in_data, pyaudio.paContinue)

    def start_recording(self):
        self.recording = True
        self.audio_frames = []
        self.silent_chunks = 0
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk_size,
                                  stream_callback=self.callback)
        print("Recording started...")
        self.stream.start_stream()

    def get_recorded_audio(self):
        output_filename = os.path.join('calix','audios','recorded_speech.wav')
        try:
            with wave.open(output_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.audio_frames))
        except Exception as e:
            print(f"Failed to save audio file: {e}")

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.get_recorded_audio()
        print("Recording stopped.")
