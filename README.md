# Memoro II - Your Memory Assistant Redefined

Memoro II is the brainchild of Memoro, a powerful memory assistant designed to listen to conversations, transcribe them, and provide contextual answers based on previously stored data. 
Memoro II is being developed at the Artificial Intelligence and Data Analytics Lab (AIDA Lab) at Prince Sultan University (PSU) with the aim of furthering the efforts of Memoro. Utilizing OpenAI's GPT-4o-mini model, Memoro II can retrieve relevant information and assist users by answering queries accurately.

## Features

- **Audio Recording:** Records audio using the default microphone or a specified audio input device.
- **Speech-to-Text:** Converts recorded audio to text using OpenAI's Whisper model.
- **Contextual Search:** Retrieves relevant information from short and long term buffers.
- **Text-to-Speech:** Converts text responses back to speech for a seamless user experience.

## Installation

### Prerequisites

- Python 3.7 or later
- `pip` package manager

### Steps

1. **Clone the repository:**

   ```
   git clone https://github.com/MuddassirKhalidi/MEMORO---II.git
   cd MEMORO---II
   ```

2. **Install dependencies:**

   `pip install -U -r requirements.txt `

3. **Set up environment variables:**

   1. Navigate to Your Project Directory
   2. Open the `.env` file with `nano`:

      `nano .env`
   4. Edit the `.env` File:
      ```
      OPENAI_API_KEY=your-openai-api-key
      PINECONE_API_KEY=your-pinecone-api-key
      ```
   5. Save and Exit:
      - To save the changes, press Ctrl + O (write out), then press Enter.
      - To exit, press Ctrl + X.

## Usage
### Setting Memoro Up

**`FFmpeg` Installation**

#### On Windows:

##### Download
Go to the FFmpeg Official Website and download the latest build for Windows.

##### Extract
Extract the downloaded ZIP file to a directory, for example, C:\FFmpeg.

##### Environment Variable:
- Right-click on 'This PC' or 'Computer' on your desktop or File Explorer, and select 'Properties'.

- Click on 'Advanced system settings' and then 'Environment Variables'.

- Under 'System Variables', find and select 'Path', then click 'Edit'.

- Click 'New' and add the path to your FFmpeg bin directory, e.g., C:\FFmpeg\bin.

- Click 'OK' to close all dialog boxes.

#### On macOS:

You can install `ffmpeg` using Homebrew:

`brew install ffmpeg`

#### On Linux:
For Ubuntu and other Debian-based distributions, you can install ffmpeg from the apt repository:

`sudo apt update`

`sudo apt install ffmpeg`

## Code Overview

### Functions

- **get_OPENAI_API():** Loads the OpenAI API key from environment variables.
- **list_audio_devices():** Lists available audio input devices.
- **get_device_index_by_name(name):** Finds the index of an audio device by its name.
- **getAudio():** Records audio until a period of silence is detected and saves it to a file.
- **create_metadata():** Creates metadata for sentences with a sliding window approach.
- **get_PINECONE_API():** Initializes connection to Pinecone API and returns the index.
- **upsert_vectors():** Upserts vectors into Pinecone from sentences.
- **speech_to_text():** Converts recorded audio to text using Whisper model.
- **process_context():** Processes the context by recording speech, converting it to text, and upserting to Pinecone.
- **text_to_speech():** Converts text to speech and plays the audio.
- **write_to_file():** Writes the text to a file.
- **read_from_file():** Reads text from a file.
- **play_audio():** Plays an audio file.
- **get_prompt():** Retrieves the prompt by converting speech to text and finding relevant contexts from Pinecone.
- **process_prompt():** Processes the prompt by generating a response from the GPT-3.5-turbo model and converting it to speech.


## Acknowledgements

- [OpenAI](https://www.openai.com) for providing the powerful GPT-3.5-turbo and Whisper models.
- [Pinecone](https://www.pinecone.io) for the vector database services.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for the audio handling capabilities.
- [playsound](https://github.com/TaylorSMarks/playsound) for audio playback functionality.
