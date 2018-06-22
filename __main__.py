import argparse
import json
import sys

import networkx as nx

from . import (
  dataflow_graph_to_dot_graph,
  dataflow_to_cytoscape_json,
  dataflow_graph_from_json_object,
  graph_to_dot,
)

CONVERTERS = {
  'graphviz': (lambda dfg: graph_to_dot(dataflow_graph_to_dot_graph(dfg))),
  'cytoscape': (lambda dfg: json.dumps(dataflow_to_cytoscape_json(dfg))),
}

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--to', choices=list(sorted(CONVERTERS.keys())), default='graphviz')
args = parser.parse_args()

converter = CONVERTERS[args.to]
dfg = dataflow_graph_from_json_object(json.load(sys.stdin))

print(converter(dfg))
