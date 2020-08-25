from predict import *
from recommend import *
from sys import argv



# Default Test Case
#x_org = -122.416
#y_org = 37.81
#x_dest = -122.3952897
#y_dest = 37.77697665
#time =  30

# Selec top M from N candidates
N = 12
M = 6

if __name__ == '__main__':
	# Read command line arguments
	x_org = float(argv[2])
	print(x_org)
	y_org = float(argv[1])
	print(y_org)
	x_dest = float(argv[4])
	print(x_dest)
	y_dest = float(argv[3])
	print(y_dest)
	time =  float(argv[5])
	print(time)
	# Get the recommend list
	park_info = park_recommd(x_org,y_org, x_dest,y_dest, time, N, M, plot = True)

	# write the output
	output_path = "../html/" 
	park_info.to_csv(output_path + 'test.csv')