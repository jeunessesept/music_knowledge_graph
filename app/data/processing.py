import json
from pathlib import Path


RAW_FILE = Path("data/raw/artists.json")
OUTPUT_FILE = Path("data/processed/graph.json")


def load_artists():
    with open(RAW_FILE, "r") as file:
        return json.load(file)


def create_graph():
    return {
        "nodes": {
            "artists": {},
            "genres": {},
            "labels": {},
            "release_groups": {},
            "areas": {}
        },
        "edges": []
    }


def add_node(graph, category, id, data):
    if id not in graph["nodes"][category]:
        graph["nodes"][category][id] = data


def add_edge(graph, source, target, relation, weight=None):

    edge = {
        "source": source,
        "target": target,
        "type": relation
    }

    if weight:
        edge["weight"] = weight

    if edge not in graph["edges"]:
        graph["edges"].append(edge)



def transform_artists(artists):

    graph = create_graph()

    for artist in artists:

        artist_id = artist["id"]

        add_node(
            graph,
            "artists",
            artist_id,
            {
                "name": artist["name"],
                "country": artist.get("country"),
                "type": artist.get("type")
            }
        )



        for genre in artist.get("genres", []):

            genre_id = genre["id"]
            add_node(
                    graph,
                    "genres",
                    genre_id,
                    {
                    "name": genre["name"],
                    "count": genre.get("count"),
                     }
            )

            add_edge(
                graph,
                artist_id,
                genre_id,
                "HAS_GENRE",
                genre.get("count")
            )


    return graph



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