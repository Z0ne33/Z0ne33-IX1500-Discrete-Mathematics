import heapq
import random
import networkx as nx
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="sweden_city_locator")

cities = [
    "Abisko", "Boden", "Falun", "Goteborg", "Hoganas", "Hudiksvall", "Jonkoping",
    "Kalmar", "Kiruna", "Lidkoping", "Linkoping", "Lulea", "Lund", "Malmo", 
    "Mariestad", "Ostersund", "Stockholm", "Strangnas", "Timra", "Uppsala", 
    "Umea", "Varberg", "Visby"
]

# Fetch coordinates
city_coordinates = {}
for city in cities:
    location = geolocator.geocode(city + ", Sweden")
    if location:
        city_coordinates[city] = (location.latitude, location.longitude)
    else:
        print(f"Could not find coordinates for {city}")

links = [
    (15, 18), (13, 17), (3, 16), (6, 3), (18, 6), (12, 2), (15, 11), (19, 21), (7, 8),
    (19, 2), (7, 4), (21, 17), (17, 11), (23, 11), (10, 7), (16, 17), (10, 20),
    (13, 5), (3, 17), (7, 22), (15, 10), (16, 18), (11, 16), (17, 23), (18, 17),
    (20, 6), (11, 7), (9, 2), (3, 20), (4, 17), (19, 17), (7, 20), (22, 4), (14, 7),
    (15, 17), (6, 17), (20, 5), (16, 15), (11, 3), (9, 1), (4, 10), (5, 14), (6, 16),
    (16, 19), (13, 8), (8, 23), (16, 10), (4, 13), (2, 16), (15, 3), (20, 18)
]



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
    if (link[0], link[1]) in capacity:
        weights[link] = round(1 / capacity[(link[0], link[1])], 3)
    elif (link[1], link[0]) in capacity:
        weights[link] = round(1 / capacity[(link[1], link[0])], 3)

G = nx.Graph()
for link, weight in weights.items():
    G.add_edge(cities[link[0] - 1], cities[link[1] - 1], weight=weight)

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


sweden_map = folium.Map(location=[63.0, 18.0], zoom_start=5)

for city, coords in city_coordinates.items():
    folium.Marker(location=coords, popup=city).add_to(sweden_map)


for link in links:
    city1 = cities[link[0] - 1]
    city2 = cities[link[1] - 1]
    folium.PolyLine(
        locations=[city_coordinates[city1], city_coordinates[city2]], 
        color='blue', 
        weight=2.5, 
        opacity=0.5
    ).add_to(sweden_map)


sweden_map.save('sweden_cities_map.html')

print("Map saved as 'sweden_cities_map.html'")
