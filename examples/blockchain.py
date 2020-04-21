"""
We shall start with the most trivial case; a block-chain implementing transactions.
Here to demonstrate our block implementation flexibility.
Inspired by https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
"""

from block import Block, PayloadType, DataPayload, GenesisPayload
import time
import json


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.entries = []
        self.head_index = 0
        # Create a genesis block
        self.new_block(PayloadType.Genesis)

    def new_block(self, btype: PayloadType):
        # Creates a new block and adds it to the chain
        prev_hash = None
        if btype == PayloadType.Data:
            prev_hash = self.chain[-1].header.blockhash
        elif btype == PayloadType.Genesis:
            prev_hash = '0x0'
        else:
            raise ValueError("Only data and genesis blocks supported")
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'entries': self.entries,
            'previous_hash': prev_hash
        }
        data = json.dumps(block)
        newb = None
        if btype == PayloadType.Data:
            dataload = DataPayload(len(data), data)
            newb = Block(1, [self.chain_head.header.blockhash], dataload)
            newb.update_hash()
        elif btype == PayloadType.Genesis:
            dataload = GenesisPayload(len(data), data)
            newb = Block(0, [], dataload)
            newb.update_hash()
        self.entries = []
        self.chain.append(newb)
        self.head_index += 1
        return newb

    def new_entry(self, sender, recipient, amount):
        # Adds a new entry to be processed into a block
        self.entries.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.head_index + 1

    @property
    def chain_head(self):
        # Returns the last block in the chain
        return self.chain[-1]


exchain = Blockchain()
exchain.new_entry('Me', 'You', 100)
exchain.new_entry('You', 'Them', 50)
exchain.new_block(PayloadType.Data)