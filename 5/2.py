#!/usr/bin/python3
import sys
from termcolor import colored

def create_grid(coords):
	grid = {}
	# find coord max value x, y
	xmax = 0
	ymax = 0
	for start,end in coords:
		if start[0] > xmax:
			xmax = start[0]
		if end[0] > xmax:
			xmax = end[0]	
		if start[1] > ymax:
			ymax = start[1]
		if end[1] > ymax:
			ymax = end[1]	
	# initialize grid with zeroes
	for x in range(xmax+2):
		for y in range(ymax+2):
			grid[(x,y)] = 0
	return grid,xmax,ymax

def pretty_print_grid(grid,xmax,ymax):
	for y in range(ymax+1):
		for x in range(xmax+1):
			if grid[(x,y)] > 0:
				print(colored(str(grid[(x,y)]).rjust(2), 'yellow'),end='')
			else:
				print(colored(str(grid[(x,y)]).rjust(2), 'green'),end='')
			print(' ',sep='',end='')
		print('')
	print()

def parse_coords(coord_string):
	return tuple([int(a) for a in coord_string.split(',')])

def add_line_to_grid(grid,start,end):
	#print(start)
	#print(end)
	if start[0] < end[0]:
		xpos1 = start[0]
		xpos2 = end[0]
	else:
		xpos1 = end[0]
		xpos2 = start[0]
	if start[1] < end[1]:
		ypos1 = start[1]
		ypos2 = end[1]
	else:
		ypos1 = end[1]
		ypos2 = start[1]
	if start[0] == end[0] or start[1] == end[1]:
		# vertical or horizontal line
		for x in range(xpos1,xpos2+1):
			for y in range(ypos1,ypos2+1):
				#print("adding to coord: %d,%d" % (x,y))
				grid[(x,y)] += 1 
	else:
		# diagonal
		xcoords = []
		ycoords = []
		for i in range(abs(start[0]-end[0])+1):
			if start[0] < end[0]:
				xcoords.append(start[0]+i)
			else:
				xcoords.append(start[0]-i)
			if start[1] < end[1]:
				ycoords.append(start[1]+i)
			else:
				ycoords.append(start[1]-i)
		print("xcoords",xcoords)
		print("ycoords",ycoords)
		for i in range(len(xcoords)):
			grid[(xcoords[i],ycoords[i])] += 1

	return grid

def count_overlaps(grid):
	count = 0
	for c in grid:
		if grid[c] > 1:
			count +=1
	return count

### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

f = open(fname)

coords = []
for line in f:
	coords.append([parse_coords(c) for c in line.rstrip().split(' -> ')])
grid,xmax,ymax = create_grid(coords)
print("grid size: %dx%d" % (xmax,ymax))
for start,end in coords:
	grid = add_line_to_grid(grid,start,end)
	pretty_print_grid(grid,xmax,ymax)
danger = count_overlaps(grid) 
print("Overlapping points:",danger)
 

