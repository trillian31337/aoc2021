#!/usr/bin/python3
import sys
from termcolor import colored

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

def initialize_counters(counters,numbers):
	for n in numbers:
		counters[int(n)] += 1
	return counters

def simulate_day(counters):
	spawning = counters[0]
	for i in range(0,9):
		counters[i] = counters[i+1]
	counters[6] += spawning
	counters[8] += spawning
	return counters


def pretty_print_counters(counters,days):
	print("After %02d days: " % days,end='')
	for c in counters:
		print("%d," % c,end='')
	print(" sum: %d" % sum(counters))

f = open(fname)
numbers = [int(n) for n in f.readline().split(',')]

counters = [0]*10
counters = initialize_counters(counters,numbers)
pretty_print_counters(counters,0)
for d in range(1,256+1):
	counters = simulate_day(counters)
	pretty_print_counters(counters,d)

