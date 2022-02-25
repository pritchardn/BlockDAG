[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

## Usage

## Requirements / Assumptions

- Vertex keys are assumed to be unique
- The fields 'hash' and 'signature' will be overwritten if `append_hashes` is set to `True`
- While it will not cause any issues, cycles will be ignored in the original graph.

## Testing

## Contributions
Feel free to help out, submit issues and make merge requests.