class Vertex:
    """Class to represent a vertex in the graph."""
    def __init__(self, name):
        self.name = name
        self.edges = []
    def add_edge(self, neighbor, fuzzy_weight):
        """Add an edge from this vertex to a neighbor with fuzzy weight."""
        self.edges.append((neighbor, fuzzy_weight))

