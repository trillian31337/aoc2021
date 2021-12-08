#!/usr/bin/python3
import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

with open(fname) as f:
	depths = [int(v) for v in f.readlines()]

icounter = 0
previous = False
for x,y,z in zip(depths[::],depths[1::],depths[2::]):
	if previous != False and sum([x,y,z]) > previous:
		icounter += 1
	previous = sum([x,y,z])
   
print(icounter)
