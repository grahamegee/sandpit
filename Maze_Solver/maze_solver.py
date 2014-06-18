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
	
	if maze[position] in [end,new,been]:
		return maze[position]
	else:
		return None	

#---------------------------------------------------------------------------------

def find_start(maze):
	""" function to extract the start position from the maze.
	"""
	return [key for key, val in maze.items() if val == start][0]

#---------------------------------------------------------------------------------

def chooseDirection(position, maze, previousDirection):
	""" choose the best direction to move in from current position.
			
		Uses:
			priority_move()
	"""
	moves = [check(movement(position),maze) for movement in directions]
	
	# if you can finish do so, otherwise keep moving

	if end in moves:
		return directions[moves.index(end)]

	else:
		move = priority_move(moves, previousDirection)
		if move is not None:
			return move
		else:	
			# this should never happen.
			return None

#---------------------------------------------------------------------------------

def priority_move(moves, previousDirection):
	""" chooses highest priority direction to move in if there is a choice.
	"""
	#1) a new square takes priority over a square you have already been on
	#2) keep going in the same direction if you can.
	new_directions  = [directions[x] for x in range(len(moves)) if moves[x] == new]
	been_directions = [directions[x] for x in range(len(moves)) if moves[x] == been]
	
	if new_directions != []:
		if previousDirection in new_directions:
			return previousDirection
		else:
			return new_directions[0]

	elif been_directions != []:	
		if previousDirection in been_directions:
		 	return previousDirection
		else:
			return been_directions[0]
	
	else:
		#this should never happen...
		return None
	
#---------------------------------------------------------------------------------

def solve(position, maze, previousDirection=None):
	"""
	top level solve function
	"""
	
	while maze[position] is not end:
	
		direction = chooseDirection(position, maze, previousDirection)
		if direction == None:
			break

		previousDirection = direction
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
		print "I got stuck..."
#---------------------------------------------------------------------------------

def main():
	
	parser = argparse.ArgumentParser(description='Solve a maze')
	parser.add_argument('file', type=file)

	args = parser.parse_args()
	maze = parse_maze(args.file.readlines())
	solve(find_start(maze), maze)

#---------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
