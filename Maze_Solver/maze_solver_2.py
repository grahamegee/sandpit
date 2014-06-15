#!/bin/python

import argparse

route   = '.' 
new     = ' '
been    = '*'
start   = 'S'
end     = 'G'
edge    = '\n'

up    = lambda (row,col): (row-1,col)	
down  = lambda (row,col): (row+1,col)
right = lambda (row,col): (row,col+1)
left  = lambda (row,col): (row,col-1)

#----------------------------------------------------------------------------------

def parse_maze(mazeFile):
	""" Turn the maze into a dictionary of the form:
		{(row,col), maze character}
	"""
	maze = {}
	for row in range(len(mazeFile)):
		for col in range(len(mazeFile[row])):
			maze[(row,col)] = mazeFile[row][col]
	return maze

#----------------------------------------------------------------------------------

def find_start(maze):
	""" function to extract the start position from the maze.
	"""
	
	for key in maze.keys():
		if maze[key] == start:
			return key

#----------------------------------------------------------------------------------

def show_maze(maze):
	""" Print the maze to standard out
	"""
	positions = maze.keys()
	positions.sort()
	print "".join([maze[position] for position in positions]) 

#----------------------------------------------------------------------------------

def solve(position, maze):
	
	if position not in maze.keys():
		print "invalid position"
		return False
	if maze[position] is end:
		print "solved!"
		show_maze(maze)
		return True
	if maze[position] not in [new,start]:
		print "not a new path position"
		return False
	print "mark as been"
	maze[position] = been
	show_maze(maze)
	if solve(up(position), maze) or solve(down(position), maze) \
	or solve(left(position), maze) or solve(right(position), maze):
	#	print "fill in route"
	#	maze[position] = route
	#	show_maze(maze)
		return True
	return False
	 
	
#----------------------------------------------------------------------------------
	
def main():
	
	parser = argparse.ArgumentParser(description='Solve a maze')
	parser.add_argument('file', type=file)

	args = parser.parse_args()
	maze = parse_maze(args.file.readlines())

	start = find_start(maze)
	solve(start, maze)

#---------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
