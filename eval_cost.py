import re

#according to google, conversion from euros to dollar is 1.8
def convert_to_euros(x):
	return 1.8 * x

def parse_to_float(X,is_euro):
	if X.startswith('US'):
		X = X[2:]
	if '-' in X:
		X = X.replace('-',' - ')
	X = X.replace('million',' million')
	X = X.replace(',','')
	X = X.replace('$','')
	X = X.replace('\xc2\xa3','')
	X = X.split()
	# print X
	if len(X) == 1:
		if is_euro:
			return convert_to_euros(float(X[0]))
		else:
			return float(X[0])
	if len(X) == 2:
		if X[1] == 'million':
			if is_euro:
				return convert_to_euros(1000000 * float(X[0]))
			else:
				return 1000000 * float(X[0])
	else:
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

def parse_string(X):
	if not X:
		return None,False
	X = ''.join(X.split())

	# check for all cases
	if len(re.findall(r'(\$[0-9,.-]*million)',X)) > 0:
		return re.findall(r'(\$[0-9,.-]*million)',X)[0],False

	if len(re.findall(r'(\$[0-9,.-]*)',X)) > 0:
		return re.findall(r'(\$[0-9,.-]*)',X)[0], False
	if len(re.findall(r'(\xc2\xa3[0-9,.-]*million)',X)) > 0:
		return re.findall(r'(\xc2\xa3[0-9,.-]*million)',X)[0],True
	if len(re.findall(r'(\xc2\xa3[0-9,.-]*)',X)) > 0:
		return re.findall(r'(\xc2\xa3[0-9,.-]*)',X)[0],True
	else:
		# print "oops"
		return '0',False


def main():
	#make array
	f = open('output','r')
	arr = f.read().split('\n')
	# print len(arr)
	arr1 = []
	arr2 =[]
	i = 0
	for item in arr:
		# print item
		val, is_euro = parse_string(item)
		if not val:
			continue
		print parse_to_float(val,is_euro)
		# if '$' in item:
		# 	arr1.append(item)
		# elif '\xc2\xa3' in item:
		# 	arr2.append(item)
		# else:
		# 	i+=1
	# print arr1
	# print arr2
	# print ((len(arr1)+len(arr2)+i)==len(arr)) 

	# print parse_to_float(parse_string('$32 million'),False)
	# print parse_to_float(parse_string('$58.8 million'),False)
	# print parse_to_float(parse_string('$8-8.5 million '),False)
	# print parse_to_float(parse_string('$800,000-850,000  '),False)
	# print parse_to_float(parse_string('US$1,644,736'),False)
	# print parse_to_float(parse_string('$839,727'),False)
	# print parse_to_float(parse_string('\xc2\xa3400,000'),True)
	# print parse_string('$839,727')
	# print parse_string('$32 million')
	# print parse_string('$8-8.5 million')
	# print parse_string('\xc2\xa332 million')










if __name__ == '__main__':
	main()