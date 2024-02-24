# behind-mirror-assistant

## Installation

1. Install python libraries from `requirements.txt`
2. Pull and run whisper-asr-webservice:
```bash
docker pull onerahmet/openai-whisper-asr-webservice:latest
docker run -d -p 9000:9000 -e ASR_MODEL=base -e ASR_ENGINE=openai_whisper onerahmet/openai-whisper-asr-webservice:latest
```
