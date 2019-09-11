"""
	1-3.py
			25-Feb-2014
"""
import sys
import random

def random_data(count, data_array):
	for i in range(count):
		data_array.append(random.randint(10, 100))

def quicksort(arr):
	less=[]
	pivotList=[]
	more=[]
	if len(arr) <= 1:
		return arr
	else:
		pivot = arr[0]		
		for i in arr:
			if i < pivot:
				less.append(i)
			elif i > pivot:
				more.append(i)
			else:
				pivotList.append(i)
		less = quicksort(less)
		more = quicksort(more)
		return less + pivotList + more

def main(argv):
	a=[]
	if (len(argv)!=1):
		sys.exit("Usage: 1-3.py [data count]")
	
	data_cnt = int(sys.argv[1])
	random_data(data_cnt, a)
	# print "Original Array: ", a
	a = quicksort(a)
	for i in range(len(a)):
		print 'Rank {0:2} : {1:3}'.format(i+1, a[len(a)-i-1])
	
if __name__=="__main__":
	main(sys.argv[1:])


