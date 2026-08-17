import streamlit as st
from graph.visualization import (
    build_networkx_graph,
    generate_pyvis_html,
    get_artist_subgraph
)
import json



GRAPH_FILE = "data/processed/graph.json"


def load_graph():

    with open(GRAPH_FILE, "r") as file:
        return json.load(file)


graph = load_graph()


st.title("🎵 Electronic Music Knowledge Graph")


artists = graph["nodes"]["artists"]
genres = graph["nodes"]["genres"]
edges = graph["edges"]


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Artists",
        len(artists)
    )

with col2:
    st.metric(
        "Genres",
        len(genres)
    )

with col3:
    st.metric(
        "Relations",
        len(edges)
    )


st.divider()

st.subheader("Explore an artist")

artist_ids = sorted(
    artists,
    key=lambda artist_id: artists[artist_id]["name"]
)

selected_artist_id = st.selectbox(
    "Select an artist",
    options=artist_ids,
    format_func=lambda artist_id: artists[artist_id]["name"]
)

depth = st.slider(
    "Exploration depth",
    min_value=1,
    max_value=3,
    value=1
)

networkx_graph = build_networkx_graph(graph)

artist_graph = get_artist_subgraph(
    networkx_graph,
    selected_artist_id,
    depth
)

st.caption(
    f"Showing {artist_graph.number_of_nodes()} nodes "
    f"and {artist_graph.number_of_edges()} relations"
)

graph_html = generate_pyvis_html(artist_graph)

st.iframe(
    graph_html,
    height=720
)

st.subheader("Artists")

for artist_id, artist in artists.items():

    st.write(
        f"🎧 {artist['name']}"
    )


st.subheader("Genres")

for genre_id, genre in genres.items():

    st.write(
        f"🎼 {genre['name']}"
    )