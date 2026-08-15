import networkx as nx
from pyvis.network import Network

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


