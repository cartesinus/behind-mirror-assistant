"""
This script utilizes the Porcupine wake word engine to detect specific keywords in real-time audio
streams. It integrates with the Porcupine library and a custom recorder to continuously listen to
audio input from a specified device, identify occurrences of given keywords, and respond
accordingly.

The script defines a `detect_kwd` function to initialize the Porcupine engine with specific
parameters, including keyword sensitivity and audio device configuration. On detecting a keyword,
the function returns the keyword's index from the provided list.

Example usage is provided within the script, demonstrating how to set up the keyword detection with
an access key and a list of keywords.
"""

import pvporcupine
from pvrecorder import PvRecorder

def detect_kwd(
        access_key, keywords=None, keyword_paths=None, library_path=None, model_path=None,
        sensitivities=None, audio_device_index=-1
    ):
    """
    Initializes and runs the Porcupine wake word engine to detect specific keywords from audio
    input.

    Args:
        access_key (str): Access key for using Porcupine's API.
        keywords (list of str, optional): List of keywords to detect. Default is None.
        keyword_paths (list of str, optional): List of paths to keyword model files. Default is
            None.
        library_path (str, optional): Path to Porcupine's dynamic library. Default is None.
        model_path (str, optional): Path to Porcupine's model file. Default is None.
        sensitivities (list of float, optional): Detection sensitivities for each keyword. Default
            is [0.8].
        audio_device_index (int, optional): Index of the audio input device. Default is -1
            (default device).

    Returns:
        int: The index of the detected keyword within the `keywords` list, if any.

    Raises:
        ValueError: If both `keywords` and `keyword_paths` are None.
    """
    # Validate and setup keyword paths and sensitivities
    if keyword_paths is None:
        if keywords is None:
            raise ValueError("Either keywords or keyword_paths must be set.")
        keyword_paths = [pvporcupine.KEYWORD_PATHS[x] for x in keywords]
    if sensitivities is None:
        sensitivities = [0.8] * len(keyword_paths)

    # Create Porcupine instance
    porcupine = pvporcupine.create(
        access_key=access_key,
        library_path=library_path,
        model_path=model_path,
        keyword_paths=keyword_paths,
        sensitivities=sensitivities)

    # Setup recorder
    recorder = PvRecorder(device_index=audio_device_index, frame_length=porcupine.frame_length)
    recorder.start()

    print('Listening for keywords...')

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)
            if result >= 0:
                print(f"Keyword detected: {keywords[result]}")
                return result
    finally:
        recorder.delete()
        porcupine.delete()
