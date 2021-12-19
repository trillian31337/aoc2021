#!/usr/bin/python3
import sys
from math import floor

def matching(s1,s2):
	opening = ['(','[','{','<']
	closing = [')',']','}','>']
	if opening.index(s1) == closing.index(s2):
		return True
	else:
		return False

def check_sequence(sequence):
	if sequence == []:
		return []
	else:
		# split list after last open paranthesis
		split = 0
		while sequence[split] in ['(','[','{','<']:
			split += 1
			if split >= len(sequence):
				return sequence
		if split == 0:
			return None
		elif matching(sequence[split-1],sequence[split]):
			sequence.pop(split)
			sequence.pop(split-1)
			return check_sequence(sequence)
		else:
			return None

def complete(remaining):
	return [lookup_closing(s) for s in remaining[::-1]]
	
def lookup_closing(s):
	opening = ['(','[','{','<']
	closing = [')',']','}','>']
	return closing[opening.index(s)]

def lookup_points(s):
	closing = [')',']','}','>']
	points = [1,2,3,4]	
	return points[closing.index(s)]

def points(completion):
	score = 0
	for s in completion:
		score = score*5 + lookup_points(s)
	return score

### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

f = open(fname)
results = [] 
for line in f:
	remaining = check_sequence(list(line.rstrip()))
	if remaining == None:
		print("line is corrupted")
	else:
		completion = complete(remaining)
		print("line is fine, completion:",''.join(completion)) 
		results.append(points(completion))
print("results:",results)
print("middle index:",floor(len(results)/2)) 
print("middle score:",(sorted(results)[floor(len(results)/2)]))
