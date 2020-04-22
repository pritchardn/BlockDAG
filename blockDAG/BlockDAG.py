# Author: Nic Pritchard
import networkx as nx
import json
from block import Block, DataPayload


def build_data_payload(content) -> DataPayload:
    """
    Takes arbitrary data and returns a data payload ready for insertion into a full block
    :param content: Arbitrary data
    :return: DataPayload containing the arbitrary data
    """
    data = json.dumps(content, sort_keys=True)
    return DataPayload(len(data), data)


class BlockDAG(object):
    """
    A basic implementation of a BlockDAG.
    Can be viewed as a MerkleDAG with reversed links
    Can also be viewed as a Blockchain with DAG properties.
    Unlike a MerkleDAG however, the links are built dynamically; not setup and committed as separate stages.

    # TODO: Turn off cascading, forcing leaf-only growth
    # TODO: Support for all block-types
    """

    def __init__(self):
        self.new_node_name = 0
        self.graph = nx.DiGraph()

    def __generate_hash__(self, node):
        """
        For a given node, updates its hash-status by collecting all immediate parents.
        :param node: The candidate node
        :return: None
        """
        # Collect hashes of parents of node
        parents = nx.ancestors(self.graph, node)
        numparents = len(parents)
        parenthashes = []
        for elem in parents:
            parenthashes.append(self.graph.nodes[elem]['block'].header.blockhash)
        self.graph.nodes[node]['block'].update_parents(numparents, parenthashes)
        for child in nx.neighbors(self.graph, node):
            self.__generate_hash__(child)

    def add_node(self, data) -> int:
        """
        Adds a node to the blockDAG.
        Note: A node needs edges to be included in the blockDAG.
        :return: -1 if data is unsupported, int otherwise (node's label)
        """
        if data is None:
            return -1
        payload = build_data_payload(data)
        self.graph.add_node(self.new_node_name,
                            block=Block(payload),
                            name=self.new_node_name)
        self.new_node_name += 1
        return self.new_node_name - 1

    def add_edge(self, u: int, v: int) -> bool:
        """
        Adds an edge to the blockDAG u -> v.
        Cascades updates down through the DAG to the leaves.
        :return: False upon failure, True otherwise
        """
        if not self.graph.has_node(u) or not self.graph.has_node(v):
            print("Nodes do not exist yet, need to be created with content first")
            return False
        else:
            self.graph.add_edge(u, v)
            if not nx.is_directed_acyclic_graph(self.graph):
                print("Change created a loop, reconsider")
                self.graph.remove_edge(u, v)
                return False
            self.__generate_hash__(v)
            return True


x = BlockDAG()
a = x.add_node("test")
b = x.add_node("potato")
x.add_edge(a, b)
c = x.add_node(45)
x.add_edge(c, b)
x.add_edge(c, a)
