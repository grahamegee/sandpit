import operator

operators = {'+' : operator.add,
	     '-' : operator.sub,
	     '*' : operator.mul,
	     '/' : operator.div}

expression = [5,1,2,'+',4,'*','+',3,'-']
#expression = [3,5,'+',7,2,'-','*']

def interpret(token):
	""" takes a token which can either be a number or an operator, and return
	    a stack to stack function.
	"""
	if operators.has_key(token):
		return lambda stack : stack [:-2] + \
			  	      [operators[token](stack[-2],stack[-1])]
	else:
		return lambda stack : stack + [token]

print reduce(lambda x,f : f(x), [interpret(token) for token in expression] ,[])


