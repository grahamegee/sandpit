#!/bin/python

import argparse

#---------------------------------------------------------------------------------
# maze file interpretation variables
#---------------------------------------------------------------------------------

wall    = '#' 
new     = ' '
been    = '*'
start   = 'S'
end     = 'G'
edge    = '\n'

#---------------------------------------------------------------------------------
# movement functions
#---------------------------------------------------------------------------------

up    = lambda (row,col): (row-1,col)	
down  = lambda (row,col): (row+1,col)
right = lambda (row,col): (row,col+1)
left  = lambda (row,col): (row,col-1)

directions = [right,down,left,up]

#---------------------------------------------------------------------------------

def parse_maze(mazeFile):
	""" Turn the maze into a dictionary of the form:
		{(row,col), maze character}
	"""
	maze = {}
	for row in range(len(mazeFile)):
		for col in range(len(mazeFile[row])):
			maze[(row,col)] = mazeFile[row][col]
	
	return maze

#---------------------------------------------------------------------------------

def show_maze(maze):
	""" Print the maze to standard out
	"""
	positions = maze.keys()
	positions.sort()
	print "".join([maze[position] for position in positions]) 

#---------------------------------------------------------------------------------

def check(position, maze):
	""" Check the position. If it is end/new/been return it, otherwise return
	    None.
	"""
		
	if position not in maze.keys():
		return None	
	
	if maze[position] == end:
		return end

	elif maze[position] == new:
		return new

	elif maze[position] == been:
		return been

	else:
		return None	

#---------------------------------------------------------------------------------

def find_start(maze):
	""" function to extract the start position from the maze.
	"""
	
	for key in maze.keys():
		if maze[key] == start:
			return key

#---------------------------------------------------------------------------------

def chooseDirection(position, maze, previousDirection):
	""" choose the best direction to move in from current position.
			
		Uses:
			priority_move()
	"""
	moves = [check(movement(position),maze) for movement in directions]
	
	# if you can finish do so, otherwise keep moving

	if end in moves:
		return (moves.index(end),directions[moves.index(end)])

	else:
		move = priority_move(moves, previousDirection)
		if move is not None:
			return (move, directions[move])
		else:	
			# less than ideal but this function returns a tuple...
			# this should never happen.
			return (None,None)

#---------------------------------------------------------------------------------

def priority_move(moves, previousDirection):
	""" chooses highest priority direction to move in if there is a choice.
	"""
	#1) a new square takes priority over a square you have already been on
	#2) keep going in the same direction if you can.
	indexes_for_new  = [x for x in range(len(moves)) if moves[x] == new]
	indexes_for_been = [x for x in range(len(moves)) if moves[x] == been]
	
	if indexes_for_new != []:
		if previousDirection in indexes_for_new:
			return previousDirection
		else:
			return indexes_for_new[0]

	elif indexes_for_been != []:	
		if previousDirection in indexes_for_been:
		 	return previousDirection
		else:
			return indexes_for_been[0]
	
	else:
		#this should never happen...
		return None
	
#---------------------------------------------------------------------------------

def solve(position, maze, previousDirection=None):
	"""
	top level solve function
	"""
	
	while maze[position] is not end:
	
		directionIndex, direction = chooseDirection(position,
							    maze,
							    previousDirection)
		if direction == None:
			break

		previousDirection = directionIndex
		# if we're moving over a new position drop a crumb so that
		# subsequent moves can be prioritised
		if maze[position] == new:
			maze[position] = been
		# move
		position = direction(position)
		show_maze(maze)
	
	if maze[position] is end:
		print "solved!"
	else:
		print "I got stuck.. bugger!"
#---------------------------------------------------------------------------------

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
