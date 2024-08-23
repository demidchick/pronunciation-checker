import openai
import os
from pathlib import Path

# Function to generate the pronunciation audio using the new API
def generate_audio(word, language="pl"):
    # Retrieve the OpenAI API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OpenAI API key must be set in the environment variable 'OPENAI_API_KEY'.")

    # Initialize the OpenAI client with the API key
    openai.api_key = api_key

    # Define the client
    client = openai.OpenAI()

    # Define the output file path
    audio_file_path = Path(f"./audio/{word}.mp3")

    # Generate the audio using the updated API
    response = client.audio.speech.create(
        model="tts-1",  # Use tts-1-hd for higher quality audio if needed
        voice="alloy",  # Choose the appropriate voice
        input=word
    )

    # Save the audio to the file
    response.stream_to_file(audio_file_path)

    return str(audio_file_path)

# Function to update the HTML file with the new audio
def update_html(audio_file_path, word):
    html_file_path = "index.html"
    with open(html_file_path, "r") as file:
        html_content = file.read()

    # Update the src attribute for the audio tag
    new_audio_tag = f'<source src="{audio_file_path}" type="audio/mpeg">'
    updated_content = html_content.replace('<source src="audio/gnocchi.mp3" type="audio/mpeg">', new_audio_tag)

    # Save the updated HTML
    with open(html_file_path, "w") as file:
        file.write(updated_content)

# Main function to generate audio and update HTML
def main():
    word = "gnocchi"

    audio_file_path = generate_audio(word)
    update_html(audio_file_path, word)

if __name__ == "__main__":
    main()