# find the largest prime factor of the given integer.

number = 600851475143
#number = 32

def find_prime_factors(n):
	primes  = []
	integers = [n]
	devisor = 2
	while reduce(lambda x,y: x*y, primes + integers) == n:

		while numbers != [] and integers[0] % devisor == 0:
			
			if numbers[0] == devisor:
				primes.append(numbers[0])
				numbers = numbers[1:]
			else:
				numbers.append(devisor)
				numbers.append(numbers[0]/devisor)
				numbers = numbers[1:]
		
		if numbers == []:
			return primes
		
		devisor += 1
	else:
		return None

primefactors = find_prime_factors(number)

if primefactors is not None:
	print "largest prime factor of %d is %d" %(number, primefactors[-1])
else:
	print "something went wrong"
