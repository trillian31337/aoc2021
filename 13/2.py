from termcolor import colored
import re
import sys
import numpy as np

def create_matrix(coordinates):
	xmax = max([int(c[0]) for c in coordinates])
	ymax = max([int(c[1]) for c in coordinates])
	data = []
	for y in range(ymax+1):
		data.append([0]*(xmax+1))
	for c in coordinates:
		data[int(c[1])][int(c[0])] = 1
	paper = np.matrix(data)	
	return paper

def fold(paper, folding_instruction):
	dim = folding_instruction[0]
	value = int(folding_instruction[1])

	xlen = (paper.shape)[1]
	ylen = (paper.shape)[0]
	# create two matrixes
	if dim == 'x':
		part1 = paper[0:ylen+1,0:value]
		part2 = paper[0:ylen+1,value+1:xlen+1]
	else:
		part1 = paper[0:value,0:xlen+1]
		part2 = paper[value+1:ylen,0:xlen+1]

	# flip the lower/left part
	if dim == 'x':
		part2_flipped = np.flip(part2,1)
	else:
		part2_flipped = np.flip(part2,0)

	# add the matrixes	
	new_paper = part1 + part2_flipped
	return new_paper

def convert_dot(v):
	if v > 0:
		return 1
	else:
		return 0

def count_dots(paper):
	vconvert = np.vectorize(convert_dot)
	paper_visible_dots = vconvert(paper)
	print("Number of visible dots:")
	print(int(np.sum(paper_visible_dots,axis=(0,1))))
	return paper_visible_dots

def pretty_print_paper(paper):
	for iy, ix in np.ndindex(paper.shape):
		if ix == 0:
			print()
		if paper[iy, ix] == 1:
			print('#',end=' ')
		else:
			print('.',end=' ')
	print()
	print()

### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

f = open(fname)
y = 0
coordinates = []
folding_instructions = []
p1 = re.compile(r'^(\d+),(\d+)')
p2 = re.compile(r'^fold along ([xy])=(\d+)')
for line in f:
	m = p1.match(line.rstrip())
	if m != None:
		coordinates.append((m.group(1),m.group(2)))
	else:
		m = p2.match(line.rstrip())
		if m != None:
			folding_instructions.append((m.group(1),m.group(2)))
paper = create_matrix(coordinates)
for f in folding_instructions:
	new_paper = fold(paper,f)
	paper = new_paper
paper_visible_dots = count_dots(paper)
pretty_print_paper(paper_visible_dots)
