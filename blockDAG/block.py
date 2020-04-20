# Author: Nic Pritchard
import enum
import hashlib
import json
from dataclasses import dataclass, asdict
from enforce_typing import enforce_types


class Goal(enum.Enum):
    Rerun = 0
    Repeat = 1
    Reproduce = 2
    Replicate = 3


class PayloadType(enum.Enum):
    Genesis = 0
    Code = 1
    Data = 2
    Meta = 3


# @enforce_types
@dataclass
class Header:
    numparents: int
    parents: list
    payloadhash: str  # Generated at creation
    blockhash: str  # Hashing payloadhash and parent(s) together


# @enforce_types
@dataclass
class GenesisPayload:
    length: int
    data: str


# @enforce_types
@dataclass
class CodePayload:
    language: str
    runtime: str
    code: str
    versiontag: str


# @enforce_types
@dataclass
class DataPayload:
    length: int
    data: str


# @enforce_types
@dataclass
class MetaPayload:
    authors: str
    intitute: str
    goal: Goal


class Block(object):

    def __init__(self, numparents: int, parents: list, payload):
        if type(numparents) != int:
            raise TypeError("numparents must be int")
        if type(parents) != list:
            raise TypeError("parents needs to be a list of bytes objects")

        if type(payload) == GenesisPayload:
            self.ptype = PayloadType.Genesis
            if numparents != 0:
                raise ValueError("Genesis block must have no parents")
            if parents:
                raise ValueError("Genesis block must have no parents []")
        elif numparents <= 0:
            raise ValueError("Positive number of parents needed")
        else:
            all(isinstance(i, bytes) for i in parents)
        if type(payload) == CodePayload:
            self.ptype = PayloadType.Code
        elif type(payload) == DataPayload:
            self.ptype = PayloadType.Data
        elif type(payload) == MetaPayload:
            self.ptype = PayloadType.Meta

        # TODO: Change to Merkle Tree
        payhash = hashlib.sha3_256(json.dumps(asdict(payload), sort_keys=True).encode('utf-8')).hexdigest()
        headhash = hashlib.sha3_256((''.join(parents) + payhash).encode('utf-8')).hexdigest()
        self.header = Header(numparents, parents, payhash, headhash)
        # print(self.header.payloadhash)
        # print(self.header.blockhash)
        # print("-------- == --------")
