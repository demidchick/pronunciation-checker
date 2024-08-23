import requests

def get_google_autocomplete_suggestions(query, language="pl"):
    """Fetches Google autocomplete suggestions for a given query."""
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={query}&hl={language}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    suggestions = response.json()[1]  # Get the list of suggestions from the response
    return suggestions

def pick_top_keywords(suggestions, n=50):
    """Picks the top N keywords from the suggestions."""
    return suggestions[:n]

def clean_keyword(keyword, prefix):
    """Removes the prefix and cleans up the keyword."""
    return keyword.replace(prefix, "").strip().lower()

def main():
    seed_query = "jak się wymawia" 
    
    print(f"Fetching autocomplete suggestions for '{seed_query}'...")
    suggestions = get_google_autocomplete_suggestions(seed_query)
    
    print("Raw suggestions:", suggestions)
    
    cleaned_keywords = [clean_keyword(suggestion, seed_query) for suggestion in suggestions]
    
    top_keywords = pick_top_keywords(cleaned_keywords)
    
    print("Top 50 keywords:", top_keywords)
    return top_keywords

if __name__ == "__main__":
    keywords = main()