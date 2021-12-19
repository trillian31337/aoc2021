from termcolor import colored
import re
import sys
import numpy as np

def template2polymer(template):
	polymer = {}
	for i in range(len(template)-1):	
		pair = template[i] + template[i+1]
		if pair in polymer:
			polymer[pair] += 1 
		else:
			polymer[pair] = 1
	first = template[:2]
	last = template[-2:]
	return polymer,first,last

def insertion(polymer,rules,first,last):
	newpairs = {}
	for pair in polymer:
		if pair in rules:
			insert = rules[pair]
			newpair1 = pair[0]+insert
			newpair2 = insert+pair[1]
			if first == pair:
				first = newpair1
			if last == pair:
				last = newpair2
			for newpair in [newpair1,newpair2]:
				if newpair in newpairs:
					newpairs[newpair] += polymer[pair]
				else:
					newpairs[newpair] = polymer[pair]

	return newpairs,first,last

def countelements(polymer):
	elementcounts = {}
	# count only the first element in each pair to avoid counting them double
	for pair in polymer:
		if pair[0] in elementcounts:
			elementcounts[pair[0]] += polymer[pair]
		else:
			elementcounts[pair[0]] = polymer[pair]
		# if last is of this pair type, count the second element as one more of that type
		if last == pair:
			if pair[1] in elementcounts:
				elementcounts[pair[1]] += 1
			else:
				elementcounts[pair[1]] = 1
	countlist = []
	for e in elementcounts:
		countlist.append((elementcounts[e],e))
	return sorted(countlist)

### main
if len(sys.argv) > 1 and sys.argv[1] == "test1":
	fname = 'input_test'
	steps = 10
elif len(sys.argv) > 1 and sys.argv[1] == "test2":
	fname = 'input_test'
	steps = 40
elif len(sys.argv) > 1 and sys.argv[1] == "1":
	fname = 'input'
	steps = 10
elif len(sys.argv) > 1 and sys.argv[1] == "2":
	fname = 'input'
	steps = 40
else:
	fname = 'input'
	steps = 40

f = open(fname)
template = f.readline().rstrip()
next(f)
rules = {}
polymer,first,last = template2polymer(template)

for line in f:
	rule = line.rstrip().split(' -> ')
	rules[rule[0]] = rule[1]

for i in range(steps):
	polymer,first,last = insertion(polymer,rules,first,last) 
	countlist = countelements(polymer)

print("Most common element",countlist[-1][0])
print("Least common element",countlist[0][0])

print("Most common - least common = %d" % (countlist[-1][0] - countlist[0][0]))
