#!/usr/bin/python3
import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

with open(fname) as f:
	diag = [list(l.rstrip()) for l in f.readlines()]

counts = [0]*len(diag[0])

for d in diag:
	for i in range(len(d)):
		if d[i] == '1':
			counts[i] += 1

gr = ''
half = len(diag)/2
for c in counts:
	if c > half:
		gr += '1'
	else:
		gr += '0'

gr_ = int(gr,2)
mask = int('1'*len(gr),2) 
er_ = ~gr_ & mask

print("Gamma rate:", gr_, " Epsilon rate:", er_, " power consumption:",gr_*er_)

