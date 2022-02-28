"""
Runs a Binomial tree example which should take a few seconds to compute.
"""

import hashlib
from blockdag import build_block_dag, pretty_prints


def _hashfunc(value):
    return hashlib.sha256(value).hexdigest()


def _binomial_tree(size):
    num_nodes = 1
    edges = []
    vertices = {}
    for i in range(size):
        edges += [(edge[0] + num_nodes, edge[1] + num_nodes) for edge in edges]
        edges += [(0, num_nodes)]
        num_nodes *= 2
    for i in range(num_nodes):
        vertices[i] = {"data": i}
    return vertices, edges


def _main():
    data, edges = _binomial_tree(15)
    print(f"{len(data)} vertices\n{len(edges)} edges")
    sig = build_block_dag(data, edges, _hashfunc, ["data", "important"])
    print(pretty_prints(data, edges, sig))


if __name__ == "__main__":
    _main()
