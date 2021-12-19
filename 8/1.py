#!/usr/bin/python3
import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

def parse_input(s):
	start_outputs = s.index('|')
	outputs = []
	outputs.append(s[start_outputs+1:])
	return outputs	

def count_segments(outputs):
	count = 0
	for o in outputs:
		for symbol in o:
			if len(symbol) == 2 or len(symbol) == 4 or len(symbol) == 3 or len(symbol) == 7:
				count += 1
	return count

f = open(fname)
outputs = []
for line in f:
	outputs.extend(parse_input(line.rstrip().split(' ')))
count = count_segments(outputs)
print("Count 1,4,7,8:",count)

