import copy

from typing import NewType

import networkx as nx
import pydot

DataflowGraph = NewType('DataflowGraph', nx.DiGraph)
DotGraph = NewType('DotGraph', nx.DiGraph)

def dataflow_graph_from_json_object(j: dict) -> DataflowGraph:
  result = DataflowGraph(nx.DiGraph())

  duplicate_node_ids = set(j.get('stores', {}).keys()) & set(j.get('processes', {}).keys())
  if duplicate_node_ids:
    raise ValueError('node ids {} are given as both stores and values'.format(duplicate_node_ids))
  for (id, attrs) in j.get('stores', {}).items():
    result.add_node(id, type='store', **attrs)
  for (id, attrs) in j.get('processes', {}).items():
    result.add_node(id, type='process', **attrs)

  for (src, outgoingss) in j.get('transfers', {}).items():
    for (dst, outgoings) in outgoingss.items():
      for attrs in outgoings:
        result.add_edge(src, dst, **attrs)

  return result

def dataflow_graph_to_dot_graph(g: DataflowGraph) -> DotGraph:
  result = copy.deepcopy(g)
  for (id, attrs) in result.nodes.items():
    if attrs['type'] == 'store':
      result.nodes[id]['shape'] = 'cylinder'
    if attrs.get('datatype'):
      result.nodes[id].setdefault('label', attrs['datatype'])
  return DotGraph(result)

def graph_to_dot(g: DotGraph) -> str:
  return nx.nx_pydot.to_pydot(g).create_dot().decode()
