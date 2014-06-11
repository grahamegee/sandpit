#!/bin/python

import argparse

#---------------------------------------------------------------------------------
# maze file interpretation variables
#---------------------------------------------------------------------------------

wall    = '#' 
new     = ' '
been    = '.'
retrace = '!'
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

	maze = {}
	for row in range(len(mazeFile)):
		for col in range(len(mazeFile[row])):
			maze[(row,col)] = mazeFile[row][col]
	
	return maze

#---------------------------------------------------------------------------------

def show_maze(maze):
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

def dropCrumb(position, crumb, maze):
	""" substitute character in maze at current position with a crumb 
	    character

		Inputs:
		    position (row,collum)
		    crumb been|retrace
		    maze
	"""
	maze[position] = crumb 
	
	return maze

#---------------------------------------------------------------------------------

def move(position, direction, maze):
	""" apply movement from current position in the given direction 
	    and drop a breadcrumb.
	    
	    Inputs:
		position (row,collumn)
		direction up|down|left|right
		maze
	"""
	newPosition = direction(position)

	if maze[position] == new:
		maze = dropCrumb(position,been,maze)
	
	# if we are retracing and find a new path, we want to be able to
	# retrace along this new path.
	elif maze[position] == been == maze[newPosition]:
		maze = dropCrumb(position,retrace,maze)
	
	elif maze[position] == been:
		maze = dropCrumb(position,been,maze)
	
	return newPosition, maze

#---------------------------------------------------------------------------------

def chooseDirection(position, maze, previousDirection):
	""" choose the best direction to move in from current position.
			
		Uses:
			priority_move()
	"""
	moves = [check(movement(position),maze) for movement in directions]
	
	# if you can finish do so, otherwise prioritise

	if end in moves:
		return (moves.index(end),directions[moves.index(end)])

	else:
		move = priority_move(moves, previousDirection)
		if move != None:
			return (move, directions[move])
		else:
			#less than ideal but this function returns a tuple
			return (None, None)

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
		# if you hit a wall and turn around, this will ensure
		# that you keep moving away from the wall.
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
		position, maze = move(position, direction, maze)
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
	print start
	solve(start, maze)

#---------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
