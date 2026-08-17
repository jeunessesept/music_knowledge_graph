import networkx as nx
from pyvis.network import Network
from data.utils.helpers import get_node

NODE_STYLES = {
    "artist": {
        "color": "#EF476F",
        "shape": "dot",
        "size": 30
    },
    "genre": {
        "color": "#9B5DE5",
        "shape": "dot",
        "size": 20
    },
    "label": {
        "color": "#06D6A0",
        "shape": "box",
        "size": 22
    },
    "release_group": {
        "color": "#FFD166",
        "shape": "box",
        "size": 18
    },
    "release": {
        "color": "#8D99AE",
        "shape": "dot",
        "size": 12
    }
}


def get_node_label(node_id: str, node_data: dict) -> str:
    return (
        node_data.get("name")
        or node_data.get("title")
        or node_id
    )


def add_node_to_graph(
        graph: nx.DiGraph,
        node_id: str, 
        node_type: str,
        node_data: dict
) -> None:

    style = NODE_STYLES.get(node_type, {})

    graph.add_node(
        node_id,
        label= get_node_label(node_id, node_data),
        node_type=node_type,
        **style
    )


def build_networkx_graph(graph_data: dict) -> nx.DiGraph:
    graph = nx.DiGraph()

    for edge in graph_data["edges"]:
        source_id = edge["source"]
        source_type = edge["source_type"]

        target_id = edge["target"]
        target_type = edge["target_type"]

        source_data = get_node(
            graph_data,
            source_type,
            source_id
        )

        target_data = get_node(
            graph_data,
            target_type,
            target_id
        )

        if not source_data or not target_data:
            continue    

        add_node_to_graph(graph, source_id, source_type, source_data)
        add_node_to_graph(graph, target_id, target_type, target_data)
        graph.add_edge(source_id, target_id, relation=edge['type'], title=edge['type'])

    return graph


def get_artist_subgraph(
    graph: nx.DiGraph,
    artist_id: str,
    depth: int
) -> nx.DiGraph:
    if artist_id not in graph:
        return nx.DiGraph()

    return nx.ego_graph(
        graph,
        artist_id,
        radius=depth,
        undirected=True
    )

def create_pyvis_network(graph: nx.DiGraph) -> Network:
    network = Network(
        height="700px",
        width="100%",
        bgcolor="#111827",
        font_color="#F9FAFB",
        directed=True,
        cdn_resources="in_line"
    )

    network.from_nx(graph)

    network.set_options("""
    {
        "nodes": {
            "font": {
                "size": 14,
                "color": "#F9FAFB"
            }
        },
        "edges": {
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            },
            "color": {
                "color": "#6B7280"
            },
            "smooth": false
        },
        "physics": {
            "enabled": true,
            "stabilization": {
                "iterations": 150
            }
        }
    }
    """)

    return network


def generate_pyvis_html(graph: nx.DiGraph) -> str:
    network = create_pyvis_network(graph)

    return network.generate_html()

