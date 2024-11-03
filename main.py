import json
import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt


from Graph import Graph
from Vertex import Vertex
from FuzzyDijkstra import FuzzyDijkstra



# Pengaturan GUI
def run_dijkstra():
    json_data = json_input.get("1.0", tk.END).strip()
    source = source_entry.get().strip()

    # Validasi JSON
    try:
        graph = Graph()
        graph.load_from_json(json_data)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Format JSON invalid.")
        return

    # Validasi node asal
    if source not in graph.vertices:
        messagebox.showerror("Error", f"Node '{source}' tidak terdapat pada graph.")
        return

    # jalankan Fuzzy Dijkstra
    fuzzy_dijkstra = FuzzyDijkstra(graph)
    distances, previous_nodes = fuzzy_dijkstra.fuzzy_dijkstra(source)

    # Tambilkan hasil
    result_text = f"Jarak terpendek dari {source}:\n"
    for vertex, distance in distances.items():
        result_text += f"Jarak ke {vertex}: {distance}\n"
    result_text += "\nNode-node sebelumnya di lintasan terpendek:\n"
    for vertex, prev in previous_nodes.items():
        result_text += f"Node sebelum {vertex}: {prev}\n"

    result_display.delete("1.0", tk.END)
    result_display.insert(tk.END, result_text)


# Bagian setup window
root = tk.Tk()
root.title("Fuzzy Dijkstra")
root.geometry("700x600")

# Bagian input graph dalam JSON
tk.Label(root, text="Masukkan graph dalam format JSON:").pack()
json_input = scrolledtext.ScrolledText(root, width=80, height=10)
json_input.pack()

# Bagian input node asal
tk.Label(root, text="Node asal:").pack()
source_entry = tk.Entry(root, width=20)
source_entry.pack()

# Tombol run
run_button = tk.Button(root, text="Jalankan Fuzzy Dijkstra", command=run_dijkstra)
run_button.pack(pady=10)

# Tampilkan hasil
tk.Label(root, text="Hasil:").pack()
result_display = scrolledtext.ScrolledText(root, width=80, height=15)
result_display.pack()

root.mainloop()