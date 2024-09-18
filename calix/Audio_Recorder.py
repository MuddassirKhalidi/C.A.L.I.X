import pyaudio
import wave
import os

class AudioRecorder:
    def __init__(self, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=16000):
        """
        Initialize the audio recorder with parameters for chunk size, format, channels, and rate.
        """
        self.chunk_size = chunk_size  # Size of each audio chunk
        self.format = format  # Audio format (e.g., 16-bit audio)
        self.channels = channels  # Number of audio channels (1 for mono)
        self.rate = rate  # Sampling rate in Hz
        self.audio_frames = []  # List to store recorded audio frames
        self.recording = False  # Recording status flag
        self.stream = None  # PyAudio stream object
        self.p = pyaudio.PyAudio()  # Initialize PyAudio instance

    def callback(self, in_data, frame_count, time_info, status):
        """
        Callback function for PyAudio stream.
        Collects incoming audio data when recording.
        """
        if not self.recording:
            return (None, pyaudio.paComplete)
        
        self.audio_frames.append(in_data)  # Append the audio data
        return (in_data, pyaudio.paContinue)

    def start_recording(self):
        """
        Start recording audio. Initializes a new stream and stores audio frames.
        """
        try:
            self.recording = True
            self.audio_frames = []  # Reset audio frame buffer
            
            self.stream = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size,
                                      stream_callback=self.callback)
            
            print("Recording started...")
            self.stream.start_stream()  # Start the stream

        except Exception as e:
            print(f"Error starting the recording: {e}")

    def get_recorded_audio(self):
        """
        Save the recorded audio to a WAV file.
        """
        output_dir = os.path.join('calix', 'audios')
        output_filename = os.path.join(output_dir, 'recorded_speech.wav')

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # Create directory if it doesn't exist

        try:
            with wave.open(output_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.audio_frames))  # Write audio frames as bytes
            print(f"Audio saved to {output_filename}")
        except Exception as e:
            print(f"Failed to save audio file: {e}")

    def stop_recording(self):
        """
        Stop the recording and close the audio stream.
        """
        try:
            if self.recording:
                self.recording = False
                self.stream.stop_stream()  # Stop the audio stream
                self.stream.close()  # Close the stream
                self.get_recorded_audio()  # Save the recorded audio
                print("Recording stopped.")
            else:
                print("Recording was not started.")
        except Exception as e:
            print(f"Error stopping the recording: {e}")

    def __del__(self):
        """
        Destructor to ensure PyAudio resources are properly cleaned up.
        """
        self.p.terminate()
