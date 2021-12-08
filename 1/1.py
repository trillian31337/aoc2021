#!/usr/bin/python3
import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

with open(fname) as f:
	depths = [int(v) for v in f.readlines()]

icounter = 0
for x,y in zip(depths[::],depths[1::]): 
	print (x,y)
	if y > x:
		icounter += 1
   
print(icounter)
