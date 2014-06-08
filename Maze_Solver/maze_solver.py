#!/bin/python

import argparse

#---------------------------------------------------------------------------------
# maze file interpretation variables
#---------------------------------------------------------------------------------

wall    = '#' 
new     = ' '
been    = '.'
retrace = '!'
start   = "S"
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

def check(position,maze):
	""" Check the position. If it is end/new/been return it, otherwise return
	    None.
	"""
	height = len(maze)
	width  = len(maze[0])
		
	row,col = position
	# avoid accessing the array from the other side!
	if row < 0 or col < 0:
		return None
	
	# dont access index out of range
	if row == height or col == width:
		return None	
	
	if maze[row][col] == end:
		return end

	elif maze[row][col] == new:
		return new

	elif maze[row][col] == been:
		return been

	else:
		return None	

#---------------------------------------------------------------------------------

def find_start(maze):
	""" function to extract the start position from the maze.
	"""
	for subArray in range(len(maze)):
		if start in maze[subArray]:
			position = (subArray, maze[subArray].index(start))
	
	return position
		
#---------------------------------------------------------------------------------

def dropCrumb(position, crumb, maze):
	""" substitute character in maze at current position with a crumb 
	    character

		Inputs:
		    position (row,collum)
		    crumb been|retrace
		    maze
	"""
	row,col = position
	
	# strings are immutable so do some slicing
	maze[row] = maze[row][:col] + crumb + maze[row][col+1:]

#---------------------------------------------------------------------------------

def move(position, direction, maze):
	""" apply movement from current position in the given direction 
	    and drop a breadcrumb.
	    
	    Inputs:
		position (row,collumn)
		direction up|down|left|right
		maze
	"""
	row,col = position
	newRow,newCol = direction(position)

	if maze[row][col] == new:
		maze[row][col]
		dropCrumb(position,been,maze)
	
	# if we are retracing and find a new path, we want to be able to
	# retrace along this new path.
	elif maze[row][col] == been == maze[newRow][newCol]:
		dropCrumb(position,retrace,maze)
	
	elif maze[row][col] == been:
		dropCrumb(position,been,maze)
	
	return direction(position)

#---------------------------------------------------------------------------------

def chooseDirection(position, previousDirection, maze):
	""" choose the best direction to move in from current position.
			
		Uses:
			priority_move()
	"""
	moves = [check(movement(position),maze) for movement in directions]
	
	# if you can finish do so, otherwise prioritise

	if end in moves:
		return (moves.index(end),directions[moves.index(end)])

	else:
		move = priority_move(moves, previousDirection, maze)
		if move != None:
			return (move, directions[move])
		else:
			#less than ideal but this function returns a tuple
			return (None, None)

#---------------------------------------------------------------------------------

def priority_move(moves, previousDirection, maze):
	""" chooses highest priority direction to move in if there is a choice.
	"""
	#1) a new square takes priority over a square you have already been on
	#2) keep going in the same direction if you can.
	indexes_for_new  = []
	indexes_for_been = []
	
	for item in range(len(moves)):
		if moves[item] == new:
			indexes_for_new.append(item)
		if moves[item] == been:
			indexes_for_been.append(item)

	if indexes_for_new != []:
		if len(indexes_for_new) == 1:
			return indexes_for_new[0]
		else:
			if previousDirection in indexes_for_new:
				return previousDirection
			else:
				return indexes_for_new[0]

	elif indexes_for_been != []:	
		if len(indexes_for_been) == 1:
			return indexes_for_been[0]
		else:
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
	Recursive function to solve the maze
	"""
	print "".join(maze)
	
	row,col = position
	
	if maze[row][col] == end:
		print "done"
	
	else:
		directionIndex, direction = chooseDirection(position,
							    previousDirection,
							    maze)
		if direction != None:
			previousDirection = directionIndex
			newPosition = move(position, direction, maze)
			solve(newPosition, maze, previousDirection)
		else:
			print "I've got stuck. Bugger!"

#---------------------------------------------------------------------------------

def main():
	
	parser = argparse.ArgumentParser(description='Solve a maze')
	parser.add_argument('file', type=file)

	args = parser.parse_args()
	maze =  args.file.readlines()
	
	start = find_start(maze)
	solve(start, maze)

#---------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
