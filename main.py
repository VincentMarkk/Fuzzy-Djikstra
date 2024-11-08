import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt

from Graph import Graph
from Vertex import Vertex
from FuzzyDijkstra import FuzzyDijkstra

def reconstruct_path(previous, source, target):
    path = []
    while target is not None:
        path.insert(0, target) 
        target = previous[target]
    return path if path[0] == source else []  


def run_dijkstra():
    json_data = json_input.get("1.0", tk.END).strip()
    source = source_entry.get().strip()
    # Validate JSON input
    try:
        graph = Graph()
        graph.load_from_json(json_data)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Format JSON invalid.")
        return
    if source not in graph.vertices:
        messagebox.showerror("Error", f"Node '{source}' tidak terdapat pada graph.")
        return
        
    # Run Fuzzy Dijkstra
    fuzzy_dijkstra = FuzzyDijkstra(graph)
    distances, previous_nodes = fuzzy_dijkstra.fuzzy_dijkstra(source)

    result_text = f"Jarak/waktu terpendek dari {source}:\n\n"
    for vertex, distance in distances.items():
        path = reconstruct_path(previous_nodes, source, vertex)
        if path: 
            route_str = ' -> '.join(path)  
            result_text += f"Jarak/waktu ke {vertex}: {distance:.2f}, dengan rute {route_str}\n"  
        else:
            result_text += f"Jarak/waktu ke {vertex}: {distance:.2f}, tidak ada rute dari {source} ke {vertex}.\n"

    result_display.delete("1.0", tk.END)
    result_display.insert(tk.END, result_text)

# Main GUI setup
root = tk.Tk()
root.title("Fuzzy Dijkstra")
root.geometry("700x600")

# Input section for JSON graph
tk.Label(root, text="Masukkan graph dalam format JSON:").pack()
json_input = scrolledtext.ScrolledText(root, width=80, height=10)
json_input.pack()

# Input for source node
tk.Label(root, text="Node asal:").pack()
source_entry = tk.Entry(root, width=20)
source_entry.pack()

# Button to run Fuzzy Dijkstra
run_button = tk.Button(root, text="Jalankan Fuzzy Dijkstra", command=run_dijkstra)
run_button.pack(pady=10)

# Display area for results
tk.Label(root, text="Hasil:").pack()
result_display = scrolledtext.ScrolledText(root, width=80, height=20)
result_display.pack()

root.mainloop()