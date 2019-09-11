"""
	1-2.py

	19-Feb-2014
"""

import sys
import random
histarray= [0]*11

def histgram( dataarray ):
	for x in range(len(dataarray)):
		t = dataarray[x]/10
		histarray[t]+=1

def rand_data(count, data_array):
	for i in range(count):
		data_array.append(random.randint(0, 100))
		
def histprint( dataarray ):
	for i in range (len(dataarray)):
		print "Range: %d0 - %d9: " % (i, i), 
		print dataarray[i]
		
def main(argv):
	if (len(argv)!=1):
		sys.exit("Usage:1-2.py [sample count]")
		
	data_count = int(sys.argv[1])
	data_stream = []
	rand_data( data_count, data_stream )
	histgram( data_stream )
	histprint( histarray )
	
if __name__=="__main__":
	main(sys.argv[1:])
	