import json
import random
import string
from hashlib import sha256
import time


class Block:
    def __init__(self, index, prev_hash, nonce_type, server_id):
        self.hash = None
        self.data = None
        self.index = index
        self.server_id = server_id,
        self.prev_hash = prev_hash
        self.nonce = 1
        self.generate_random_data(256)
        self.generate_hash(nonce_type)
        self.timestamp = time.time()

    def generate_random_data(self, length):
        self.data = ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def generate_hash(self, nonce_type):
        c_string = str(self.index) + self.prev_hash + self.data + str(self.nonce)
        c_hash = sha256(c_string.encode('utf-8'))
        while c_hash.hexdigest()[-4:] != "0000":
            self.nonce += random.randint(1, 30)
            c_string = str(self.index) + self.prev_hash + self.data + str(self.nonce)
            c_hash = sha256(c_string.encode('utf-8'))
        self.hash = c_hash.hexdigest()

    def block_to_json(self):
        jsondict = {
            'Node ': self.server_id,
            'index': self.index,
            'hash': self.hash,
            'prev_hash': self.prev_hash,
            'data': self.data,
            'nonce': self.nonce
        }
        return json.dumps(jsondict)


def create_genesis():
    return create_new_block(0, 'GENESIS', 1, -1).block_to_json()


def create_new_block(index, _prev_hash, nonce_type, server_id):
    return Block(index, _prev_hash, nonce_type, server_id)
