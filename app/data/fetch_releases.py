import json
import time
from pathlib import Path

import requests


BASE_URL = "https://musicbrainz.org/ws/2"
RAW_ARTISTS_FILE = Path("data/raw/artists.json")
OUTPUT_FILE = Path("data/raw/releases.json")

HEADERS = {
    "User-Agent": "music-knowledge-graph/1.0"
}


def load_artists() -> list[dict]:
    with open(RAW_ARTISTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_release_groups(artists: list[dict]) -> dict:
    release_groups = {}

    for artist in artists:
        for release_group in artist.get("release-groups", []):
            release_groups[release_group["id"]] = release_group

    return release_groups

def fetch_musicbrainz_data(url: str, params: dict) -> dict:
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            response.raise_for_status()

            time.sleep(1)

            return response.json()

        except requests.exceptions.RequestException as error:
            if attempt == 2:
                raise

            wait_seconds = 2 ** (attempt + 1)

            print(
                f"Request failed: {error}. "
                f"Retrying in {wait_seconds} seconds..."
            )

            time.sleep(wait_seconds)


def fetch_releases_for_group(release_group_id: str) -> list[dict]:
    releases = []
    offset = 0

    while True:
        url = f"{BASE_URL}/release"

        params = {
            "fmt": "json",
            "release-group": release_group_id,
            "status": "official",
            "limit": 100,
            "offset": offset,
            "inc": "labels+release-groups"
        }

        data = fetch_musicbrainz_data(url, params)
        page = data.get("releases", [])

        releases.extend(page)

        time.sleep(1)

        if not page or len(releases) >= data.get("release-count", 0):
            break

        offset += len(page)

    return releases


def fetch_all_releases(release_groups: dict) -> list[dict]:
    releases_by_id = {}

    for index, release_group in enumerate(release_groups.values(), start=1):
        print(
            f"[{index}/{len(release_groups)}] "
            f"Fetching: {release_group['title']}"
        )

        releases = fetch_releases_for_group(release_group["id"])

        for release in releases:
            releases_by_id[release["id"]] = release

    return list(releases_by_id.values())


def save_releases(releases: list[dict]) -> None:
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            releases,
            file,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":
    artists = load_artists()
    release_groups = get_release_groups(artists)

    releases = fetch_all_releases(release_groups)

    save_releases(releases)

    print(f"Saved {len(releases)} releases to {OUTPUT_FILE}")