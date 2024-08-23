import os
from openai import OpenAI
from pathlib import Path

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Function to fetch the definition of the word using OpenAI's Chat API
def fetch_word_definition(word, language="pl"):
    prompt = (
        f"Podaj dokładną definicję słowa '{word}' w języku polskim, "
        "wraz z przykładami użycia, jeśli to możliwe. Definicja powinna być "
        "krótka, jasna i zrozumiała, odpowiednia dla osób uczących się języka."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.5,
    )

    if response.choices and len(response.choices) > 0:
        definition = response.choices[0].message.content.strip()
        return definition
    return "Nie znaleziono definicji tego słowa."

# Function to create a new HTML file for a keyword
def create_html_page(keyword, audio_file_path, definition):
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
                <source src="{audio_file_path}" type="audio/mpeg">
                Twoja przeglądarka nie obsługuje elementu audio.
            </audio>
        </section>

        <section class="banner">
            <h2>Popraw swoją wymowę z naszą aplikacją!</h2>
            <p>Pobierz naszą aplikację, która pomoże Ci poprawić wymowę trudnych słów w różnych językach. <a
                    href="https://gov.pl">Zainstaluj teraz!</a></p>
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

# Main function to process all keywords and generate the corresponding HTML pages
def main():
    audio_dir = Path("audio")
    if not audio_dir.exists():
        print(f"Audio directory {audio_dir} does not exist.")
        return

    # Iterate through all mp3 files in the audio directory
    for audio_file in audio_dir.glob("*.mp3"):
        keyword = audio_file.stem  # Get the keyword by removing the file extension
        audio_file_path = audio_file.resolve()

        # Fetch the definition for the keyword
        definition = fetch_word_definition(keyword)
        if definition == "Nie znaleziono definicji tego słowa.":
            print(f"Definition not found for keyword: {keyword}")
        
        # Create the HTML page for the keyword
        create_html_page(keyword, audio_file_path, definition)

if __name__ == "__main__":
    main()