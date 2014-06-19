# find the largest prime factor of the given integer.

number = 600851475143
#number = 300

def find_prime_factors(n):
	primes  = []
	integers = [n]
	devisor = 2
	while reduce(lambda x,y: x*y, primes + integers) == n:

		while integers != [] and integers[0] % devisor == 0:
			
			if integers[0] == devisor:
				primes.append(integers[0])
				integers = integers[1:]
			else:
				integers.append(devisor)
				integers.append(integers[0]/devisor)
				integers = integers[1:]
		
		if integers == []:
			return primes
		
		devisor += 1
	else:
		return None

primefactors = find_prime_factors(number)

if primefactors is not None:
	print "largest prime factor of %d is %d" %(number, primefactors[-1])
else:
	print "something went wrong"
