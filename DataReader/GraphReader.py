import pandas as pd
import networkx as nx

source = "sourcepage"
rebuttal = "rebuttalpage"
data = pd.read_csv("out.tab", sep="\t", header=0, usecols=[source, rebuttal])
graph = nx.DiGraph()
edges = zip(data[rebuttal], data[source])
graph.add_edges_from(edges)
graph2 = nx.Graph(graph)

comps = nx.connected_components(graph2)
comps_sorted = sorted(comps, key=len, reverse=True)
nodes = list()
maxs = list()

#Get the 25 largest components
for i in range(25):
    max = 0
    node_max = ""
    for node in comps_sorted[i]:
        if graph.in_degree(node) > max:
            node_max = node
            max = graph.in_degree(node)
    nodes.append(node_max)
    maxs.append(max)
zip_list = zip(nodes, maxs)
zip_sort = sorted(zip_list, key=lambda x: x[1], reverse=True)

#Get the 10 nodes with the highest in degree
file = open("output.txt", 'w')
for i in range(10):
    pair = zip_sort[i]
    file.write("new node\n")
    file.write(pair[0] + "\n")
    file.write("list\n")
    for n in graph.predecessors(pair[0]):
        file.write(n + "\n")
