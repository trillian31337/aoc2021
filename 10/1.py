#!/usr/bin/python3
import sys

def matching(s1,s2):
	opening = ['(','[','{','<']
	closing = [')',']','}','>']
	if opening.index(s1) == closing.index(s2):
		return True
	else:
		return False

def corrupted(sequence):
	if sequence == []:
		return 0
	else:
		# split list after last open paranthesis
		split = 0
		while sequence[split] in ['(','[','{','<']:
			split += 1
			if split >= len(sequence):
				return 0
		if split == 0:
			return lookup_score(sequence[0])
		elif matching(sequence[split-1],sequence[split]):
			sequence.pop(split)
			sequence.pop(split-1)
			return corrupted(sequence)
		else:
			return lookup_score(sequence[split])

def lookup_score(s):
	if s == ')':
		return 3
	elif s == ']':
		return 57
	elif s == '}': 
		return 1197
	else:
		return 25137

### main
if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

f = open(fname)
score = 0
for line in f:
	result = corrupted(list(line.rstrip()))
	if result > 0:
		print("line is corrupted")
	else:
		print("line is fine") 
	score += result
print("score:",score)
