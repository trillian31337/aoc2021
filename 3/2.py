#!/usr/bin/python3
import sys

def most_common(diag, remaining, bit):
	half = sum(remaining)/2
	count = 0
	for i in range(len(diag)):
		if remaining[i] == 1:
			if diag[i][bit] == '1':
				count += 1
	print("count:",count)
	if count >= half:
		return 1
	else:
		return 0		
	
def least_common(diag, remaining, bit):
	half = sum(remaining)/2
	print("half",half)
	count = 0
	for i in range(len(diag)):
		if remaining[i] == 1:
			if diag[i][bit] == '1':
				count += 1
	print("count:",count)
	if count >= half:
		return 0
	else:
		return 1		
	
	

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

with open(fname) as f:
	diag = [list(l.rstrip()) for l in f.readlines()]


remaining = [1]*len(diag)
for bit in range(len(diag[0])):
	v = most_common(diag, remaining, bit)
	print("most common:",v)
	for i in range(len(diag)):
		if diag[i][bit] != str(v):
			remaining[i] = 0
   # print the remaining
	for i in range(len(diag)):
		if remaining[i] == 1:
			print(diag[i])
	# check if only one number left
	if sum(remaining) == 1:
		print("one remaining!")
		index = remaining.index(1)
		break

oxygen = int(''.join(diag[index]),2)
print("Oxygen generator rating:", oxygen)

remaining = [1]*len(diag)
for bit in range(len(diag[0])):
	v = least_common(diag, remaining, bit)
	print("least common:",v)
	for i in range(len(diag)):
		if diag[i][bit] != str(v):
			remaining[i] = 0
   # print the remaining
	for i in range(len(diag)):
		if remaining[i] == 1:
			print(diag[i])
	# check if only one number left
	if sum(remaining) == 1:
		print("one remaining!")
		index = remaining.index(1)
		break

co2 = int(''.join(diag[index]),2)
print("CO2 scrubber rating:", co2)

print("oxygen * co2: ", oxygen*co2)
