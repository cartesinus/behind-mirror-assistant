# -*- coding: utf-8 -*-
"""
This module serves as an interface for a magic mirror, designed to communicate and display messages
on the mirror. It facilitates the sending of messages from backend services to the frontend display
of a magic mirror, enabling dynamic interaction and content updates.
"""

import requests
import json

def send_message_to_frontend(message: str):
    """
    Sends a message to the frontend via POST request.

    Args:
        message (str): The message to send to the frontend.
    """
    url = "http://localhost:8080/custom-message"
    headers = {"Content-Type": "application/json"}
    payload = {
        "messageHeader": "GPT",
        "message": message
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.ok:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
