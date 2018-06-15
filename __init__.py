import copy

import networkx as nx
import pydot

def dataflow_graph_from_json_object(j: dict) -> nx.DiGraph:
  result = nx.DiGraph()
  for (id, attrs) in j.get('nodes', {}).items():
    if attrs['type'] not in {'store', 'process'}:
      raise ValueError('node {!r} does not have type=store or type=process'.format(id))
    result.add_node(id, **attrs)
  for (src, outgoings) in j.get('transfers', {}).items():
    for (dst, attrs) in outgoings.items():
      result.add_edge(src, dst, **attrs)
  return result

def dataflow_graph_to_dot_graph(g: nx.DiGraph) -> nx.DiGraph:
  result = copy.deepcopy(g)
  for (id, attrs) in result.nodes.items():
    if attrs['type'] == 'store':
      result.nodes[id]['shape'] = 'cylinder'
    if attrs.get('datatype'):
      result.nodes[id].setdefault('label', attrs['datatype'])
  return result

def nx_to_dot(g: nx.Graph) -> str:
  return nx.nx_pydot.to_pydot(g).create_dot().decode()
