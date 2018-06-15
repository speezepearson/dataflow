import json
import sys

import networkx as nx

from . import nx_to_dot

print(nx_to_dot(nx.json_graph.node_link_graph(json.load(sys.stdin))))
