import openai
import os
from pathlib import Path

# Generate the pronunciation audio
def generate_audio(words, language="pl"):
    # Retrieve the OpenAI API key from the environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OpenAI API key must be set in the environment variable 'OPENAI_API_KEY'.")

    openai.api_key = api_key

    client = openai.OpenAI()

    audio_dir = Path("./audio")
    audio_dir.mkdir(exist_ok=True)

    for word in words:
        # Output file path
        audio_file_path = audio_dir / f"{word}.mp3"

        # Generate the audio using the updated API
        response = client.audio.speech.create(
            model="tts-1",  # Use tts-1-hd for higher quality audio if needed
            voice="alloy",  # Choose the appropriate voice
            input=word
        )

        # Save the audio to the file
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(response.content)

        print(f"Audio file saved at: {audio_file_path}")

    return [str(audio_dir / f"{word}.mp3") for word in words]

# Main function to generate audio
def main():
    words = ["gnocchi","croissant","shein",""]

    audio_file_paths = generate_audio(words)
    for path in audio_file_paths:
        print(f"Audio file saved at: {path}")

if __name__ == "__main__":
    main()