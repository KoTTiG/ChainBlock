from flask import Flask, request
import time
import threading
import grequests
import json
import block


def start(server_id, current_node):
    current_server = Flask(__name__)
    if server_id == 1:
        current_port = 2000
        port2 = 2001
        port3 = 2002
    elif server_id == 2:
        current_port = 2001
        port2 = 2000
        port3 = 2002
    else:
        current_port = 2002
        port2 = 2000
        port3 = 2001
    servers_urls = [f'http://localhost:{current_port}/', f'http://localhost:{port2}/', f'http://localhost:{port3}/']

    def new_blocks_generator():
        while True:
            if len(current_node.blocks_array) != 0:
                prev_hash = json.loads(current_node.blocks_array[-1])['hash']
                new_block = block.create_new_block(current_node.block_index + 1, prev_hash, current_node.server_id, server_id)
                if new_block.index > current_node.block_index:
                    grequests.map((grequests.post(u, json=new_block.block_to_json()) for u in servers_urls))
            time.sleep(0.5)

    @current_server.route("/", methods=['POST'])
    def server_handler():
        if not current_node.block_handler(request.get_json()):
            return "Error"
        return "new Block"
    current_server = threading.Thread(target=current_server.run, args=('localhost', current_port))
    current_server_generator = threading.Thread(target=new_blocks_generator)
    current_server.setDaemon(False)
    current_server_generator.setDaemon(False)
    current_server.start()
    current_server_generator.start()
    if server_id == 1:
        time.sleep(1)
        genesis_block = block.create_genesis()
        rs = (grequests.post(u, json=genesis_block) for u in servers_urls)
        grequests.map(rs)