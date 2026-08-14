## 🎵  Electronic Music Knowledge Graph

An interactive knowledge graph dedicated to electronic music, built with Python and Streamlit.
The project explores relationships between artists, genres, releases, labels and musical influences, using data collected from public music APIs.

## 🎯  Project goals

The goal is to build a small but complete data project that demonstrates:
- API consumption
- Data collection and cleaning
- Graph data modeling
- Graph algorithms
- Interactive data visualization
- Python development
- Streamlit application development
The project is intentionally limited in scope to keep it simple, understandable and easy to extend.

## 🕸️ Concept
The application represents electronic music as a network of interconnected entities.

For example:

```plain text

                    IDM
                  ↗     ↘
                 /       \
        Aphex Twin       Autechre
             │               │
          RELEASED         RELEASED
             ↓               ↓
 Selected Ambient       Tri Repetae
     Works 85–92
             │
        RELEASED_BY
             ↓
           Warp

```

An artist can therefore be connected to:

- Genres
- Sub-genres
- Releases
- Labels
- Similar artists
- Influences
- Collaborations

## 📡 Data sources

### MusicBrainz

MusicBrainz will be the main source for structured music metadata.
The API provides information about:
- Artists
- Releases
- Release groups
- Labels
- Genres
- Tags
- Release dates
- Countries

MusicBrainz identifiers (MBIDs) will be used to uniquely identify entities.

API documentation:
https://musicbrainz.org/doc/MusicBrainz_API


### Last.fm

Last.fm will complement MusicBrainz with information particularly useful for discovering relationships between artists.

Potential data:

- Similar artists
- Tags
- Top albums
- Top tracks
- Similar genres

API documentation:

https://www.last.fm/api

Example:

```text
Aphex Twin
    │
    ├── SIMILAR_TO → Autechre
    ├── SIMILAR_TO → Squarepusher
    ├── TAGGED_AS → IDM
    └── TAGGED_AS → Ambient

```

## Wikidata — optional

Wikidata could be added in a later version to enrich the graph with additional information such as:

- Birth dates
- Countries
- Instruments
- Occupations
- Influences


## 🛠️ Tech stack

``` text
Python
├── Pandas          → Data processing
├── NetworkX        → Graph construction and algorithms
├── Streamlit       → Interactive web application
└── PyVis / Plotly  → Graph visualization
```

## 🧩 Graph model

### Nodes
```text
Artist
Genre
Release
Label
``` 

### Edges

```text
Artist ── RELEASED ──> Release

Release ── RELEASED_BY ──> Label

Artist ── PLAYS ──> Genre

Genre ── SUBGENRE_OF ──> Genre

Artist ── SIMILAR_TO ──> Artist

Artist ── INFLUENCED ──> Artist
```

### 🔎 Features

#### Explore an artist
Select an artist and explore their musical ecosystem:

```text

Aphex Twin
├── Genres
├── Releases
├── Labels
├── Similar artists
└── Influences
```

#### Explore a genre

For example:

```
IDM
├── Aphex Twin
├── Autechre
├── Boards of Canada
├── Squarepusher
└── ...
```

#### Find connections
Find the shortest path between two artists.
For example:

```text

Aphex Twin
    ↓
Warp Records
    ↓
Autechre
```

or 

```text 

Aphex Twin
    ↓
IDM
    ↓
Autechre
```

This feature will make use of graph traversal and shortest-path algorithms.

## 📊 Initial scope

The first version will intentionally remain small.

Target dataset:

20–30 artists
10–15 genres
~10 labels
50–100 releases
The initial dataset could focus on:
IDM / Ambient Techno / Experimental Electronic

The graph can then be expanded once the core application is working.

## 🚀 Roadmap

### V1 — Core application

Fetch data from MusicBrainz

Fetch complementary data from Last.fm

Clean and normalize the data

Build the graph with NetworkX

Create the Streamlit interface

Display the interactive graph

Implement artist exploration

Implement genre exploration

Implement shortest-path search

### V2 — Graph database


Model the graph in Neo4j or GraphDB

Connect Neo4j or GraphDB to the Streamlit application

 
### V3 — Enrichment

Add Wikidata data

Add graph statistics

Add genre filtering

Add time-period filtering

Add artist recommendations

Explore graph centrality and communities

