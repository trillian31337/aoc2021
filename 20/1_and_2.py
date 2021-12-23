# Usage:
# python3 1_and_2.py <steps>
# For part 1:
# python3 1_and_2.py 2
# For part 2:
# python3 1_and_2.py 50
import sys
from copy import deepcopy

# add two columns/rows of darkness on all sides
def expand_grid(grid,step,zero_pixel):
	if zero_pixel == 0 or (zero_pixel == 1 and step % 2 == 0):
		expand_pixel = 0
	else:
		expand_pixel = 1
	xvals = [x for (x,y) in grid.keys()]
	xmin = min(xvals) 
	xmax = max(xvals)
	yvals = [y for (x,y) in grid.keys()]
	ymin = min(yvals)
	ymax = max(yvals)
	# top rows and bottom rows
	for x in range(xmin,xmax+1):
		for i in range(1,6):
			grid[(x,ymin-i)] = expand_pixel
			grid[(x,ymax+i)] = expand_pixel
	ymin = ymin-i
	ymax = ymax+i
	# left and right columns
	for y in range(ymin,ymax+1):
		for i in range(1,6):
			grid[(xmin-i,y)] = expand_pixel
			grid[(xmax+i,y)] = expand_pixel
	return grid



def enhance_image(grid,enhancement,step):
	# two rows/columns of darkness added
	grid = expand_grid(grid,step,pixel2num(enhancement[0]))
	newgrid = {**grid}	
	xvals = [x for (x,y) in grid.keys()]
	xmin = min(xvals) 
	xmax = max(xvals)
	yvals = [y for (x,y) in grid.keys()]
	ymin = min(yvals)
	ymax = max(yvals)
	# don't run the algoritm on the outermost border	
	for y in range(ymin+1,ymax):
		for x in range(xmin+1,xmax):
			# binary list to integer conversion
			val = 0
			pixels = [grid[(x-1,y-1)],grid[(x,y-1)],grid[(x+1,y-1)],grid[(x-1,y)],grid[(x,y)],grid[(x+1,y)],grid[(x-1,y+1)],grid[(x,y+1)],grid[(x+1,y+1)]]
			for bit in pixels:
				val = (val << 1) | bit
			#print('(',x,',',y,')',pixels,val,enhancement[val])
			newgrid[(x,y)] = pixel2num(enhancement[val])
	# set outermost border pixels correctly
	border_pixel = newgrid[(xmin+1,ymin+1)]
	for y in range(ymin,ymax+1):
		newgrid[xmin,y] = border_pixel
		newgrid[xmax,y] = border_pixel
	for x in range(xmin,xmax+1):
		newgrid[x,ymin] = border_pixel
		newgrid[x,ymax] = border_pixel

	return newgrid	

def count_lit_pixels(grid,step):	
	xvals = [x for (x,y) in grid.keys()]
	xmin = min(xvals) 
	xmax = max(xvals)
	yvals = [y for (x,y) in grid.keys()]
	ymin = min(yvals)
	ymax = max(yvals)
	count = 0
	for (x,y) in grid:
		#if x >= -(step) and x < xmax - 6 and y >= -(step) and y < ymax - 6:
		if grid[(x,y)] == 1:
			count += 1
	return count
		

def pixel2num(p):
	if p == '.':
		return 0
	else:
		return 1

def num2pixel(n):
	if n == 0:
		return '.'
	else:
		return '#'

def pretty_print_grid(grid):
	xvals = [x for (x,y) in grid.keys()]
	xmin = min(xvals) 
	xmax = max(xvals)
	yvals = [y for (x,y) in grid.keys()]
	ymin = min(yvals)
	ymax = max(yvals)
	for y in range(ymin,ymax+1):
		for x in range(xmin,xmax+1):
			if x == 0 and y == 0:
				print('o', end=' ')
			else:
				print(num2pixel(grid[(x,y)]), end=' ')
		print()
	print()

### main
steps = None
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
	if len(sys.argv) > 2:
		steps = int(sys.argv[2])
else:
	fname = 'input'
	if len(sys.argv) > 1:
		steps = int(sys.argv[1])
if steps == None:
	steps = 2

f = open(fname)
coordinates = []

enhancement = list(f.readline().rstrip())
f.readline() # empty line

grid = {}
for y,row in enumerate(f):
	for x,pixel in enumerate(list(row.rstrip())):
		grid[(x,y)] = pixel2num(pixel)
pretty_print_grid(grid)
for i in range(steps):
	grid = enhance_image(grid,enhancement,i)
	pretty_print_grid(grid)
	count = count_lit_pixels(grid,i)
	print("Enhancement number:", i+1)
	print("%d pixels are lit" % (count))

