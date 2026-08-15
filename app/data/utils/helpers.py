NODE_TYPES = {
    "artist": "artists",
    "genre": "genres",
    "label": "labels",
    "release_group": "release_groups",
    "area": "areas"
}


def get_node(graph, node_type, node_id):
    collection = NODE_TYPES[node_type]
    return graph["nodes"][collection].get(node_id)