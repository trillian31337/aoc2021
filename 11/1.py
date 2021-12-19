#!/usr/bin/python3
import sys
from termcolor import colored

class octopus:
	def __init__(self, x, y, energy):
		self.x = x
		self.y = y
		self.energy = int(energy)

	def check_coord(self,x,y):
		if x == self.x and y == self.y:
			return True
		else:
			return False

def parse_input(y,row, octopus_grid):
	for x,energy in enumerate(row):
		octopus_grid.append(octopus(x,y,energy))	
	return octopus_grid

def increase_adjacent(flashing, octopus_grid):
	count = 0
	for f in flashing:
		# find coordinates to increase
		coords = []
		for y in [-1,0,1]:
			for x in [-1,0,1]:
				coords.append((f.x+x,f.y+y))
		# increase energy of adjacent octopuses if not in flash list
		for ax,ay in coords:
			if ax >= 0 and ax <= 9 and ay >= 0 and ay <= 9 and (ax != f.x or ay != f.y):
				inflashing = False
				for g in flashing:
					if ax == g.x and ay == g.y:
						inflashing = True
						break
				if inflashing == False:
					for o in octopus_grid:
						if o.check_coord(ax,ay):
							if o.energy == 9:
								o.energy = 0
								count += 1
								flashing.append(o)
							else:
								o.energy += 1
							break
	return octopus_grid, count

def simulate_step(octopus_grid):
	flashing = []
	count = 0
	# increase energy level of all octopuses
	for o in octopus_grid:
		if o.energy == 9:
			o.energy = 0
			count += 1
			flashing.append(o)
		else:
			o.energy += 1
	# flashing
	octopus_grid,count_adjacent_flashes = increase_adjacent(flashing, octopus_grid)
	count += count_adjacent_flashes

	return octopus_grid,count

def pretty_print_octopuses(octopus_grid):
	# access octopuses in order
	for y in range(10):
		for x in range(10): 
			for o in octopus_grid:
				if o.check_coord(x,y):
					if o.energy == 0:
						print(colored(str(o.energy).rjust(2), 'cyan'),end='')
					else:
						print(colored(str(o.energy).rjust(2), 'blue'),end='')
					break
			print(' ',sep='',end='')
		print('')
	print()

### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

f = open(fname)
y = 0
octopus_grid = []
for line in f:
	octopus_grid = parse_input(y,list(line.rstrip()),octopus_grid)
	y += 1
pretty_print_octopuses(octopus_grid)
totalcount = 0
for i in range(100):
	octopus_grid,count = simulate_step(octopus_grid)
	totalcount += count
	pretty_print_octopuses(octopus_grid)
print("total count of flashes:",totalcount)
