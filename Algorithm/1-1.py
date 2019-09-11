"""
Algorithm Practice
== 1-1 Combination

"""

import sys

def combination(choose_val, all_val):
	factorial1 = 1
	factorial2 = 1
	factorial3 = 1

	for i in range(1, choose_val+1):
		factorial1 = factorial1 * i

	for i in range(1, all_val-choose_val+1):
		factorial2 = factorial2 * i

	for i in range(1, all_val+1):
		factorial3 = factorial3 * i
		
	return factorial3/(factorial1*factorial2)

def main (argv):
	if (len(argv)!= 2):
		sys.exit("Usage: 1-1.py [all value] [choose value] ")
	
	allval = int(sys.argv[1])
	choose = int(sys.argv[2])

	print ("Chose "), choose,
	print (" from "), allval,
	print (".")
	print ("[r C n] is "), combination(choose, allval)
	
if __name__=="__main__":
	main (sys.argv[1:])
 


