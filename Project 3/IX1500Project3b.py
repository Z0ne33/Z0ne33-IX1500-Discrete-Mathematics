import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt


cities = [
    "Abisko", "Boden", "Falun", "Goteborg", "Hoganas", "Hudiksvall", "Jonkoping",
    "Kalmar", "Kiruna", "Lidkoping", "Linkoping", "Lulea", "Lund", "Malmo", 
    "Mariestad", "Ostersund", "Stockholm", "Strangnas", "Timra", "Uppsala", 
    "Umea", "Varberg", "Visby"
]


links = [
    (15, 18), (13, 17), (3, 16), (6, 3), (18, 6), (12, 2), (15, 11), (19, 21), (7, 8),
    (19, 2), (7, 4), (21, 17), (17, 11), (23, 11), (10, 7), (16, 17), (10, 20),
    (13, 5), (3, 17), (7, 22), (15, 10), (16, 18), (11, 16), (17, 23), (18, 17),
    (20, 6), (11, 7), (9, 2), (3, 20), (4, 17), (19, 17), (7, 20), (22, 4), (14, 7),
    (15, 17), (6, 17), (20, 5), (16, 15), (11, 3), (9, 1), (4, 10), (5, 14), (6, 16),
    (16, 19), (13, 8), (8, 23), (16, 10), (4, 13), (2, 16), (15, 3), (20, 18)
]


links = [(u, v) for u, v in links if u < len(cities) and v < len(cities)]


capacity = {
    (17, 4): 25,   # Stockholm - Göteborg
    (17, 12): 30,  # Stockholm - Lund
    (4, 13): 25,   # Göteborg - Lund
    (17, 3): 15,   # Stockholm - Falun
    (3, 16): 15,   # Falun - Östersund
    (16, 21): 15   # Östersund - Umeå
}
weights = {}


for link in links:
    if link not in capacity and (link[1], link[0]) not in capacity:
        capacity[link] = random.randint(1, 10)


for link in links:
    if link in capacity:
        weights[link] = round(1 / capacity[link], 3)
    if (link[1], link[0]) in capacity:
         weights[link] = round(1 / capacity[(link[1], link[0])], 3)

G = nx.Graph()


for link, weight in weights.items():
    G.add_edge(cities[link[0] -1], cities[link[1] -1], weight=weight)
 



start_node = "Stockholm"


def dijkstra(graph, start):
    
    distances = {city: float('inf') for city in graph.nodes}
    distances[start] = 0
    visited = set()
    
    while len(visited) < len(graph.nodes):
       
        current_node = min((city for city in graph.nodes if city not in visited), 
                           key=lambda city: distances[city])

       
        visited.add(current_node)

        
        for neighbor, attributes in graph[current_node].items():
            weight = attributes['weight']
            if neighbor not in visited:
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    return distances





if start_node in G:
    shortest_paths = dijkstra(G, start_node)
    for city, distance in shortest_paths.items():
        print(f"Distance from {start_node} to {city}: {distance:.3f}")
else:
    print(f"Start node '{start_node}' not found in the graph.")


pos = nx.spring_layout(G, k=0.6, scale=5)  # Increasing 'k' spreads out the nodes

# Draw the graph with updated layout
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')

# Draw edge labels (weights)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.3f}" for k, v in edge_labels.items()})

plt.title("Graph Representation with Weights")
plt.show()