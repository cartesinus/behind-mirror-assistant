# asr_client.py
import requests
from typing import Optional

def transcribe_audio(file_path: str) -> Optional[str]:
    """
    Sends an audio file to the local ASR API for transcription.
    
    Args:
        file_path: The path to the WAV audio file to be transcribed.
    
    Returns:
        The transcribed text as a string if successful, None otherwise.
    """
    url = 'http://localhost:9000/asr'
    params = {
        'encode': 'true',
        'task': 'transcribe',
        'language': 'pl',
        'word_timestamps': 'false',
        'output': 'txt'
    }
    headers = {'accept': 'application/json'}
    files = {'audio_file': (file_path, open(file_path, 'rb'), 'audio/wav')}
    
    try:
        response = requests.post(url, params=params, headers=headers, files=files)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        files['audio_file'][1].close()

if __name__ == "__main__":
    # Example usage
    file_path = 'test-speech-recording-pl.wav'
    transcribed_text = transcribe_audio(file_path)
    if transcribed_text is not None:
        print(f"Transcribed Text: {transcribed_text}")
    else:
        print("Failed to transcribe audio.")
