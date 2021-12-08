#!/usr/bin/python3
import sys
from termcolor import colored

if len(sys.argv) > 1 and sys.argv[1] == "test":
	fname = 'input_test'
else:
   fname = 'input'

def readboards(f):
	boards = {}
	counter = 0
	while True:
		f.readline() # skip empty line
		board = []
		for i in range(5):
			row = [(int(v),0) for v in f.readline().split()]
			if row == []:
				return boards # end of file
			board.append(row)
		boards[counter] = board
		counter += 1

def check_bingo(boards):
	for b in boards:
		# check rows
		for y in range(5):
			fiveinarow = 1
			for x in range(5):	
				if boards[b][y][x][1] == 0:
					fiveinarow = 0
					break
			if fiveinarow == 1:
				return b
		# check columns
		for x in range(5):
			fiveinarow = 1
			for y in range(5):	
				if boards[b][y][x][1] == 0:
					fiveinarow = 0
					break
			if fiveinarow == 1:
				return b
	return -1				

def pretty_print_board(board):
	for y in range(5):
		for x in range(5):
			if board[y][x][1] == 1:
				print(colored(str(board[y][x][0]).rjust(2), 'yellow'),end='')
			else:
				print(colored(str(board[y][x][0]).rjust(2), 'green'),end='')
			print(' ',sep='',end='')
		print('')
	print()

f = open(fname)
numbers = [int(n) for n in f.readline().split(',')]
boards = readboards(f)

# call numbers
for n in numbers:
	print("number:",n)
	for b in boards:
		for x in range(5):
			for y in range(5):	
				if boards[b][y][x][0] == n:
					boards[b][y][x] = (n,1) # mark number
		pretty_print_board(boards[b])
	winner = check_bingo(boards)
	if winner != -1:
		break

print("Winner board:", winner, "final number", n, "product")

usum = 0
for y in range(5):
	for x in range(5):
		if boards[winner][y][x][1]	== 0:
			usum += boards[winner][y][x][0]	

print("Sum of unmarked values (%d) * last number called (%d) = %d" % (usum, n, usum*n))
