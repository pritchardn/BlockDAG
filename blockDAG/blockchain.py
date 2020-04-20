"""
We shall start with the most trivial case; a block-chain implementing transactions.
Here to demonstrate our block implementation flexibility.

"""

from block import *
import time
import json


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.entries = []
        # Create a genesis block
        self.new_block(PayloadType.Genesis)

    def new_block(self, btype: PayloadType):
        # Creates a new block and adds it to the chain
        if btype == PayloadType.Data or btype == PayloadType.Genesis:
            block = {
                'index': len(self.chain) + 1,
                'timestamp': time.time(),
                'entries': self.entries,
                'previous_hash': self.chain[-1].Header.blockhash
            }
            data = json.dumps(block).encode('utf-8')
            dataload = DataPayload(len(data), data)
            newb = Block(1, [self.chain_head], dataload)
            self.entries = []
            self.chain.append(newb)
            return newb
        else:
            raise ValueError("Only data and genesis blocks supported")

    def new_entry(self, sender, recipient, amount):
        # Adds a new entry to be processed into a block
        self.entries.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.chain_head['index'] + 1

    @property
    def chain_head(self):
        # Returns the last block in the chain
        return self.chain[-1]
