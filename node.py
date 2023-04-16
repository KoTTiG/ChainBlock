import json


class Node:
    blocks_array = []

    def __init__(self, server_id):
        self.server_id = server_id
        self.block_index = None

    def block_handler(self, received_block):
        if int(json.loads(received_block)['index']) == 0:
            self.blocks_array.append(received_block)
            self.block_index = 0
            return True
        if int(json.loads(received_block)['index']) > json.loads(self.blocks_array[-1])['index']:
            self.blocks_array.append(received_block)
            self.block_index = int(json.loads(received_block)['index'])
            return True
        return False

def block_to_string(json_block):
    index = int(json_block['index'])
    current_hash = json_block['hash']
    prev_hash = json_block['prev_hash']
    data = json_block['data']
    nonce = int(json_block['nonce'])
    gen_num = json_block['Node '][0]
    answ = f'Node [{gen_num}]:     Index = {index}, Hash = {current_hash}, ' \
           f'Prev_Hash = {prev_hash}, Data = {data}, Nonce = {nonce}'
    return answ
