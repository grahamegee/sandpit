A = 12345
B = 678

def solve(A, B):
	array_A = list(str(A))
	array_B = list(str(B))	
	length_A = len(array_A)
	length_B = len(array_B)
	
	i = 0
	ziparr = []
	
	while i <= (length_A - 1) or i <= (length_B - 1):
		
		if i <= (length_A - 1):
			ziparr.append(array_A[i])
		if i <= (length_B - 1):
			ziparr.append(array_B[i])

		i += 1

	return int("".join(ziparr))

print solve(A,B)
