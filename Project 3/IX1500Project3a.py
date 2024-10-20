import networkx as nx
import matplotlib.pyplot as plt


def find(parent, i):
    while parent[i] != i:
        i = parent[i]
    return i


def union(parent, rank, x, y):
    rX = find(parent, x)
    rY = find(parent, y)


    if rank[rX] < rank[rY]:
        parent[rX] = rY
    elif rank[rX] > rank[rY]:
        parent[rY] = rX
    else:
        parent[rY] = rX
        rank[rX] += 1
def kruskal_mst(graph):
    edges = graph['edges']
    V = graph['vertices']

    
    edges = sorted(edges, key=lambda item: item[0])

    result = []  

    parent = []
    rank = []

   
    for node in range(V):
        parent.append(node)
        rank.append(0)

    
    for weight, u, v in edges:
        root_u = find(parent, u)
        root_v = find(parent, v)

        if root_u != root_v:
            result.append((u, v, weight))
            union(parent, rank, root_u, root_v)

        if len(result) == V - 1:
            break

    return result


def plot_graph_and_mst(graph, mst):
    G = nx.Graph()
    
    
    for weight, u, v in graph['edges']:
        G.add_edge(u, v, weight=weight)
    
    pos = nx.spring_layout(G)
    
    
    plt.figure(figsize=(8, 6))
    
    
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12, font_weight='bold')
    
    
    edge_labels = {(u, v): f'{weight}' for (weight, u, v) in graph['edges']}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

   
    mst_edges = [(u, v) for u, v, w in mst]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3, edge_color='green')

    plt.title("Graph with Minimum Spanning Tree (MST) Highlighted", size=15)
    plt.show()


graph = {
    'vertices': 6,
    'edges': [
        (10, 0, 1),
        (15, 0, 2),
        (5, 1, 3),
        (15, 2, 3),
        (4, 1, 2),
        (4, 4, 5),
        (7, 3, 5), 
        (1, 2, 5)
    ]
}


mst = kruskal_mst(graph)


print("Edges in the Minimum Spanning Tree:")
for u, v, weight in mst:
    print(f"Edge ({u}, {v}) with weight {weight}")


plot_graph_and_mst(graph, mst)
