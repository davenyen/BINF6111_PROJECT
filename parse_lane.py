# Author: Chelsea Liang (parse read one + merging functions)
# Author: David Nguyen (cell assignment)
# Function: Filters read one by cell barcode and library indices, writes read two to group_indices.fastqs

import os
import re
import sys
import time
import datetime
from functions import read_matrix, create_indices_list, create_coordinates_barcodes_dictionary, create_target_directory
from functions import create_fastq_files, split_read_two, create_sorted_fastq_file, write_to_log, create_threads, close_all_files

## TODO
## Error checking will be done by master script

if __name__ == '__main__':

	# VARIABLES

	## Arguments
	read_one = sys.argv[1]
	csv_matrix = sys.argv[2]
	desired_barcodes = sys.argv[3]
	indices_path = sys.argv[4]
	experiment_name = sys.argv[5]
	num_threads = 8 # sys.argv[6]
	append_target_directory = False # sys.argv[7]
	split_shortcut_dir = False # sys.argv[8] ONLY FOR TESTING PURPOSES IF YOU DONT PUT A DIR HERE IT WILL SPLIT
	
	## Derived
	working_dir = os.path.dirname(read_one)
	read_two = read_one.replace('_R1_','_R2_')
	message = []
	start_time = time.time()

	## Settings (can tweak)
	log_path = working_dir + '/pipeline_log.txt'
	output_dir = (working_dir + '/SORTED_GROUPS')
	maaaaaaaaany_lines = 100000000

	## Writing to log
	message.append('read_one = ' + read_one)
	message.append('csv_matrix = ' + csv_matrix)
	message.append('indices_path = ' + indices_path)
	message.append('experiment_name = ' + experiment_name)
	message.append('working_dir = ' + working_dir)
	message.append('read_two = ' + read_two)
	message.append('log_path = ' + log_path)
	message.append('output_dir = ' + output_dir)
	write_to_log (start_time, log_path, '\n'.join(message))
	message = []
	

	# MAIN FUNCTIONS

	## Set up
	desired_barcodes = read_matrix (desired_barcodes)
	group_barcode_matrix = read_matrix (csv_matrix)
	indices_list = create_indices_list (indices_path)
	dir_name = create_target_directory (output_dir, append_target_directory)
	file_dictionary = create_fastq_files (dir_name, indices_list, group_barcode_matrix)

	start_time = time.time()
	coord_barcode_matrix, line_count = create_coordinates_barcodes_dictionary (read_one, group_barcode_matrix, desired_barcodes, indices_list)

	if line_count >= maaaaaaaaany_lines and num_threads != 0:
		# split file function, optimise on num_threads variable
		# run on split files
		split_files, tmp_dir = split_read_two (read_two, line_count, 8, split_shortcut_dir)
		create_threads (split_files, group_barcode_matrix, coord_barcode_matrix, dir_name, indices_list, file_dictionary)
		close_all_files (file_dictionary.values())
		os.system("rm -r {}".format(tmp_dir))
		message.append("COMPLETED")
	else:
		create_sorted_fastq_file (read_two, group_barcode_matrix, coord_barcode_matrix, output_dir, indices_list, file_dictionary)
		message.append("COMPLETED")


	write_to_log (start_time, log_path, '\n'.join(message))
	
	

	