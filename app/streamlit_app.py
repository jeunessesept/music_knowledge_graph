import streamlit as st
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