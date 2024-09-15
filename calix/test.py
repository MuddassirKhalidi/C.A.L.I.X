from pydub import AudioSegment
import os

def combine_audios(audio_files, output_path):
    # Start with an empty audio segment
    combined_audio = AudioSegment.empty()

    # Loop through the list of audio files and combine them
    for audio_file in audio_files:
        # Load the current audio file
        audio = AudioSegment.from_file(audio_file)
        # Append it to the combined audio
        combined_audio += audio

    # Export the combined audio to the desired output path
    combined_audio.export(output_path, format="wav")

if __name__ == "__main__":
    # Path to your audio files
    audio_dir = os.path.join('calix', 'audios')
    
    # List of your 9 audio files
    audio_files = [
        os.path.join(audio_dir, 'recorded_speech', f"speech_part{i}.mp3") for i in range(9)
    ]
    
    # Combine and save as 'combined_audio.wav'
    output_path = os.path.join(audio_dir, 'recorded_speech.wav')
    combine_audios(audio_files, output_path)

    print("Audio files combined successfully!")
