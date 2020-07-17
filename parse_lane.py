# Author: Chelsea Liang (parse read one + merging functions)
# Author: David Nguyen (cell assignment)
# Function: Filters read one by cell barcode and library indices, writes read two to group_indices.fastqs

import os
import re
import sys
import time
import datetime
from functions import *

# TODO
## Error checking will be done by master script

if __name__ == '__main__':

	# VARIABLES

	## Arguments
	read_one = sys.argv[1]
	csv_matrix = sys.argv[2]
	desired_barcodes = sys.argv[3]
	indices_path = sys.argv[4]
	experiment_name = sys.argv[5]
	append_target_directory = True # sys.argv[6]

	## Derived
	working_dir = os.path.dirname(read_one)
	read_two = read_one.replace('_R1_','_R2_')
	log_path = working_dir + '/pipeline_log.txt'
	output_directory = (working_dir + '/SORTED_GROUPS')
	message = []
	start_time = time.time()

	## Writing to log
	message.append('read_one = ' + read_one)
	message.append('csv_matrix = ' + csv_matrix)
	message.append('indices_path = ' + indices_path)
	message.append('experiment_name = ' + experiment_name)
	message.append('working_dir = ' + working_dir)
	message.append('read_two = ' + read_two)
	message.append('log_path = ' + log_path)
	message.append('output_directory = ' + output_directory)
	write_to_log (start_time, log_path, '\n'.join(message))
	message = []
	start_time = time.time()

	# MAIN FUNCTIONS
	barcode_matrix = read_matrix (csv_matrix)
	indices_list = create_indices_list (indices_path)
	dir_name = create_target_directory (output_directory, append_target_directory)
	coordinates_barcodes = coordinates_barcodes_dictionary (read_one, barcode_matrix, indices_list)


	# write_to_log (start_time, log_path, '\n'.join(message))
	
	

	