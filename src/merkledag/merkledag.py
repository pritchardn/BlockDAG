import json
import hashlib
import collections
from merklelib import MerkleTree


def _default_hash(value):
    return hashlib.sha256(value).hexdigest()


def _build_hash_payload(vertex: dict, data_fields, hash_function):
    data = []
    for key, val in vertex.items():
        if key in data_fields:
            data.append(val)
    mtree = MerkleTree(sorted(data), hash_function)
    return {'data_hash': mtree.merkle_root}


def _build_block_hash(data: dict, hash_function):
    hashes = []
    for _, val in data.items():
        if val is not None:
            if isinstance(val, list):
                hashes.extend(val)
            else:
                hashes.append(val)
    mtree = MerkleTree(sorted(hashes), hash_function)
    data['hash'] = mtree.merkle_root


def _generate_graph_signature(leaves: list, hash_function):
    hashes = []
    for leaf in leaves:
        hashes.append(leaf['hash'])
    mtree = MerkleTree(sorted(hashes), hash_function)
    return mtree.merkle_root


def build_merkle_dag(vertices: dict, edges: list, hash_function, data_fields, append_global=True,
                     append_hash=True, overwrite=True):
    dropset = {}
    workingset = {}
    outputset = {}
    neighbourset = {}
    leaves = []
    visited = []

    queue = collections.deque()

    for v_id, vertex in vertices.items():
        dropset[v_id] = [vertex, 0, 0]  # Data, in-degree, out-degree
        workingset[v_id] = [None, []]  # Block_data, Parent_hashes
        neighbourset[v_id] = []

    for src, dest in edges:
        dropset[dest][1] += 1
        dropset[src][2] += 1
        neighbourset[src].append(dest)

    for v_id in dropset:
        if dropset[v_id][1] == 0:
            queue.append(v_id)
        if not neighbourset[v_id]:
            leaves.append(v_id)

    while queue:
        v_id = queue.pop()
        workingset[v_id][0] = _build_hash_payload(dropset[v_id][0], data_fields, hash_function)
        hashes = {}
        hashes.update(workingset[v_id][0])
        hashes['parent_hashes'] = workingset[v_id][1]
        _build_block_hash(hashes, hash_function)
        outputset[v_id] = hashes
        visited.append(v_id)
        for neighbour in neighbourset[v_id]:
            dropset[neighbour][1] -= 1
            workingset[neighbour][1].append(outputset[v_id]['hash'])
            if dropset[neighbour][1] == 0:
                queue.append(neighbour)
    if len(visited) != len(dropset):
        raise AssertionError("Some vertices untraversed")

    leaf_vertices = []
    for leaf in leaves:
        leaf_vertices.append(outputset[leaf])
    outputset['signature'] = _generate_graph_signature(leaf_vertices, hash_function)
    return outputset


def compare_dags(vertices_1: dict, vertices_2: dict):
    # Assumes vertices_1 contains the hash signatures for this data
    if vertices_1['signature'] == vertices_2['signature']:
        # They match, no work to be done
        return True, [], []
    sigmap_1 = {}
    sigmap_2 = {}
    for key, val in vertices_1.items():
        if not isinstance(val, dict):
            continue
        sigmap_1[val['hash']] = key
    for key, val in vertices_2.items():
        if not isinstance(val, dict):
            continue
        sigmap_2[val['hash']] = key

    sigset_1 = set(sigmap_1.keys())
    sigset_2 = set(sigmap_2.keys())
    difs_1 = sigset_1.difference(sigset_2)
    difs_2 = sigset_2.difference(sigset_1)
    out_1 = []
    out_2 = []
    for sig in difs_1:
        out_1.append(sigmap_1[sig])
    for sig in difs_2:
        out_2.append(sigmap_2[sig])
    return False, sorted(out_1), sorted(out_2)


def pretty_print(vertices=None, edges=None, signatures=None, indent=4):
    if vertices:
        print("------\tVERTICES\t------")
        print(json.dumps(vertices, indent=indent))
    if edges:
        print("------\tEDGES\t------")
        print(json.dumps(edges, indent=indent))
    if signatures:
        print("------\tSIGNATURES\t------")
        print(json.dumps(signatures, indent=indent))


def pretty_prints(vertices=None, edges=None, signatures=None, indent=4):
    ret = ""
    if vertices:
        ret += "------\tVERTICES\t------\n"
        ret += json.dumps(vertices, indent=indent)
    if edges:
        ret += "------\tEDGES\t------\n"
        ret += json.dumps(edges, indent=indent)
    if signatures:
        ret += "------\tSIGNATURES\t------\n"
        ret += json.dumps(signatures, indent=indent)
    return ret
