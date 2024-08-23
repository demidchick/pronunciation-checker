import os
import requests
from pathlib import Path

# Function to fetch the definition of the word from a dictionary API
def fetch_word_definition(word, language="pl"):
    # Here, we're using the Owlbot API for demonstration purposes.
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        json_response = response.json()
        if json_response and 'meanings' in json_response[0]:
            # Return the first definition found
            return json_response[0]['meanings'][0]['definitions'][0]['definition']
    return "Nie znaleziono definicji tego słowa."

# Function to create a new HTML file for a keyword
def create_html_page(keyword, audio_file_path, definition):
    # Define the HTML content template
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
            /* This pushes the content towards the center while keeping it aligned left */
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
            /* Aligns text to the left inside the banner */
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

    # Define the file path
    output_dir = Path("pages")
    output_dir.mkdir(exist_ok=True)
    file_path = output_dir / f"{keyword}.html"

    # Write the HTML content to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_template)

    print(f"Page created: {file_path}")

# Main function to process all keywords and generate the corresponding HTML pages
def main():
    # List of keywords and their corresponding audio file paths
    keywords = ["croissant"]  # Replace with your actual keywords
    for keyword in keywords:
        audio_file_path = f"audio/{keyword}.mp3"  # Update the audio path accordingly
        definition = fetch_word_definition(keyword)  # Fetch the definition for the keyword
        create_html_page(keyword, audio_file_path, definition)

if __name__ == "__main__":
    main()