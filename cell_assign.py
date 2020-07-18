# Author: David Nguyen
# Function: Assigns cells to groups/targets
# Version: 1.5

import sys
import os
import time
import datetime
from collections import Counter
from functions import create_threads, count_lines, split_read_two, create_fastq_files, read_matrix, create_target_directory, create_sorted_fastq_file, create_coordinates_barcodes_dictionary, error_check, close_all_files, create_indices_list, myThread

# Input: python3 cell_assign.py {matrix.csv} {read1.fastq} {read2.fastq}
# Output: sorted_target_groups/{lots of groups}/group.fastq (for each group)

# Sample run cmd line:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/PilotCROP_L1_R1.fastq symlinks/PilotCROP_L1_R2.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/test/check_master_script/barcodesA1.txt

# TEST RUN USE THIS:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/SML_TEST_L1_R1.fastq symlinks/SML_TEST_L1_R2.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/test/check_master_script/barcodesA1.txt
# L2 SET append == True:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/SML_TEST_L2_R1.fastq symlinks/SML_TEST_L2_R2.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/test/check_master_script/barcodesA1.txt

# Read in matrix csv
# - Associate barcode from read one to sequence in read 2
# - When file is list of groups, a list of cell barcodes from those groups are
# 	created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# 	particular group 

# TO DO
# (1) Add into master_script 
# (2) Optimise runtime 

# MAIN
if __name__ == '__main__':

	# VARIABLES
	csv_matrix = sys.argv[1]
	filtered_read_one = sys.argv[2]
	read_two = sys.argv[3]
	indices = sys.argv[4]
	desired_barcodes = sys.argv[5]
	start_time = time.time()

	# Main functions
	barcode_matrix = read_matrix (csv_matrix)
	dbc_matrix = read_matrix (desired_barcodes)
	indices_list = create_indices_list (indices)
	# Change append to true for Lane 2
	dir_name = create_target_directory ("/Users/student/BINF6111_2020/test/sample_input/FULL_RUN_SORT/", False)
	coordinates_barcodes = create_coordinates_barcodes_dictionary (filtered_read_one, barcode_matrix, dbc_matrix, indices_list)
	line_count = count_lines (filtered_read_one)
	# full lines = 1013795888
	#line_count = 1013795888


	# SPLITS READ 2 INTO SMALLER FILES has to be divisible by 4 to get output (CHANGE -l)
	lines_per_file = (line_count/8)
	while lines_per_file%4 != 0:
		lines_per_file += 2

	print(lines_per_file)
	os.system("split -l{} {} 100M_L1_R2/split_".format(int(lines_per_file), read_two))

	x = []

	for split_file in os.listdir("100M_L1_R2"):
		x.append("100M_L1_R2/{}".format(split_file))

	#x = split_read_two (read_two, line_count, 8, False)

	create_fastq_files (dir_name, indices_list, barcode_matrix)
	create_threads (x, barcode_matrix, coordinates_barcodes, dir_name, indices_list)

	# Makes a log file of runtimes
	runtime_log = os.system("touch CA_LOG.txt")
	log_file = open("CA_LOG.txt", "a")
	log_file.write("Runtime = {} h/m/s. Data set = {}\n".format(str(datetime.timedelta(seconds=time.time() - start_time)), dir_name))
	log_file.close()

	print("\nCELL ASSIGNMENT SUCCESSFUL")
	print("Runtime = {} h/m/s.\n".format(str(datetime.timedelta(seconds=time.time() - start_time))))
