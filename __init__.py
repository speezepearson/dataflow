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
    if attrs is None: attrs = {}
    result.add_node(id, type='store', **attrs)
  for (id, attrs) in j.get('processes', {}).items():
    if attrs is None: attrs = {}
    result.add_node(id, type='process', **attrs)

  for (src, outgoingss) in j.get('transfers', {}).items():
    if not result.has_node(src):
      raise KeyError('edge found with source {!r}, which corresponds to no node'.format(src))
    for (dst, outgoings) in outgoingss.items():
      if not result.has_node(dst):
        raise KeyError('edge found with destination {!r}, which corresponds to no node'.format(dst))
      for attrs in outgoings:
        result.add_edge(src, dst, **attrs)

  result.graph.update(j.get('attrs', {}))

  return result

def dataflow_to_cytoscape_json(g: DataflowGraph) -> dict:
  cyto = nx.DiGraph()
  for (id, attrs) in g.nodes.items():
    style = dict(attrs.get('cytoscape-style', {}))
    style.setdefault('label', attrs.get('label', attrs.get('datatype', id)))
    style.setdefault('shape', 'octagon' if attrs['type'] == 'store' else 'ellipse')
    style.setdefault('background-color', attrs.get('background-color', 'white'))
    style.setdefault('border-color', attrs.get('border-color', 'black'))
    style.setdefault('border-width', attrs.get('border-width', '1px'))
    cyto.add_node(id, style=style)
  for ((src, dst), attrs) in g.edges.items():
    style = dict(attrs.get('cytoscape-style', {}))
    style.setdefault('label', attrs.get('label', attrs.get('datatype', '')))
    cyto.add_edge(src, dst, style=style)

  result = nx.json_graph.cytoscape_data(cyto)['elements']
  for x in result['nodes'] + result['edges']:
    x['style'] = x['data'].pop('style')

  return result

def dataflow_graph_to_dot_graph(g: DataflowGraph) -> DotGraph:
  result = nx.DiGraph()
  for (id, attrs) in g.nodes.items():
    g_attrs = dict(attrs.get('graphviz-style', {}))
    g_attrs.setdefault('shape', 'cylinder' if attrs['type'] == 'store' else 'oval')
    g_attrs.setdefault('label', attrs.get('label', attrs.get('datatype', id)))
    result.add_node(id, **g_attrs)
  for ((src, dst), attrs) in g.edges.items():
    g_attrs = dict(attrs.get('graphviz-style', {}))
    g_attrs.setdefault('label', attrs.get('label', attrs.get('datatype', '')))
    result.add_edge(src, dst, **g_attrs)

  return DotGraph(result)

def graph_to_dot(g: DotGraph) -> str:
  pdg = nx.nx_pydot.to_pydot(g)
  for k, v in g.graph.items():
    pdg.set(k, v)
  return pdg.create_dot().decode()
