# -*- coding: utf-8 -*-
"""
Script for generating and executing Python code using OpenAI's GPT model.

This CLI tool prompts users for a command, uses OpenAI's GPT model to generate corresponding Python
code, and offers the option to execute the generated code. It includes functions to execute code
and read file contents. The script loops to allow continuous interaction, with an option to exit.

Before running the script, ensure that a .env file is present with the OpenAI API key specified
like this:
OPENAI_API_KEY="your key here"
"""

from openai import OpenAI
from dotenv import load_dotenv

class GPTAssistant():
    """
    A class to interact with the OpenAI GPT models for generating text completions. It encapsulates
    the process of sending queries to the GPT model and retrieving responses.

    Attributes:
        client (OpenAI): An instance of the OpenAI client, initialized using API credentials.
    """

    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def query(self, message):
        """
        Sends a query to the GPT model and returns the response.

        Args:
            message (str): The message to send to the GPT model.

        Returns:
            str: The text response from the GPT model.
        """
        response = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[{"role": "system", "content": "Answer this question within 200 characters:"},
                    {"role": "user", "content": message}]
        )

        return response.choices[0].message.content

    def execute_python_code(self, code):
        """
        Executes given Python code using exec().

        Parameters:
        code (str): Python code to execute.

        Does not return anything; handles and displays exceptions.
        """
        try:
            exec(code)
        except Exception as e:
            click.echo(f"Error executing code: {e}")

    def read_file_content(self, file_path):
        """
        Reads and returns the content of a specified file.

        Parameters:
        file_path (str): Path to the file to read.

        Returns:
        Content of the file as a string, or None if the file is not found.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            click.echo(f"Error: File {file_path} not found.")
            return None

    def extract_code(gpt_response):
        """
        Extracts Python code from a GPT response enclosed within markdown code blocks.

        Parameters:
        gpt_response (str): The GPT response string containing the code block.

        Returns:
        str: The extracted Python code, or an empty string if no code block is found.
        """
        if '```python' in gpt_response and '```' in gpt_response:
            # Splitting at the start of the code block and taking the second part
            code_start = gpt_response.split('```python', 1)[1]
            # Splitting at the end of the code block and taking the first part
            code = code_start.split('```', 1)[0]
            return code.strip()
        else:
            return ""
