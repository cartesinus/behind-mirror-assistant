#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script serves as the main runner for a voice-activated application. It continuously listens
for a specified keyword using the Porcupine wake word engine. Upon detecting the keyword, it records
audio for a predefined duration, sends this recording to an ASR API for transcription, and prints
the transcription to the console.

Arguments:
- access_key (str): Required access key to use the Porcupine API, obtained via command line.

The script utilizes functionalities defined in the `detect_kwd` and `transcribe_audio` modules
within the `mirror_va` package to perform keyword detection, audio recording, and transcription.
"""

import argparse
import time
from pygame import mixer
from mirror_va.detect_kwd import detect_kwd
from mirror_va.transcribe_audio import record_audio, transcribe_audio

def main(access_key):
    """
    Executes the main workflow of the voice-activated application. It listens for a specified
    keyword, records audio upon detection, sends the audio for transcription, and prints the
    transcription.

    The function loops indefinitely, performing these steps:

    1. Detects the specified keyword using the Porcupine wake word engine.
    2. Records audio for a set duration once the keyword is detected.
    3. Sends the recorded audio to an ASR API for transcription.
    4. Prints the transcribed text to the console.
    5. Pauses briefly before restarting the listening process.

    Args:
        access_key (str): The access key for using the Porcupine API, provided as a command-line
            argument.
    """
    keywords = ["bumblebee"]
    mixer.init()
    mixer.music.load('mirror_va/beep.mp3')

    while True:
        # Detect keyword
        kwd_detected = detect_kwd(access_key=access_key, keywords=keywords)
        if kwd_detected is not None:
            print("Keyword detected, starting audio recording...")
            mixer.music.play()

            # Record audio for 5 seconds
            record_audio(duration=5, output_filename='temp_audio.wav')
            mixer.music.play()

            # Send to API
            transcription = transcribe_audio('temp_audio.wav')

            # Print transcribed audio
            print("Transcription:", transcription)

            # Wait before listening again
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--access_key',
        help='AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)')
    args = parser.parse_args()

    main(args.access_key)
