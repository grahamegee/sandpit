#!/bin/python

import argparse

#----------------------------------------------------------------------------------
# maze chars
#----------------------------------------------------------------------------------

been    = '.' 
new     = ' '
route   = '*'
start   = 'S'
end     = 'G'

#----------------------------------------------------------------------------------

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
	# first index of singleton list	
	return [key for key, val in maze.items() if val == start][0]

#----------------------------------------------------------------------------------

def show_maze(maze):
	""" Print the maze to standard out
	"""
	positions = maze.keys().sort()
	print "".join([maze[position] for position in positions]) 

#----------------------------------------------------------------------------------

def mark_position(position, marker, maze):
	""" Mark the position in the maze with a marker type
	"""
	if maze[position] is not start:
		maze[position] = marker

	return maze

#----------------------------------------------------------------------------------

def solve(position, maze):
	
	if position not in maze.keys():
		return False

	if maze[position] is end:
		return True

	if maze[position] not in [new,start]:
		return False
	
	maze = mark_position(position, been, maze)

	if solve(right(position), maze) or solve(down(position), maze) \
	or solve(left(position), maze) or solve(up(position), maze):
		# marks all the way back along the successful branch
		maze = mark_position(position, route, maze)
		return True

	return False
	 
	
#----------------------------------------------------------------------------------
	
def main():
	
	parser = argparse.ArgumentParser(description='Solve a maze')
	parser.add_argument('file', type=file)

	args = parser.parse_args()
	maze = parse_maze(args.file.readlines())

	solve(find_start(maze), maze)
	show_maze(maze)

#---------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
