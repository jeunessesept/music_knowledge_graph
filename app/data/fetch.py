import requests
import time 
import json

BASE_URL = "https://musicbrainz.org/ws/2"

def fetch_artist(mbid: str) -> dict:
    """
    Fetch artist data from MusicBrainz API using the artist's MBID.

    Args:
        mbid (str): The MusicBrainz Identifier (MBID) of the artist.

    Returns:
        dict: A dictionary containing the artist's data.
    """
    url = f"{BASE_URL}/artist/{mbid}"
    params = {
        "fmt": "json",
        'inc' :"genres"
    }
    headers = {
        "User-Agent": "music-knowledge-graph/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()  # Raise an error for bad responses

    return response.json()


def search_artist(name: str) -> str:
    """
    Search for an artist on MusicBrainz and return its MBID.

    Args:
        name (str): The artist's name.

    Returns:
        str: The artist's MBID.
    """
    url = f"{BASE_URL}/artist"

    params = {
        "query": f'artist:"{name}"',
        "fmt": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "music-knowledge-graph/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data["artists"][0]["id"]



def fetch_artists(names: list[str]) -> list[dict]:
    artists = []

    for name in names:
        mbid = search_artist(name)
        artist = fetch_artist(mbid)
        artists.append(artist)

        time.sleep(1)  # Sleep for 1 second to respect rate limits

    return artists


artist_names = [
    "Aphex Twin"
]



artists = fetch_artists(artist_names)

with open("data/raw/artists.json", "w", encoding="utf-8") as f:
    json.dump(artists, f, ensure_ascii=False, indent=4)

