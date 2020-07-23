# Author: David Nguyen
# Function: Assigns cells to groups/targets
# Version: 1.5

import sys
import os
import time
import datetime
import threading
from collections import Counter
from functions import create_threads, split_read_two, create_fastq_files, read_matrix
from functions import create_target_directory, create_sorted_fastq_file, create_coordinates_barcodes_dictionary
from functions import close_all_files, create_indices_list, myThread, check_correctness

# Input: python3 cell_assign.py {matrix.csv} {read1.fastq} {read2.fastq}
# Output: sorted_target_groups/{lots of groups}/group.fastq (for each group)

# Full run test:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/PilotCROP_L1_R1.fastq symlinks/PilotCROP_L1_R2.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/test/check_master_script/barcodesA1.txt
# L2:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/PilotCROP_L2_R1.fastq symlinks/PilotCROP_L2_R2.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/test/check_master_script/barcodesA1.txt

# 100M test:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/100mil_test/100MILL_PilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/100mil_test/100MILL_PilotCROP_C_1_S1_L001_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt
# L2:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/100mil_test/100MILL_PilotCROP_C_1_S1_L002_R1_001.fastq /Users/student/BINF6111_2020/test/100mil_test/100MILL_PilotCROP_C_1_S1_L002_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt

# 10M test:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/10mil_run/10_milPilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/10mil_run/10_milPilotCROP_C_1_S1_L001_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt
# L2:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/10mil_run/10_milPilotCROP_C_1_S1_L002_R1_001.fastq /Users/student/BINF6111_2020/test/10mil_run/10_milPilotCROP_C_1_S1_L002_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt

# 500K test:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/500K_test/500000_PilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/500K_test/500000_PilotCROP_C_1_S1_L001_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt
# L2:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/500K_test/500000_PilotCROP_C_1_S1_L002_R1_001.fastq /Users/student/BINF6111_2020/test/500K_test/500000_PilotCROP_C_1_S1_L002_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt

# 2k test:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/2000_test/2000_PilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/2000_test/2000_PilotCROP_C_1_S1_L001_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt
# L2:
# python3 cell_assign.py symlinks/barcode_a1.csv /Users/student/BINF6111_2020/test/2000_test/2000_PilotCROP_C_1_S1_L002_R1_001.fastq /Users/student/BINF6111_2020/test/2000_test/2000_PilotCROP_C_1_S1_L002_R2_001.fastq symlinks/Indices_A1.txt /Users/student/BINF6111_2020/data/barcodesA1.txt

# Read in matrix csv
# - Associate barcode from read one to sequence in read 2
# - When file is list of groups, a list of cell barcodes from those groups are
# 	created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# 	particular group 

# MAIN
if __name__ == '__main__':

	# VARIABLES
	csv_matrix = sys.argv[1]
	filtered_read_one = sys.argv[2]
	read_two = sys.argv[3]
	indices = sys.argv[4]
	desired_barcodes = sys.argv[5]
	start_time = time.time()
	append = True
	split_directory = "/Users/student/BINF6111_2020/test/10mil_run/SPLIT_L2"
	output_directory = "/Users/student/BINF6111_2020/test/10mil_run/D_SORT"

	#"/Users/student/BINF6111_2020/test/full_data/L1_R2_SPLIT_8/"
	#"/Users/student/BINF6111_2020/test/full_data/D_Sorted_Groups/"

	#correct_file = create_indices_list("/Users/student/BINF6111_2020/test/10mil_run/CORRECT_HEADERS")
	#incorrect_file = create_indices_list("/Users/student/BINF6111_2020/test/10mil_run/L1_ERRORS")
	#if check_correctness ("/Users/student/BINF6111_2020/test/10mil_run/CORRECT_SORT", correct_file) == False:
	#	print("Failed")
	#else:
		#print("Success")
	#exit()

	# Main functions
	barcode_matrix = read_matrix (csv_matrix)
	dbc_matrix = read_matrix (desired_barcodes)
	indices_list = create_indices_list (indices)
	# Change append to true for Lane 2
	create_target_directory (output_directory, append)
	
	coordinates_barcodes, line_count = create_coordinates_barcodes_dictionary (filtered_read_one, barcode_matrix, dbc_matrix, indices_list)
	x = split_read_two (read_two, line_count, 8, split_directory)
	file_dic = create_fastq_files (output_directory, indices_list, barcode_matrix)
	create_threads (x, barcode_matrix, coordinates_barcodes, output_directory, indices_list, file_dic)
	close_all_files (file_dic.values())

	# Makes a log file of runtimes
	runtime_log = os.system("touch CA_LOG.txt")
	log_file = open("CA_LOG.txt", "a")
	log_file.write("Runtime = {} h/m/s. Data set = {}\n".format(str(datetime.timedelta(seconds=time.time() - start_time)), output_directory))
	log_file.close()

	print("\nCELL ASSIGNMENT SUCCESSFUL")
	print("Runtime = {} h/m/s.\n".format(str(datetime.timedelta(seconds=time.time() - start_time))))
