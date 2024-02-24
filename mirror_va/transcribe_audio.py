# -*- coding: utf-8 -*-
"""
This module provides functionalities for audio recording and transcription. It includes
functions to record audio from the default microphone for a specified duration and
to send audio files to a local Automatic Speech Recognition (ASR) API for transcription.

Functions:
- record_audio: Records audio for a given duration and saves it to a specified file.
- transcribe_audio: Sends an audio file to the ASR API and returns the transcribed text.
"""

from typing import Optional
import wave
import requests
import pyaudio

def record_audio(duration=5, output_filename='output.wav'):
    """
    Records audio from the default microphone for a specified duration and saves it to a file.

    Args:
        duration (int): Duration to record in seconds, defaults to 5.
        output_filename (str): Filename for the saved audio file.

    Returns:
        str: The path to the output audio file.
    """
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    recorder = pyaudio.PyAudio()

    stream = recorder.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print("Recording...")
    frames = []

    for _ in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    recorder.terminate()

    wav_file = wave.open(output_filename, 'wb')
    wav_file.setnchannels(channels)
    wav_file.setsampwidth(recorder.get_sample_size(format))
    wav_file.setframerate(rate)
    wav_file.writeframes(b''.join(frames))
    wav_file.close()
    return output_filename


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
        'language': 'en',
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
