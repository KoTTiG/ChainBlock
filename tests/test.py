import random
import json

import node as node
import block as block


def test_modules():
    test_nodes()
    test_blocks()


def test_nodes():
    test_node_init()
    test_node_with_blocks()


def test_blocks():
    test_first_block()
    test_next_block()
    test_json_block()


def test_node_init():
    server_id = random.randint(1, 3)
    new_node = node.Node(server_id)
    assert new_node is not None
    assert new_node.server_id == server_id
    assert new_node.block_index is None
    server_id = random.randint(1, 3)
    current_node = node.Node(server_id)
    genesis_block = block.create_genesis()
    assert current_node.server_id == server_id
    assert current_node.block_index is None
    current_node.block_handler(genesis_block)
    assert current_node.server_id == server_id
    assert current_node.block_index == 0
    node_server_id = random.randint(1, 3)
    current_node = node.Node(node_server_id)


def test_node_with_blocks():
    server_id = random.randint(1, 3)
    current_node = node.Node(server_id)
    for i in range(10):
        block_server_id = random.randint(1, 3)
        last_index = random.randint(1, 1000)
        prev_hash = 'This is Last block in Node'
        nonce_type = random.randint(1, 3)

        last_block_in_node_array = block.create_new_block(last_index, prev_hash, nonce_type,
                                                          block_server_id).block_to_json()
        current_node.block_index = last_index
        current_node.blocks_array.append(last_block_in_node_array)

        answer_false = current_node.block_handler(last_block_in_node_array)
        assert answer_false is False

        last_block_array_length = len(current_node.blocks_array)

        new_index = random.randint(1, 1000)
        new_prev_hash = 'This is new Received block'
        new_received_block = block.create_new_block(new_index, new_prev_hash, nonce_type,
                                                    block_server_id).block_to_json()

        answer_block_handler = current_node.block_handler(new_received_block)

        if new_index > last_index:
            assert answer_block_handler is True
            assert current_node.block_index == new_index
            assert len(current_node.blocks_array) == last_block_array_length + 1
        else:
            assert answer_block_handler is False
            assert current_node.block_index == last_index
            assert len(current_node.blocks_array) == last_block_array_length



def test_first_block():
    block_index = random.randint(1, 100000)
    nonce_type = 1
    prev_hash = 'old'
    server_id = random.randint(1, 3)
    new_block = block.Block(block_index, prev_hash, nonce_type, server_id)
    assert new_block is not None

    block_index = random.randint(1, 10000000)
    prev_hash = 'old block'
    nonce_type = 1
    server_id = random.randint(1, 3)
    new_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)
    assert new_block.index == block_index
    assert new_block.prev_hash == prev_hash
    assert new_block.index == block_index


def test_next_block():
    block_index = 1
    prev_hash = 'Old_data'
    nonce_type = 1
    server_id = 1
    current_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)
    old_value_data = current_block.data
    old_value_length = len(current_block.data)
    new_value_length = random.randint(0, 255)
    current_block.generate_random_data(new_value_length)
    assert old_value_length != len(current_block.data)
    assert old_value_data != current_block.data
    assert len(current_block.data) == new_value_length

    block_index = 1
    prev_hash = 'Old_Hash'
    nonce_type = 1
    server_id = 1
    current_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)
    assert type(current_block.hash) == str
    assert current_block.hash[-4:] == "0000"
    assert current_block.prev_hash == 'Old_Hash'


def test_json_block():
    block_index = random.randint(1, 100000)
    prev_hash = 'old block'
    nonce_type = random.randint(1, 3)
    server_id = random.randint(1, 3)
    new_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)
    json_block = new_block.block_to_json()
    python_object = json.loads(json_block)
    index = int(python_object['index'])
    cur_hash = python_object['hash']
    prev_hash = python_object['prev_hash']
    data = python_object['data']
    nonce = int(python_object['nonce'])
    assert index == new_block.index
    assert cur_hash == new_block.hash
    assert prev_hash == new_block.prev_hash
    assert data == new_block.data
    assert nonce == new_block.nonce

    genesis_block = block.create_genesis()
    python_object = json.loads(genesis_block)
    genesis_generated_by = python_object['Node '][0]
    genesis_index = int(python_object['index'])
    genesis_hash = python_object['hash']
    genesis_prev_hash = python_object['prev_hash']
    genesis_data = python_object['data']
    assert genesis_generated_by == -1
    assert genesis_index == 0
    assert genesis_hash[-4:] == "0000"
    assert genesis_prev_hash == 'GENESIS'
    assert len(genesis_data) == 256
