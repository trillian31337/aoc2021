#!/usr/bin/python3
import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

with open(fname) as f:
	commands = [(c.split( )) for c in f.readlines()]

hp = 0
dp = 0
aim = 0

for (d,v) in commands:
	if d == 'forward':
		hp += int(v)
		dp += aim*int(v)
	elif d == 'down':
		aim += int(v)
	elif d == 'up':
		aim -= int(v)
	print("Position: horizontal:", hp, " depth:", dp, " aim:", aim)

print("Position: horizontal:", hp, " depth:", dp, " product:",dp*hp)

