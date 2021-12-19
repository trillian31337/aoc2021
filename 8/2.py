#!/usr/bin/python3
import sys
from termcolor import colored

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

def parse_input(s):
	start_outputs = s.index('|')
	outputs = []
	outputs.append(s[start_outputs+1:])

	inputs = set(s[:start_outputs])
	input_symbols = []
	for symbol in inputs:
		if set(symbol) not in input_symbols:
			input_symbols.append(set(symbol))
	outputs = s[start_outputs+1:]
	output_symbols = []
	for symbol in outputs:
		output_symbols.append(set(symbol))
	
	return input_symbols,output_symbols

def pretty_print_display_decoding(lookup):
	print("")
	top_segment = next(iter(lookup[7] - lookup[1]))
	top_right = next(iter(lookup[1] - lookup[5]))
	top_left = next(iter(lookup[9] - lookup[3]))
	middle = next(iter(lookup[8] - lookup[0]))
	bottom_right = next(iter(lookup[1] - lookup[2]))
	bottom_left = next(iter(lookup[6] - lookup[5]))
	bottom = next(iter(lookup[5] - lookup[4] - lookup[7]))
	print(" %s " %(top_segment*4))
	print("%s    %s" %(top_left,top_right))
	print("%s    %s" %(top_left,top_right))
	print("%s    %s" %(top_left,top_right))
	print(" %s " %(middle*4))
	print("%s    %s" %(bottom_left,bottom_right))
	print("%s    %s" %(bottom_left,bottom_right))
	print("%s    %s" %(bottom_left,bottom_right))
	print(" %s " %(bottom*4))
	print()


def find_easy(input_symbols):
	decoding = []
	lookup = {}
	for s in input_symbols:
		if len(s) == 2:
			decoding.append((s,1))
			lookup[1] = s
		elif len(s) == 4:
			decoding.append((s,4))
			lookup[4] = s
		elif len(s) == 3:
			decoding.append((s,7))
			lookup[7] = s
		elif len(s) == 7:
			decoding.append((s,8))
			lookup[8] = s
	return decoding,lookup

def find_rest(input_symbols,decoding,lookup):
	while len(lookup) < 10:
		for s in input_symbols:
			found = 0
			for d in decoding:
				if s == d[0]:
					found = 1
					break
			if found:
				continue
			if len(s) == 5 and len(s - lookup[7]) == 2:
				decoding.append((s,3))
				lookup[3] = s
			elif len(s) == 6 and len(s & lookup[1]) == 1:
				decoding.append((s,6))
				lookup[6] = s
			elif (6 in lookup.keys()) and len(s & lookup[8]) == 6 and len(s & lookup[4]) == 3:
				decoding.append((s,0))
				lookup[0] = s
			elif (6 in lookup.keys()) and len(s) == 5 and len(s & lookup[1]) == 1 and len(s & lookup[6]) == 4:
				decoding.append((s,2))
				lookup[2] = s
			elif (3 in lookup.keys()) and len(s) == 6 and len(s - lookup[3]) == 1:
				decoding.append((s,3))
				lookup[9] = s
			elif (9 in lookup.keys()) and len(s) == 5 and len(s & lookup[9]) == 5:	
				decoding.append((s,5))
				lookup[5] = s
	return lookup			
	
def decode_output(output_symbols,lookups):
	print("output_symbols:",output_symbols)
	output_value = ''
	for o in output_symbols:
		for l in lookups:
			if lookups[l] == o:
				output_value += str(l)
				break
	return int(output_value)

f = open(fname)
outputs = []
for line in f:
	input_symbols,output_symbols = parse_input(line.rstrip().split(' '))
	decoding,lookup = find_easy(input_symbols)
	lookup = find_rest(input_symbols,decoding,lookup)
	pretty_print_display_decoding(lookup)
	outputs.append(decode_output(output_symbols,lookup))
print()
print("Outputs:",outputs)
print("Sum of outputs:",sum(outputs))

