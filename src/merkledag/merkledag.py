import collections

def _build_hash_payload(vertex: dict, data_fields):
    return {'data_hash': b''}

def build_merkle_dag(vertices: dict, edges: dict, hash_function: function, data_fields, append_global=True, append_hash=True, overwrite=True):
    dropset = {}
    outputset = {}
    neighbourset = {}
    leaves = []
    visited = []

    queue = collections.deque()

    for id, vertex in vertices.items():
        dropset[id] = [vertex, 0, 0]  # Data, in-degree, out-degree
        outputset[id] = [None, []]  # Block_data, Parent_hashes
        neighbourset[id] = []

    for u, v in edges.items():
        dropset[u][1] += 1
        dropset[v][1] += 1
        neighbourset[u].append(v)

    for id in dropset:
        if dropset[id][1] == 0:
            queue.append(id)
        if not neighbourset[id]:
            leaves.append(id)

    while queue:
        id = queue.pop()
        outputset[id][0] = _build_hash_payload(dropset[id][0], data_fields)
        visited.append(id)
        for neighbour in neighbourset[id]:
            current_neighbour = dropset[neighbour][0]
            dropset[neighbour][1] -= 1
            # TODO: Add parent hash

            if dropset[neighbour][1] == 0:
                queue.append(neighbour)

    if len(visited) != len(dropset):
        raise AssertionError("Some vertices untraversed")

    # TODO: Generate signature


def compare_dags(vertices_1, edges_1, vertices_2, edgeS_2):
    pass

def verify_leaf_inclusion(vertices, edges):
    pass

def pretty_print(vertices, edges):
    pass