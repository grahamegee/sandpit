#!/bin/python

import argparse

route   = '.' 
new     = ' '
deadend = '*'
start   = 'S'
end     = 'G'
edge    = '\n'

#----------------------------------------------------------------------------------

# use these to be verbose
def up(position):
	print "moving up"
 	row,col = position
	return (row-1,col)

def down(position):
	print "moving down"
 	row,col = position
	return (row+1,col)


def left(position):
	print "moving left"
 	row,col = position
	return (row,col-1)

def right(position):
	print "moving right"
 	row,col = position
	return (row,col+1)

#up    = lambda (row,col): (row-1,col)	
#down  = lambda (row,col): (row+1,col)
#right = lambda (row,col): (row,col+1)
#left  = lambda (row,col): (row,col-1)

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

def mark_position(position, marker, maze):
	""" Mark the position in the maze with a marker type
		Inputs:
			position (row,col)
			marker route|deadend
			maze
	"""
	if maze[position] is not start:
		maze[position] = marker
		if marker == route:
			print "Mark as explored route point"
		else:
			print "Mark as deadend"
	else:
		print "At the start"

	return maze

#----------------------------------------------------------------------------------

def solve(position, maze):
	print "current postion (%d,%d)" % position
	
	print "Is position in maze?"	
	if position not in maze.keys():
		print "No"
		return False
	print "Yes"

	print "Is position the goal?"
	if maze[position] is end:
		print "Yes"
		show_maze(maze)
		return True
	print "No"

	print "Is position unexplored and on the path?"
	if maze[position] not in [new,start]:
		print "No"
		return False
	print "Yes"
	
	maze = mark_position(position, route, maze)
	show_maze(maze)

	if solve(right(position), maze) or solve(down(position), maze) \
	or solve(left(position), maze) or solve(up(position), maze):
		return True

	print "backtracking ...."	
	maze = mark_position(position, deadend, maze)
	show_maze(maze)
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
