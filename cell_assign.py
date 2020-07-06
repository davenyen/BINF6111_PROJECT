# Author: David Nguyen
# Function: Assigns cells to groups/targets

import sys
import os
import time
import datetime
from functions import read_matrix, create_target_directory, create_sorted_fastq_file, coordinates_barcodes_dictionary, error_check, printProgressBar

# NEED TO UPDATE TO READ MULTIPLE READS OF SAME EXPERIMENT!

# CHANGE LIMITER TO FALSE FROM FUNCTIONS.PY FOR FULL OUTPUT (ATM LIMITED TO 200,000)
# (CURRENTLY ON REFACTOR [1] VERSION)
# (PRE-REFACTOR) TIME TAKEN TO RUN FULL OUTPUT ON OG_READ1 AND OG_READ2 = ETA 15 hours
# (REFACTOR [2]) TIME TAKEN TO RUN FULL OUTPUT ON OG_READ1 AND OG_READ2 = ETA 1.5 hours?

# (PRE-REFACTOR) TIME TAKEN TO RUN FULL OUTPUT ON test_r1 AND test_r2 = 9.12831641 minutes
# (REFACTOR [1]) TIME TAKEN TO RUN FULL OUTPUT ON test_r1 AND test_r2 = 0.8 minutes [avg of 5 runs]
# (REFACTOR [2]) TIME TAKEN TO RUN FULL OUTPUT ON test_r1 AND test_r2 = 1.33 minutes [avg of 5 runs]

# OPTIMISATION IDEAS: [DO 5 FOR MAXIMUM SPEED FOR SURE]
# (1) Assume some barcodes are not in the matrix, then do [if barcode not in matrix: skip] (speeds up read1)
# (2) Assume coordinates do not always match, then do [if coordinates not in read1: skip] (speeds up read2)
# (3) Assume coordinates always match, then do [if read1[coordinate] barcode not in matrix: skip] (speeds up read2)
# (4) Assume parse_fastq processes read1, get variables from that function simultaneously for speed 
# (5) Open all fastq files for appending, and then close all of them at the end (should speed up ALOT because opening files and closing takes a lot of time)

# Input: python3 cell_assign.py {matrix.csv} {read1.fastq} {read2.fastq}
# Output: sorted_target_groups/{lots of groups}/group.fastq (for each group)

# Sample run cmd line:
# python3 cell_assign.py /Users/student/BINF6111_2020/data/test_barcode.csv /Users/student/BINF6111_2020/test/output/PilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/output/PilotCROP_C_1_S1_L001_R2_001.fastq

# TEST RUN USE THIS:
# python3 cell_assign.py /Users/student/BINF6111_2020/data/test_barcode.csv /Users/student/BINF6111_2020/test/output/test_L001_R1_001.fastq /Users/student/BINF6111_2020/test/output/test_L001_R2_001.fastq 

# Read in matrix csv
# - Associate barcode from read one to sequence in read 2
# - When file is list of groups, a list of cell barcodes from those groups are
# 	created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# 	particular group 

# TO DO
# (1) Add into master_script 
# (2) Toggle num_lines to read files length
# (3) Optimise runtime 

# MAIN
if __name__ == '__main__':

	# VARIABLES
	csv_matrix = sys.argv[1]
	read_one = sys.argv[2]
	read_two = sys.argv[3]
	start_time = time.time()
	
	# Run error checking
	error_check (csv_matrix, read_one, read_two)
	
	# Main functions
	barcode_table = read_matrix (csv_matrix)
	dir_name = create_target_directory (barcode_table, read_two)
	coordinates_barcodes = coordinates_barcodes_dictionary (read_one)
	create_sorted_fastq_file (read_two, barcode_table, coordinates_barcodes, dir_name)

	print("\nCELL ASSIGNMENT SUCCESSFUL")
	print("Runtime = {} h/m/s.\n".format(str(datetime.timedelta(seconds=time.time() - start_time))))
