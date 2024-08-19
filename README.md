# AIDA - Your Memory Assistant Redefined

AUDA is the brainchild of Memoro, a powerful memory assistant designed to listen to conversations, transcribe them, and provide contextual answers based on previously stored data. 
AIDA is being developed at the Artificial Intelligence and Data Analytics Lab (AIDA Lab) at Prince Sultan University (PSU) with the aim of furthering the efforts of Memoro. Utilizing OpenAI's GPT-4o-mini model, AIDA can retrieve relevant information and assist users by answering queries accurately.

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
   git clone https://github.com/MuddassirKhalidi/AIDA.git
   cd AIDA
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

- **list_audio_devices():** Lists all available audio input devices.
- **get_device_index_by_name(name):** Gets the index of an audio device by its name.
- **embed_text(text):** Embeds text using OpenAI's text embedding model.
- **write_to_file(text):** Writes text to a file with a timestamp.
- **text_to_speech(text):** Converts text to speech and plays the audio.
- **play_audio(file_path):** Plays an audio file.
- **speech_to_text():** Converts speech to text using OpenAI's Whisper model.
- **getAudio(device_name, chunk_size, format, channels, rate, silence_threshold, silence_duration):** Records audio using the specified device.
- **load_vector_store():** Loads embeddings from a file into the FAISS index.
- **update_vector_store(new_text):** Updates the FAISS index with new embeddings.
- **query_vector_store(query, top_k):** Queries the FAISS index for relevant embeddings.
- **generate_response(query):** Generates a response to a query using OpenAI's GPT-4 model.
- **get_query():** Captures and processes a query from speech.
- **listen():** Listens for and processes speech input.
- **intro():** Plays an introductory audio message.

## Acknowledgements

- [OpenAI](https://www.openai.com) for providing the powerful GPT-4o-mini and Whisper models.
