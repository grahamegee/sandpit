# find the largest prime factor of the given integer.

number = 600851475143
#number = 450

def find_prime_factors(n):
	primes  = []
	integer = n
	divisor = 2
	while integer > 1:
		#python -O to disable invariant check
		assert reduce(lambda x,y: x*y, primes + [integer]) == n

		while integer % divisor == 0:
				primes.append(divisor)
				integer /= divisor
		
		divisor += 1
		
	return primes

primefactors = find_prime_factors(number)
print primefactors
print "largest prime factor of %d is %d" %(number, primefactors[-1])
