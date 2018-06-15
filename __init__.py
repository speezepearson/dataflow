import networkx as nx
import pydot

def nx_to_dot(g: nx.Graph) -> str:
  return nx.nx_pydot.to_pydot(g).create_dot().decode()
