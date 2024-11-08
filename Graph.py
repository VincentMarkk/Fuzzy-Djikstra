import json
from Vertex import Vertex
class Graph:
    """Class to represent the graph."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name):
        """Add a vertex to the graph."""
        self.vertices[name] = Vertex(name)

    def add_edge(self, u, v, fuzzy_weight):
        """Add an edge between two vertices with fuzzy weight."""
        # u : source, v : destination
        if u not in self.vertices:
            self.add_vertex(u)
        if v not in self.vertices:
            self.add_vertex(v)
        self.vertices[u].add_edge(v, fuzzy_weight) # directed graph
        self.vertices[v].add_edge(u, fuzzy_weight) # directed graph

    def load_from_json(self, json_string):
        """Load the graph from a JSON string."""
        graph_data = json.loads(json_string)
        for u, edges in graph_data.items():
            for v, fuzzy_weight in edges:
                self.add_edge(u, v, fuzzy_weight)
