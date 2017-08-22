from __future__ import print_function

######### Solution 1 #################

num = int(raw_input("Please enter a number: "))+1;
#pdb.set_trace()
for i in reversed(range(1,num)):
	for j in range (i):
		print ('*', end = ' ');
	print('\n');
for i in range(2,num):
	for j in range (i):
		print ('*', end = ' ');
	print('\n');
	
	
######### Solution 2 #################

num = int(raw_input("Please enter a number: "));
mid_id = num/2;
for j in range(mid_id+1):
	for i in range(num):
		if (i in range(mid_id-j+1,mid_id+j)):
			print (' ', end = ' ')
		else:
			print ('*', end = ' ');
	print ('\n');
