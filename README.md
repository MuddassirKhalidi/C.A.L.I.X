# AIDA - Your Conversational Memory Assistant

AIDA is a memory assistant that listens to conversations, processes the speech into text, stores the data for future reference, and generates responses based on historical data. The system uses OpenAI's APIs for transcription, text generation, and speech synthesis. It is built with Python and Flask for backend services, and a local vector store using FAISS for efficient query retrieval.

## Table of Contents
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Endpoints](#api-endpoints)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

## Project Structure
- `app.py`: Main Flask application that handles API endpoints.
- `Audio_Recorder.py`: Handles audio recording and detection of silence to automatically stop recording.
- `aida.py`: Manages transcription, response generation, and text-to-speech operations.
- `memory.py`: Implements the FAISS-based vector store for efficient retrieval of past conversations.
- `store/`: Directory containing the FAISS index and metadata.

## Requirements

- Python 3.7+
- Flask
- PyAudio
- NumPy
- OpenAI Python client
- SoundFile and SoundDevice
- FAISS

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AIDA.git
   cd AIDA

   ```

2. **Install dependencies:**

   `pip install -U -r requirements.txt `

3. **Set up environment variables:**

   1. Navigate to Your Project Directory
   2. Open the `.env` file with `nano`:

      `nano .env`
4. **Edit the `.env` File:**
      ```
      OPENAI_API_KEY=your-openai-api-key
      ```
5. **Save and Exit:**
      - To save the changes, press Ctrl + O (write out), then press Enter.
      - To exit, press Ctrl + X.

## Usage

### Setting AIDA Up

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

### Running the app
1. **Run the Flask app**: `python app.py`
2. The app will be available at `http://127.0.0.1:5000/`
3. Use the API Endpoints to interact with AIDA

## API Endpoints
- `/listen` (GET): Starts recording audio. Returns a message indicating that recording has started.
- `/stop` (GET): Stops recording audio, processes the speech, and stores the conversation. Returns a message indicating that recording has stopped.
- `/respond` (GET): Stops recording, processes the speech, retrieves relevant past conversations, generates a response, and returns the processed query and response.

## Credits
AIDA was developed at the Artificial Intelligence and Data Analytics Lab (AIDA Lab) by:
- [Muddassir Khalidi](https://www.linkedin.com/in/muddassir-khalidi)
- [Zainab Mariya](https://www.linkedin.com/in/zainab-mariya-mohiuddin-629a20205/)
- [Saeed Lababidi](https://www.linkedin.com/in/saeed-lababidi-32554614a/)
- [Abdulrahman Mamdouh](https://www.linkedin.com/in/abdulrhman-mamdoh-soliman-2342372ba/)
- [Arwa Bawazir](https://www.linkedin.com/in/arwa-bawazir-5113b2276/)
- [Asma Khan](https://www.linkedin.com/in/asma-vaheed-khan-035b28291/)

## Acknowledgments
- [Professor Tanzila Saba](https://www.linkedin.com/in/prof-tanzila-saba-6195621a/) for her kind guidance and supervision of the project.
