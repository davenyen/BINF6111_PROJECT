import sys
import collections
import os
import time
import csv
from itertools import islice
from functions import *

# cmd line -> python3 {matrix} {read1} {read2}

# Read in matrix csv
# - Associate barcode from read one to sequence in read two
# - When file is list of groups, a list of cell barcodes from those groups are
# created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# particular group 

###### TO DO ######
# grab read 2 sequence and header
# write as fastq files
# group separated by (target (group))
# look at barcode from read 1 and search matrix (find target)

# 1. match coordinate of read1 with read2
# 2. match read1 barcode with matrix
# 3. grab read2 sequence and put into group directory (target)
#     - quality scores as well and header?
# 4. error cases and handling last!

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Writes to sorted fastq files 
def write_fastq (void):
	pass

# MAIN
if __name__ == '__main__':

	# VARIABLES
	csv_matrix = sys.argv[1]
	read_one = sys.argv[2]
	read_two = sys.argv[3]

	try:
		barcode_table = read_matrix (csv_matrix)
		create_target_directory (barcode_table)
		coordinates_barcodes = coordinates_barcodes_dictionary (read_one)
	except Exception:
		print("ERROR")
	else:
		print("SUCCESS")