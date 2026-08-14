import json
from pathlib import Path


RAW_FILE = Path("data/raw/artists.json")
OUTPUT_FILE = Path("data/processed/graph.json")


def load_artists():
    with open(RAW_FILE, "r") as file:
        return json.load(file)


def create_node(id: str, type: str, name: str):
    return {
        "id": id,
        "type": type,
        "name": name
    }


def transform_artists(artists):
    nodes = []
    edges = []

    for artist in artists:

        # Artist node
        artist_node = create_node(
            artist["id"],
            "artist",
            artist["name"]
        )

        nodes.append(artist_node)


    return {
        "nodes": nodes,
        "edges": edges
    }


def save_graph(graph):

    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w") as file:
        json.dump(
            graph,
            file,
            indent=4,
            ensure_ascii=False
        )


if __name__ == "__main__":

    artists = load_artists()

    graph = transform_artists(artists)

    save_graph(graph)

    print("Graph generated ✅")