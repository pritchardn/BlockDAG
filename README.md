# BlockDAG
BlockDAGs for structured signature generation.

A [Merkle-Tree](https://en.wikipedia.org/wiki/Merkle_tree) is a binary tree of hash nodes.
This module implements an extension of this data-structure which differs in that:
- Data can be included at any node in the structure
- The structure between nodes can form a directed acyclic graph

Note, this is, in principle, a superset of a MerkleTree.

One creates a BlockDAG by providing a dictionary of vertices (id : dict()) 
and list of edges (id: id tuples).

## Usage

## Testing

## Contributions
Feel free to help out, submit issues and make merge requests.