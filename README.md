[![License: MIT](https://img.shields.io/badge/License-MIT-informational.svg)](https://opensource.org/licenses/MIT)
![Pylint: 10](https://github.com/pritchardn/BlockDAG/actions/workflows/pylint.yml/badge.svg)
![Tests: Passing](https://github.com/pritchardn/BlockDAG/actions/workflows/python-package.yml/badge.svg)

# BlockDAG
BlockDAGs for structured signature generation.

A [Merkle-Tree](https://en.wikipedia.org/wiki/Merkle_tree) is a binary tree of hash nodes.
This module implements an extension of this data-structure which differs in that:
- Data can be included at any node in the structure
- The structure between nodes can form a directed acyclic graph

Note, this is, in principle, a superset of a MerkleTree.

One creates a BlockDAG by providing a dictionary of vertices (id : dict()) 
and list of edges (id: id tuples).

For example (available in `examples/EX0.py`). Consider the following Graph:

<img src="https://github.com/pritchardn/BlockDAG/blob/main/img/ActualDAG.JPG"  />

Once processed, the following HashDAG is generated.

<img src="https://github.com/pritchardn/BlockDAG/blob/main/img/HashDAG.JPG"  />

Changing the values of a single vertex, or edges the graph signature will be completely different.
Moreover, the hashes of all descendent vertices will be completely different too.

The main method `build_block_dag` requires:
- A dictionary of vertices, each with a unqiue key, and dictionary of fields as values
- A list of tuples, describing the edges in the graph.
- A hash function (returns the hex-digest of the provided data. `Hashlib` provides many)
- A list of keys used to inclusively filter the data contained in each vertex. The values selected
are placed in a MerkleTree, the root of which is used as the `datahash` for that vertex
- A boolean, `append_hashes` which if True, will add the `hash` and graph `signature` to the 
original vertex dictionary.

`bulid_block_dag` returns a dictionary with the `datahash`, `parenthashes` and `blockhash` for each vertex
in the original graph, along with a whole-graph signature.

The whole-graph `signature` is computed by collecting the hashes of all leaf nodes (no outgoing edges)
then inserting them into a MerkleTree, and taking the root.

## Usage

Install it:

`pip install blockdag`

or clone it.

There are several examples in `examples` to get started.
You can compare blockdags to find differing vertices (by signature, not label) and print dags
nicely.

## Requirements / Assumptions

- Vertex keys are assumed to be unique
- The fields 'hash' and 'signature' will be overwritten if `append_hashes` is set to `True`
- While it will not cause any issues, cycles will be ignored in the original graph.

## Contributions
Feel free to help out, submit issues and make merge requests.