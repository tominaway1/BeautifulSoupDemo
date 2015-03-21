
def main():
	#make array
	f = open('output','r')
	arr = f.read().split('\n')
	# print len(arr)
	arr1 = []
	arr2 =[]
	i = 0
	for item in arr:
		if '$' in item:
			arr1.append(item)
		elif '\xc2\xa3' in item:
			arr2.append(item)
		else:
			i+=1
	print arr1
	print arr2
	print ((len(arr1)+len(arr2)+i)==len(arr)) 





if __name__ == '__main__':
	main()