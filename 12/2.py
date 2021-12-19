#!/usr/bin/python3
import sys
from termcolor import colored
import networkx as nx
from copy import deepcopy

def is_wrong_way(node,path):
	if node in path and node.islower():
		lowerlist = [n for n in path if n.islower() and n != 'start']
		counts = {n:lowerlist.count(n) for n in lowerlist}
		for n in counts:
			if counts[n] > 1:
				return True
	return False


def path_finder(node,path,G):
	global paths
	edges = G.edges(node)
	for p in edges:
		if p[1] == 'end':
			path_copy = deepcopy(path)
			path_copy.append(p[1])
			paths.append(path_copy)
		elif node != 'start' and is_wrong_way(p[1],path):
			pass
		else:
			path_copy = deepcopy(path)
			path_copy.append(p[1])
			path_finder(p[1],path_copy,G)


### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
elif len(sys.argv) > 1 and sys.argv[1] == "test2":
	fname  ='input_test2'	
elif len(sys.argv) > 1 and sys.argv[1] == "test3":
	fname  ='input_test3'	
else:
   fname = 'input'

f = open(fname)
G = nx.DiGraph()
paths = []
for line in f:
	path = line.rstrip().split('-')
	for n in path:
		# if not already in graph, add node
		G.add_node(n)
	# add edge, skip edges between small caves
	if 'start' in path or 'end' in path:
		if path[0] == 'start' or path[1] == 'end':
			G.add_edge(path[0],path[1])
		elif path[1] == 'start' or path[0] == 'end':
			G.add_edge(path[1],path[0])
	else:
		G.add_edge(path[0],path[1])
		G.add_edge(path[1],path[0])
path_finder('start',['start'],G)
print("number of unique paths:", len(paths))
