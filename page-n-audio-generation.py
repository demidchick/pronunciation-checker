import openai
import os
from pathlib import Path

# Initialize the OpenAI client with your API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OpenAI API key must be set in the environment variable 'OPENAI_API_KEY'.")

openai.api_key = api_key
client = openai.OpenAI()

# Function to generate pronunciation audio
def generate_audio(words, language="pl"):
    audio_dir = Path("audio/")
    audio_dir.mkdir(exist_ok=True)

    audio_file_paths = []

    for word in words:
        # Output file path
        audio_file_path = audio_dir / f"{word}.mp3"

        # Generate the audio using the OpenAI API
        response = client.audio.speech.create(
            model="tts-1",  # Use tts-1-hd for higher quality audio if needed
            voice="alloy",  # Choose the appropriate voice
            input=word
        )

        # Save the audio to the file
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(response.content)

        print(f"Audio file saved at: {audio_file_path}")
        audio_file_paths.append(str(audio_file_path))

    return audio_file_paths

# Function to fetch the definition of the word using OpenAI's Chat API
def fetch_word_definition(word, language="pl"):
    prompt = (
        f"Podaj dokładną definicję słowa '{word}' w języku polskim, wraz z przykładami użycia, jeśli to możliwe. Definicja powinna być krótka, jasna i zrozumiała, odpowiednia dla osób uczących się języka. Dodaj przykłady użycia, jeśli to możliwe. Wszystkie odpowiedzi muszą być w formacie tekstu bez żadnego dodatkowego formatowania."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a dictionary that gives definitions of the words with giving some examples."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.5,
    )

    if response.choices and len(response.choices) > 0:
        definition = response.choices[0].message.content.strip()
        return definition
    return "Nie znaleziono definicji tego słowa."

def create_html_page(keyword, audio_file_path, definition):
    # Update the path to be relative to the 'pages' directory
    audio_relative_path = "../" + audio_file_path

    html_template = f"""<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="Dowiedz się, jak wymawiać '{keyword}' poprawnie. Posłuchaj audio i ucz się wymowy z nami!">
    <title>Jak wymawiać '{keyword}'?</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #FAFAFA;
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}

        .container {{
            max-width: 800px;
            margin-left: 50px;
            margin-right: auto;
        }}

        h1,
        h2,
        h3 {{
            color: #2E2E2E;
            font-weight: 600;
        }}

        h1 {{
            font-size: 2.5rem;
            margin: 20px 0;
        }}

        p {{
            font-size: 1.125rem;
            line-height: 1.8;
        }}

        audio {{
            display: block;
            margin: 20px 0;
        }}

        .banner {{
            margin-top: 30px;
            padding: 20px;
            background-color: #F2F4F7;
            border-radius: 8px;
            border: 1px solid #E0E0E0;
            text-align: left;
        }}

        .banner a {{
            color: #3366FF;
            text-decoration: none;
            font-weight: 600;
        }}

        .content {{
            margin-top: 40px;
        }}

        .content h3 {{
            font-size: 1.75rem;
            margin-bottom: 10px;
        }}
    </style>
</head>

<body>
    <div class="container">
        <header>
            <h1>Jak wymawiać '{keyword}'?</h1>
            <p>Słowo '{keyword}' może być trudne do wymówienia. Oto jak poprawnie wymawiać '{keyword}':</p>
        </header>

        <section>
            <!-- Audio file -->
            <audio controls>
                <source src="{audio_relative_path}" type="audio/mpeg">
                Twoja przeglądarka nie obsługuje elementu audio.
            </audio>
        </section>

        <section class="banner">
            <h2>Popraw swoją wymowę z naszą aplikacją!</h2>
            <p>Pobierz naszą aplikację, która pomoże Ci poprawić wymowę trudnych słów w różnych językach. <a
                    href="https://gov.pl">Zarejestruj się teraz</a></p>
        </section>

        <section class="content">
            <h3>Znaczenie '{keyword}'</h3>
            <p>{definition}</p>
        </section>
    </div>
</body>

</html>"""

    output_dir = Path("pages")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / f"{keyword}.html"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"Page created: {file_path}")

# Function to create the index page
def create_index_page():
    index_content = f"""<!DOCTYPE html>
<html lang="pl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="Dowiedz się, jak wymawiać różne słowa poprawnie. Posłuchaj audio i ucz się wymowy z nami!">
    <title>Jak wymawiać te słowa?</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #FAFAFA;
            color: #333;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}

        .container {{
            max-width: 800px;
            margin-left: 50px;
            margin-right: auto;
        }}

        h1 {{
            font-size: 2.5rem;
            margin: 20px 0;
            color: #2E2E2E;
            font-weight: 600;
        }}

        p {{
            font-size: 1.125rem;
            line-height: 1.8;
        }}

        ul {{
            font-size: 1.125rem;
            line-height: 1.8;
            list-style: none;
            padding-left: 0;
        }}

        ul li {{
            margin: 10px 0;
        }}

        ul li a {{
            color: #3366FF;
            text-decoration: none;
            font-weight: 600;
        }}

        .banner {{
            margin-top: 30px;
            padding: 20px;
            background-color: #F2F4F7;
            border-radius: 8px;
            border: 1px solid #E0E0E0;
            text-align: left;
        }}

        .banner a {{
            color: #3366FF;
            text-decoration: none;
            font-weight: 600;
        }}
    </style>
</head>

<body>
    <div class="container">
        <header>
            <h1>Naucz się wymawiać te słowa</h1>
            <p>Dowiedz się, jak poprawnie wymawiać różne trudne słowa:</p>
        </header>
        <section>
            <ul>
"""

    # Dynamically add links to pages in the "pages" folder
    pages_dir = Path("pages")
    for page_file in pages_dir.glob("*.html"):
        keyword = page_file.stem
        index_content += f'                <li><a href="pages/{page_file.name}">{keyword.capitalize()}</a></li>\n'

    # Close the HTML structure
    index_content += """            </ul>
        </section>

        <section class="banner">
            <h2>Popraw swoją wymowę z naszą aplikacją!</h2>
            <p>Pobierz naszą aplikację, która pomoże Ci poprawić wymowę trudnych słów w różnych językach. <a
                    href="https://gov.pl">Zarejestruj się teraz!</a></p>
        </section>

    </div>
</body>

</html>"""

    # Write the index content to the index.html file
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(index_content)

    print("Index page created: index.html")

# Main function to generate audio, create corresponding HTML pages, and update the index page
def main():
    words = ['lamborghini']

    # Generate audio files
    audio_file_paths = generate_audio(words)

    # Create HTML pages
    for audio_file_path in audio_file_paths:
        keyword = Path(audio_file_path).stem  # Get the keyword by removing the file extension
        definition = fetch_word_definition(keyword)
        create_html_page(keyword, audio_file_path, definition)

    # Create the index page with links to all generated pages
    create_index_page()

if __name__ == "__main__":
    main()