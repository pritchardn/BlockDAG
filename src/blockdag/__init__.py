"""BlockDAG generator

This package contains code to build and compare BlockDAG in a lightweight-as-possible manner.
The main method (build_block_dag) performs a Kahn topological sort of the vertices (dict) and edges
(list of (u, v) tuples) building blocks for each vertex as needed.

"""
# pylint: disable=R0801
from blockdag.blockdag import *
