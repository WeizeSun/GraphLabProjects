import graphlab as gl

g = gl.load_sgraph('page_graph')

N = len(g.vertices)
beta = 0.02
epsilon = 150

f = open('topk_weight', 'w')

g.vertices['weight'] = 1.0
g.vertices['degree'] = 0

def increment_degree(src, edge, dst):
	src['degree'] += 1
	return (src, edge, dst)

def increment_weight(src, edge, dst):
	dst['weight_new'] += src['weight'] / src['degree']
	return (src, edge, dst)
	
g = g.triple_apply(increment_degree, mutated_fields=['degree'])

while True:
	g.vertices['weight_new'] = 0
	g.triple_apply(increment_weight, mutated_fields=['weight_new'])
	g.vertices['weight_new'] = beta / N + (1 - beta) * (g.vertices['weight_new'] + sum(g.vertices['weight'] - g.vertices['weight_new']) / N)
	diff = sum((g.vertices['weight'] - g.vertices['weight_new']) ** 2)
	g.vertices['weight'] = g.vertices['weight_new']
	print 'Now the diff is {0}'.format(diff)
	if diff < epsilon:
		break

topk_weight = g.vertices.topk('weight', k=100)['__id']
for i in topk_weight:
	f.write(str(i) + '\n')

f.close()