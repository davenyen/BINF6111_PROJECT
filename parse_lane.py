# Author: Chelsea Liang (parse read one + merging functions)
# Author: David Nguyen (cell assignment)
# Function: Filters read one by cell barcode and library indices, writes read two to group_indices.fastqs

import os
import re
import sys
import time
import datetime
from functions import read_matrix, create_indices_list, create_coordinates_barcodes_dictionary
from functions import create_target_directory, convert_groups_to_barcodes
from functions import create_fastq_files, split_read_two, create_sorted_fastq_file
from functions import write_to_log, create_threads, close_all_files

if __name__ == '__main__':

	# VARIABLES

	## Arguments
	read_one = sys.argv[1]
	csv_matrix = sys.argv[2]
	desired_barcodes = sys.argv[3]
	groups = bool(sys.argv[4])
	indices_path = sys.argv[5]
	experiment_name = sys.argv[6]
	append_target_directory = bool(sys.argv[7])
	num_threads = sys.argv[8]
	
	## Derived
	working_dir = os.path.dirname(read_one)
	read_two = read_one.replace('_R1_','_R2_')
	message = []
	start_time = time.time()

	## Settings (can tweak)
	log_path = (working_dir + '/pipeline_log.txt')
	output_dir = (working_dir + '/SORTED_GROUPS')
	maaaaaaaaany_lines = 99999999

	## Writing to log
	message.append('read_one = ' + read_one)
	message.append('csv_matrix = ' + csv_matrix)
	message.append('indices_path = ' + indices_path)
	message.append('experiment_name = ' + experiment_name)
	message.append('working_dir = ' + working_dir)
	message.append('read_two = ' + read_two)
	message.append('log_path = ' + log_path)
	message.append('output_dir = ' + output_dir)
	message.append('append_target_directory = ' + str(append_target_directory))
	message.append('num_threads = ' + str(num_threads))
	write_to_log (start_time, log_path, '\n'.join(message))
	message = []
	
	# MAIN FUNCTIONS

	## Set up
	start_time = time.time()
	write_to_log (start_time , log_path, "Start set up")
	group_barcode_matrix = read_matrix (csv_matrix)
	indices_list = create_indices_list (indices_path)
	create_target_directory (output_dir, append_target_directory)
	desired_barcodes = read_matrix (desired_barcodes)
	if groups:
		desired_barcodes, group_barcode_matrix = convert_groups_to_barcodes (desired_barcodes, group_barcode_matrix)
	file_dictionary = create_fastq_files (output_dir, indices_list, group_barcode_matrix)
	write_to_log (start_time, log_path, "Finished set up")

	start_time = time.time()
	write_to_log (start_time, log_path, "Beginning creation of coord_dic")
	coord_barcode_matrix, line_count = create_coordinates_barcodes_dictionary (read_one, group_barcode_matrix, desired_barcodes, indices_list)
	write_to_log (start_time, log_path, "Finished creation of coord_dic")

	start_time = time.time()
	write_to_log (start_time, log_path, "Beginning creation of cell assignment")
	if line_count >= maaaaaaaaany_lines and num_threads != 0:
		# split file function, optimise on num_threads variable
		split_start = time.time()
		write_to_log (split_start, log_path, "Beginning file split")
		split_files, tmp_dir = split_read_two (read_two, line_count, num_threads)
		write_to_log (split_start, log_path, "Finished file split")

		# run on split files
		write_start = time.time()
		write_to_log (write_start, log_path, "Beginning writing out grouped fastq")
		create_threads (split_files, group_barcode_matrix, coord_barcode_matrix, output_dir, indices_list, file_dictionary)
		write_to_log (write_start, log_path, "Finished writing out grouped fastq")
		close_all_files (file_dictionary.values())
		os.system("rm -r {}".format(tmp_dir))
	else:
		create_sorted_fastq_file (read_two, group_barcode_matrix, coord_barcode_matrix, output_dir, indices_list, file_dictionary)
	
	write_to_log (start_time, log_path, "End of cell assignment")


	