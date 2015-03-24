####################################
# File name: eval_cost.py          #
# Author: Tommy Inouye             #
# Date: 03/24/12                   #
# Description:  File that handled  #
# all operations that involved     #
# the budget                       #
####################################

import re

#according to google, conversion from euros to dollar is 1.8
def convert_to_euros(x):
	return 1.8 * x

#from a given string, return estimated cost
def parse_to_float(X,is_euro):
	#check string for certain words
	if X.startswith('US'):
		X = X[2:]
	if '-' in X:
		X = X.replace('-',' - ')
	X = X.replace('million',' million')
	X = X.replace(',','')
	X = X.replace('$','')
	X = X.replace('\xc2\xa3','')
	X = X.split()
	#check for default case
	if len(X) == 1:
		if is_euro:
			return convert_to_euros(float(X[0]))
		else:
			return float(X[0])
	#check to see if million is appended to it
	if len(X) == 2:
		if X[1] == 'million':
			if is_euro:
				return convert_to_euros(1000000 * float(X[0]))
			else:
				return 1000000 * float(X[0])
		else:
			if is_euro:
				return convert_to_euros(float(X[0]))
			else:
				return float(X[0])
	else:
		#check to see if it is in a range in the form x-y million and return midpoint
		if X[1] == "-":
			avg = (float(X[0])+float(X[2]))/2
			if len(X) > 3:
				if X[3] == 'million':
					if is_euro:
						return convert_to_euros(1000000 * avg)
					else:
						return 1000000 * avg
			else:
				if is_euro:
					return convert_to_euros(avg)
				else:
					return avg
	return 0

#use regular expressions to parse out price
def parse_string(X):
	if not X:
		return None,False
	X = ''.join(X.split())
	# Check for all cases

	# Checking for "$[a number] million"
	if len(re.findall(r'(\$[0-9,.-]*million)',X)) > 0:
		return re.findall(r'(\$[0-9,.-]*million)',X)[0],False
	# Checking for "$[a number]"
	if len(re.findall(r'(\$[0-9,.-]*)',X)) > 0:
		return re.findall(r'(\$[0-9,.-]*)',X)[0], False
	# Checking for "[unicode for euro][a number]million"
	if len(re.findall(r'(\xc2\xa3[0-9,.-]*million)',X)) > 0:
		return re.findall(r'(\xc2\xa3[0-9,.-]*million)',X)[0],True
	# Checking for "[unicode for euro][a number]"
	if len(re.findall(r'(\xc2\xa3[0-9,.-]*)',X)) > 0:
		return re.findall(r'(\xc2\xa3[0-9,.-]*)',X)[0],True
	else:
		# ...hopefully never reaches here....
		return '0',False


def main():
	#make array
	f = open('eval_cost_tester','r')
	arr = f.read().split('\n')

	for item in arr:
		val, is_euro = parse_string(item)
		if not val:
			continue
		print parse_to_float(val,is_euro)

	#test cases
	# print parse_to_float('$1,200,000-',False)
	# print parse_to_float(parse_string('$58.8 million'),False)
	# print parse_to_float(parse_string('$8-8.5 million '),False)
	# print parse_to_float(parse_string('$800,000-850,000  '),False)
	# print parse_to_float(parse_string('US$1,644,736'),False)
	# print parse_to_float(parse_string('$839,727'),False)
	# print parse_to_float(parse_string('\xc2\xa3400,000'),True)
	# print parse_string('$839,727')
	# print parse_string('$32 million')
	# print parse_string('$8-8.5 million')
	# print parse_string('$1,200,000-$2,275,000')

if __name__ == '__main__':
	main()