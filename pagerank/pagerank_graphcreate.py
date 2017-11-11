import graphlab as gl
from graphlab import SGraph, Vertex, Edge


f = open('web-Google.txt', 'r')
vertices = set()
edges = []

for line in f:
	v1, v2 = [int(x) for x in line.split()]
	vertices.add(v1)
	vertices.add(v2)
	edges.append(Edge(v1, v2))

print 'In total {0} vertices and {1} edges'.format(len(vertices), len(edges))
g = SGraph().add_vertices([Vertex(x) for x in vertices]).add_edges(edges)

g.save('page_graph')
