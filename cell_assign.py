# Author: David Nguyen
# Function: Assigns cells to groups/targets
# Version: 3

import sys
import os
import time
import datetime
from collections import Counter
from functions import read_matrix, create_target_directory, create_sorted_fastq_file, coordinates_barcodes_dictionary, error_check, printProgressBar, close_all_files

# NEED TO UPDATE TO READ MULTIPLE READS OF SAME EXPERIMENT!

# OPTIMISATION IDEAS: [DO 5 FOR MAXIMUM SPEED FOR SURE]
# (1) Assume some barcodes are not in the matrix, then do [if barcode not in matrix: skip] (speeds up read1)
# (2) Assume coordinates do not always match, then do [if coordinates not in read1: skip] (speeds up read2)
# (3) Assume coordinates always match, then do [if read1[coordinate] barcode not in matrix: skip] (speeds up read2)
# (4) Assume parse_fastq processes read1, get variables from that function simultaneously for speed 

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
# (2) files sorted by barcodes per target/group
# (2) Optimise runtime 

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
	files_set = create_sorted_fastq_file (read_two, barcode_table, coordinates_barcodes, dir_name)
	close_all_files (files_set)

	# Makes a log file of runtimes
	runtime_log = os.system("touch CA_LOG.txt")
	log_file = open("CA_LOG.txt", "a")
	log_file.write("Runtime = {} h/m/s. Data set = {}\n".format(str(datetime.timedelta(seconds=time.time() - start_time)), dir_name))
	log_file.close()

	print("\nCELL ASSIGNMENT SUCCESSFUL")
	print("Runtime = {} h/m/s.\n".format(str(datetime.timedelta(seconds=time.time() - start_time))))
