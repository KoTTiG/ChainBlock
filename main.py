
import argparse
import server
import node
from gevent import monkey

monkey.patch_all()
if __name__ == '__main__':
    pars = argparse.ArgumentParser()
    pars.add_argument('server_id', nargs='?')
    args = pars.parse_args().server_id
    current_node = node.Node(int(args))
    server.start(int(args), current_node)