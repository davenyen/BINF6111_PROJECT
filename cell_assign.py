# Author: David Nguyen
# Function: Assigns cells to groups/targets
# Version: 1.5

import sys
import os
import time
import datetime
from collections import Counter
from functions import create_fastq_files, read_matrix, create_target_directory, create_sorted_fastq_file, coordinates_barcodes_dictionary, error_check, close_all_files, create_indices_list, myThread

# Input: python3 cell_assign.py {matrix.csv} {read1.fastq} {read2.fastq}
# Output: sorted_target_groups/{lots of groups}/group.fastq (for each group)

# Sample run cmd line:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/PilotCROP_L1_R1.fastq symlinks/PilotCROP_L1_R2.fastq symlinks/Indices_A1.txt

# TEST RUN USE THIS:
# python3 cell_assign.py symlinks/barcode_a1.csv symlinks/SML_TEST_L1_R1.fastq symlinks/SML_TEST_L1_R2.fastq symlinks/Indices_A1.txt

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
	start_time = time.time()
	
	# Run error checking
	error_check (csv_matrix, filtered_read_one, read_two, indices)

	# SPLITS READ 2 INTO SMALLER FILES has to be divisible by 4 to get output (CHANGE -l)
	try:
		os.makedirs("split_dir")
	except:
		pass

	# splits into 2/4/8 based on lines%4 == 0
	# splits 4
	#os.system("split -l253448972 {} split_dir/split_".format(read_two))
	# splits 8
	#os.system("split -l126724486 {} split_dir/split_".format(read_two))

	split_file_list = []

	for split_file in os.listdir("split_dir"):
		split_file_list.append("split_dir/{}".format(split_file))

	# Main functions
	barcode_matrix = read_matrix (csv_matrix)
	indices_list = create_indices_list (indices)
	dir_name = create_target_directory (barcode_matrix, read_two)
	coordinates_barcodes = coordinates_barcodes_dictionary (filtered_read_one, barcode_matrix, indices_list)

	# testing
	open_files = create_fastq_files (dir_name, indices_list, barcode_matrix)
	
	# create loop for thread making probably and starting
	thread1 = myThread(1, "Thread 1", split_file_list[0], barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	thread2 = myThread(2, "Thread 2", split_file_list[1], barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	thread3 = myThread(3, "Thread 3", split_file_list[2], barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	thread4 = myThread(4, "Thread 4", split_file_list[3], barcode_matrix, coordinates_barcodes, dir_name, indices_list)

	thread5 = myThread(5, "Thread 5", split_file_list[4], barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	thread6 = myThread(6, "Thread 6", split_file_list[5], barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	thread7 = myThread(7, "Thread 7", split_file_list[6], barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	thread8 = myThread(8, "Thread 8", split_file_list[7], barcode_matrix, coordinates_barcodes, dir_name, indices_list)

	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	thread5.start()
	thread6.start()
	thread7.start()
	thread8.start()

	#os.system("rm -r split_dir")

	close_all_files (open_files)

	#files_set = create_sorted_fastq_file (read_two, barcode_matrix, coordinates_barcodes, dir_name, indices_list)
	#close_all_files (files_set)

	# Makes a log file of runtimes
	runtime_log = os.system("touch CA_LOG.txt")
	log_file = open("CA_LOG.txt", "a")
	log_file.write("Runtime = {} h/m/s. Data set = {}\n".format(str(datetime.timedelta(seconds=time.time() - start_time)), dir_name))
	log_file.close()

	print("\nCELL ASSIGNMENT SUCCESSFUL")
	print("Runtime = {} h/m/s.\n".format(str(datetime.timedelta(seconds=time.time() - start_time))))
