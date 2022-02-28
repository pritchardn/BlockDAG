"""BlockDAG generator

This package contains code to build and compare BlockDAG in a lightweight-as-possible manner.
The main method (build_block_dag) performs a Kahn topological sort of the vertices (dict) and edges
(list of (u, v) tuples) building blocks for each vertex as needed.

"""
import json
import hashlib
import collections.abc
from merklelib import MerkleTree


def _default_hash(value):
    return hashlib.sha256(value).hexdigest()


def _build_hash_payload(vertex: dict, data_fields, hash_function):
    data = []
    for key, val in vertex.items():
        if data_fields is not None:
            if key in data_fields:
                data.append(val)
        else:
            data.append(val)
    mtree = MerkleTree(data, hash_function)
    return {"data_hash": mtree.merkle_root}


def _build_block_hash(data: dict, hash_function):
    hashes = []
    for _, val in data.items():
        if val is not None:
            if isinstance(val, collections.Iterable):
                hashes.extend(val)
            else:
                hashes.append(val)
    mtree = MerkleTree(sorted(hashes), hash_function)
    data["hash"] = mtree.merkle_root


def _generate_graph_signature(leaves: list, hash_function):
    hashes = []
    for leaf in leaves:
        hashes.append(leaf["hash"])
    mtree = MerkleTree(sorted(hashes), hash_function)
    return mtree.merkle_root


def _check_args_build_block_dag(vertices, edges, data_fields, append_hashes):
    if not hasattr(data_fields, "__contains__") and data_fields is not None:
        raise AttributeError("data_fields object does not implement __contains__")
    if not hasattr(vertices, "__getitem__"):
        raise AttributeError("vertices object does not implement '__getitem__")
    if not isinstance(append_hashes, bool):
        raise AttributeError("append_hashes needs to be a boolean")
    if not isinstance(edges, collections.abc.Iterable):
        raise AttributeError("edges does not implement collections.Iterable")


def build_block_dag(
        vertices: dict,
        edges: list,
        hash_function=_default_hash,
        data_fields=None,
        append_hashes=False,
):
    """Builds and returns (optionally appending to the original data) BlockDAG signature data for a
    graph. Performs a Kahn topological sort of the vertices and edges, inclusively filtering by
    data_fields. The final signature is built by concatenating and sorting the hashes from each
    leaf in the graph, inserting them all into a Merkle Tree and taking the root.

    Parameters
    ----------
    vertices : dict
        A dictionary of vertex information.
    edges : list
        A list of (u, v) tuples containing the keys in the vertices.
    hash_function : function
        A function used to generate signatures throughout, as hex-digests.
    data_fields : list
        A list of keys used to inclusively filter data in all vertices.
        If none, will include all fields.
    append_hashes : bool, default=False
        If true, data hash data and will be appended to each vertex's value dictionary.
        The whole graph signature however, will not be added to the graph.

    Returns
    -------
    output_signatures : dict
        A dictionary containing the signature information for each vertex and for the whole graph.
    """
    _check_args_build_block_dag(vertices, edges, data_fields, append_hashes)
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

    for v_id, _ in dropset.items():
        if dropset[v_id][1] == 0:
            queue.append(v_id)
        if not neighbourset[v_id]:
            leaves.append(v_id)

    while queue:
        v_id = queue.pop()
        workingset[v_id][0] = _build_hash_payload(
            dropset[v_id][0], data_fields, hash_function
        )
        hashes = {}
        hashes.update(workingset[v_id][0])
        hashes["parent_hashes"] = workingset[v_id][1]
        _build_block_hash(hashes, hash_function)
        outputset[v_id] = hashes
        visited.append(v_id)
        for neighbour in neighbourset[v_id]:
            dropset[neighbour][1] -= 1
            workingset[neighbour][1].append(outputset[v_id]["hash"])
            if dropset[neighbour][1] == 0:
                queue.append(neighbour)
    if len(visited) != len(dropset):
        raise AssertionError("Some vertices untraversed")

    leaf_vertices = []
    for leaf in leaves:
        leaf_vertices.append(outputset[leaf])
    outputset["signature"] = _generate_graph_signature(leaf_vertices, hash_function)
    if append_hashes:
        for vid, vertex in vertices.items():
            vertex.update(outputset[vid])
    return outputset


def _check_args_compare_dags(vertices_1, vertices_2):
    if not hasattr(vertices_1, "__getitem__"):
        raise AttributeError("vertices_1 does not implement '__getitem__")
    if not hasattr(vertices_2, "__getitem__"):
        raise AttributeError("vertices_2 does not implement '__getitem__")
    if vertices_1.get("signature") is None:
        raise ValueError("vertices_1 does not contain 'signature' field")
    if vertices_2.get("signature") is None:
        raise ValueError("vertices_2 does not contain 'signature' field")


def compare_dags(vertices_1: dict, vertices_2: dict):
    """Compares two BlockDags and finds vertices which differ between them.

    Parameters
    ----------
    vertices_1 : dict
        The dictionary of the first BlockDAG containing all information built with build_hash_dag.
    vertices_2 : dict
        The dictionary of the first BlockDAG containing all information built with build_hash_dag.

    Returns
    -------
    identical : bool
        True if DAGs are identical, False otherwise.
    difference_list_1 : list
        List of vertex labels from the first set which differ.
    difference_list_2 : list
        List of vertex labels form the second set which differ.
    """
    # Assumes vertices_1 contains the hash signatures for this data
    _check_args_compare_dags(vertices_1, vertices_2)
    if vertices_1["signature"] == vertices_2["signature"]:
        # They match, no work to be done
        return True, [], []
    sigmap_1 = {}
    sigmap_2 = {}
    for key, val in vertices_1.items():
        if not hasattr(val, "__get__"):
            continue
        if val.get("hash") is not None:
            sigmap_1[val["hash"]] = key
        else:
            raise ValueError(f"Vertex {key} does not contain hash")
    for key, val in vertices_2.items():
        if not hasattr(val, "__get__"):
            continue
        if val.get("hash") is not None:
            sigmap_2[val["hash"]] = key
        else:
            raise ValueError(f"Vertex {key} does not contain hash")

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
    """Prints the given vertices, edges and generated signatures as an indented json dump

    Parameters
    ----------
    vertices : dict
        The dictionary of vertices to print
    edges : list
        The list of (u, v) tuples to print
    signatures : dict
        The dictionary of generated signatures (from build_block_dag)
    indent : int, default=True
        The level of json indentation
    """
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
    """Returns the string tht would be printed, edges and generated signatures as an indented json
    dump.

    Parameters
    ----------
    vertices : dict
        The dictionary of vertices to print
    edges : list
        The list of (u, v) tuples to print
    signatures : dict
        The dictionary of generated signatures (from build_block_dag)
    indent : int, default=True
        The level of json indentation
    """
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
