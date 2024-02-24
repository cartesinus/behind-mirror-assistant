# Behind-Mirror Assistant

A hobby project that transforms a Raspberry Pi into a virtual assistant hidden behind a Venetian
mirror, enabling basic question-and-answer interactions.

## Installation

### Prerequisites

- Python 3.8 or newer
- Docker
- Conda (recommended for managing Python versions and dependencies)

### Steps

1. **Environment Setup**:
   - Install Conda and create a new environment:
     ```bash
     conda create -n mirror_va python=3.8
     conda activate mirror_va
     ```

2. **Install Dependencies**:
   - With your environment activated, install the required Python libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Speech Recognition Service**:
   - Download and run the OpenAI Whisper ASR webservice:
     ```bash
     docker pull onerahmet/openai-whisper-asr-webservice:latest
     docker run -d -p 9000:9000 -e ASR_MODEL=base -e ASR_ENGINE=openai_whisper onerahmet/openai-whisper-asr-webservice:latest
     ```

4. **PortAudio**:
   - Required for audio recording on Raspberry Pi:
     ```bash
     sudo apt-get install portaudio19-dev
     ```

## Usage

1. **Start the Speech Recognition Service**:
   - Ensure the Whisper ASR webservice container is running as described in the installation section.

2. **Running the Assistant**:
   - Obtain an access key from [Porcupine Console](https://console.picovoice.ai/).
   - Start the assistant with the command:
     ```bash
     python run_mirror_va.py --access_key $KEY
     ```
   - Replace `$KEY` with your Porcupine access key.
