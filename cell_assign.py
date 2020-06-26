import os
import sys
import csv

# Read in matrix csv
# - Associate barcode from read one to sequence in read two
# - When file is list of groups, a list of cell barcodes from those groups are
# created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# particular group 

###### TO DO ######
# read pilot crop
# take x y position (use instead of barcode)
# grab read 2 sequence and header
# write as fastq files
# group separated by (target (group))
# look at barcode from read 1 and search matrix (find target)

# Make dictionary for O(1)
# quality scores?

# FUNCTIONS

# Reads matrix csv and saves as a data structure (dictionary)
def read_matrix (csv_matrix):
	with open(csv_matrix, 'r') as file:
	    reader = csv.reader(file)
	    i = 0
	    for row in reader:
	        print(row)
	        i += 1
	        if i == 5:
	        	break
	pass

# MAIN
if __name__ == '__main__':

	csv_matrix = sys.argv[1]
	read_matrix (csv_matrix)
	