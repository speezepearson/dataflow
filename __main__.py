import json
import sys

import networkx as nx

from . import (
  dataflow_graph_to_dot_graph,
  dataflow_graph_from_json_object,
  graph_to_dot,
)

print(
  graph_to_dot(
    dataflow_graph_to_dot_graph(
      dataflow_graph_from_json_object(
        json.load(sys.stdin)
      )
    )
  )
)
