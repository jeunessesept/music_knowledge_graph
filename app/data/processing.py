import json
from pathlib import Path


RAW_ARTISTS_FILE = Path("data/raw/artists.json")
RAW_RELEASES_FILE = Path("data/raw/releases.json")
OUTPUT_FILE = Path("data/processed/graph.json")


def load_artists():
    with open(RAW_ARTISTS_FILE, "r") as file:
        return json.load(file)

def load_releases():
    with open(RAW_RELEASES_FILE, "r") as file:
        return json.load(file)

def create_graph():
    return {
        "nodes": {
            "artists": {},
            "genres": {},
            "labels": {},
            "release_groups": {},
            "releases": {},
            "areas": {}
        },
        "edges": []
    }


def add_node(graph, category, id, data):
    if id not in graph["nodes"][category]:
        graph["nodes"][category][id] = data

def add_edge(
    graph,
    source,
    source_type,
    target,
    target_type,
    relation,
    weight=None
):

    edge = {
        "source": source,
        "source_type": source_type,
        "target": target,
        "target_type": target_type,
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
                "artist",
                genre_id,
                "genre",
                "HAS_GENRE",
                genre.get("count")
            )

        # Release groups

        for release_group in artist.get("release-groups", []):

            release_id = release_group["id"]

            add_node(
                graph,
                "release_groups",
                release_id,
                {
                    "title": release_group["title"],
                    "type": release_group.get("primary-type"),
                    "date": release_group.get("first-release-date")
                }
            )


            add_edge(
                graph,
                artist_id,
                "artist",
                release_id,
                "release_group",
                "RELEASED"
            )

        ## Label relations 

        for relation in artist.get("relations", []):

            if relation.get("target-type") != "label":
                continue

            label = relation.get("label")

            if not label:
                continue

            label_id = label["id"]

            add_node(
                graph,
                "labels",
                label_id,
                {
                    "name": label["name"],
                    "type": label.get("type"),
                    "label_code": label.get("label-code")
                }
            )

            add_edge(
                graph,
                artist_id,
                "artist",
                label_id,
                "label",
                relation["type"]
            )

    return graph


def add_releases_to_graph(graph, releases):

    for release in releases:

        release_id = release["id"]
        release_group = release.get("release-group")

        if not release_group:
            continue    

        release_group_id = release_group["id"]

        add_node(
            graph,
            "releases",
            release_id,
            {
                "title": release["title"],
                "date": release.get("date"),
                "country": release.get("country"),
            }
        )

        add_edge(
            graph,
            release_group_id,
            "release_group",
            release_id,
            "release",
            "HAS_RELEASE"
        )

        for label_info in release.get("label-info", []):

            label = label_info.get("label")

            if not label:
                continue

            label_id = label["id"]

            add_node(
                graph,
                "labels",
                label_id,
                {
                    "name": label["name"],
                    "type": label.get("type"),
                    "label_code": label.get("label-code")
                }
            )

            add_edge(
                graph,
                release_id,
                "release",
                label_id,
                "label",
                "RELEASED_BY"
            )

    


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
    releases = load_releases()

    graph = transform_artists(artists)
    add_releases_to_graph(graph, releases)

    save_graph(graph)

    print("Graph generated ✅")