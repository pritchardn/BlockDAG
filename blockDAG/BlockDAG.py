# Author: Nic Pritchard
import networkx as nx
from block import Block, PayloadType, GenesisPayload, DataPayload


def build_data_payload(content):
    """
    Takes arbitrary data and returns a data payload ready for insertion into a full block
    :param content: Arbitrary data
    :return: DataPayload containing the arbitrary data
    """
    pass


class BlockDAG(object):
    pass