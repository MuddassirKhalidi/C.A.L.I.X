# Memoro II - Your Memory Assistant Redefined

Memoro II is the brainchild of Memoro, a powerful memory assistant designed to listen to conversations, transcribe them, and provide contextual answers based on previously stored data. 
Memoro II is being developed at the Artificial Intelligence and Data Analytics Lab (AIDA Lab) at Prince Sultan University (PSU) with the aim of furthering the efforts of Memoro. Utilizing OpenAI's GPT-3.5-turbo model and Pinecone's vector database, Memoro II can retrieve relevant information and assist users by answering queries accurately.

## Features

- **Audio Recording:** Records audio using the default microphone or a specified audio input device.
- **Speech-to-Text:** Converts recorded audio to text using OpenAI's Whisper model.
- **Text Embeddings:** Generates text embeddings using OpenAI's `text-embedding-ada-002` model.
- **Contextual Search:** Retrieves relevant information from Pinecone's vector database based on user queries.
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
1. **Install dependencies**
   ```!pip install playsound
   !pip install -U openai
   !pip install -U openai-whisper
   !pip install pyaudio
   !pip install wave
   !pip install numpy
   !pip install tqdm
   !pip install pinecone
   !pip install nltk
   ```

2. **`FFmpeg` Installation**

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

3. **Importing Libraries and Downloading NLTK data:**
   ```import os
   import openai
   from openai import OpenAI
   from dotenv import load_dotenv, find_dotenv
   from playsound import playsound
   import pyaudio
   import wave
   import numpy as np
   import whisper
   import warnings
   import pinecone
   import nltk
   from tqdm import tqdm
   from time import sleep
   nltk.download('punkt')
   from pinecone import Pinecone
    ```
4. **Load environment variables from .env file**
```
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
```

5. **Selecting Micrphone**

### Microphone Device Selection

#### The `PyAudio` library requires you to choose a device with which you want to input speech. 

#### Use the cell below to decide on which audio device you will use for your microphone.

### RUN THIS CELL BEFORE THE MAIN CODE CELL
```
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
print(f'Index | Device')
devices = []
for index, name in device_list:
    devices.append(name)
    print(f'{index}     |  {name}')
    
device = input('Choose a device from the list above by name: ')
while device not in devices:
    device = input('Choose a valid device: ')
```

### Recording and Processing Audio

1. **Start a conversation:**

   Ensure your microphone is set up and run the `Main Cell` start recording:

2. **Process the context:**

   The recorded audio will be transcribed, and the transcriptions will be upserted into the Pinecone database:

3. **Query the assistant:**

   Run the next cell to prompt Memoro II

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
- [NLTK](https://www.nltk.org) for the natural language processing tools.
- [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) for the audio handling capabilities.
- [playsound](https://github.com/TaylorSMarks/playsound) for audio playback functionality.
