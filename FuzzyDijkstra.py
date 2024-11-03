import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt

from Graph import Graph
from Vertex import Vertex


class FuzzyDijkstra:
    """Class to perform the fuzzy Dijkstra algorithm."""
    def __init__(self, graph):
        self.graph = graph

    def defuzzify(self, fuzzy_weight):
        """Defuzzification method to convert fuzzy weight to a crisp value."""
        a, b, c = fuzzy_weight
        return (a + 4 * b + c) / 6  # Centroid defuzzification

    def fuzzy_dijkstra(self, source):
        """Calculate shortest paths from the source to all vertices in the fuzzy graph."""
        dist = {v: float('inf') for v in self.graph.vertices}
        previous = {v: None for v in self.graph.vertices}
        dist[source] = 0
        unvisited = list(self.graph.vertices.keys())         \

        while unvisited:
            u = min(unvisited, key=lambda vertex: dist[vertex])
            if dist[u] == float('inf'):
                break

            unvisited.remove(u)

            for neighbor, fuzzy_weight in self.graph.vertices[u].edges:
                alt = dist[u] + self.defuzzify(fuzzy_weight)

                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    previous[neighbor] = u

        # visualize_graph(graph, distances, previous_nodes, source)
        visualize_graph(self.graph, dist, previous, source)
        return dist, previous

def visualize_graph(graph, distances=None, previous_nodes=None, source=None):
    G = nx.DiGraph()

    for vertex, edges in graph.vertices.items():
        for neighbor, fuzzy_weight in edges.edges:
            G.add_edge(vertex, neighbor, weight=1)

    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, width=2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    edge_labels = {}
    for vertex in graph.vertices:
        for neighbor, fuzzy_weight in graph.vertices[vertex].edges:
            edge_labels[(vertex, neighbor)] = f"{fuzzy_weight}"

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')


    if distances and previous_nodes and source:
        for vertex in graph.vertices:
            if previous_nodes[vertex] is not None:
                G[previous_nodes[vertex]][vertex]['color'] = 'orange'

        edges = G.edges(data=True)
        colors = ['orange' if 'color' in edge[2] else 'gray' for edge in edges]
        nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=20, width=2, edge_color=colors)

    plt.title("Fuzzy SPP using Dijkstra")
    plt.axis('off')
    plt.show()
