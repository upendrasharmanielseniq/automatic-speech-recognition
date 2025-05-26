import requests
from config import TMDB_API_KEY

def enrich_with_metadata(title):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={title}"
    resp = requests.get(url).json()
    if results := resp.get("results"):
        first = results[0]
        return {
            "poster": f"https://image.tmdb.org/t/p/w500{first['poster_path']}" if first.get("poster_path") else None,
            "overview": first.get("overview", ""),
        }
    return {}