# Author: Chelsea Liang
# Function: Parses read one fastq of a sample and filters by barcode
# Version: 1.4

import sys
from itertools import islice
import collections
import os
import time
from functions import consume, read_matrix, filter_read_one, write_out_dictionary_csv

# run cases
# output_path=/Users/student/BINF6111_2020/test/output
# file=testR1_1.fastq
# list_path='/Users/student/BINF6111_2020/test/test_list_barcodes.txt'
# experiment_name=PilotCROP_C_1_S1
# read=R1
# python3 parse_read1_fastq.py ${list_path} ${output_path}/${file} ${experiment_name}

# OPTIMISATION IDEAS:
# (1) Pass the coordinates_barcodes matrix to cell assign (merge scripts or write out?)

# Input: ${data_path}/${file} {output_path}/${file} ${list_path} ${experiment_name}
# Output: filtered_read_1.py and written out dictionary o

 
# This script will open a file and go through every header and sequence line
# for loop of every desired cell barcode
# if match
	# write to new file
	# else next



# MAIN
if __name__ == '__main__':

	# VARIABLES
	csv_matrix = sys.argv[2]
	read_one = sys.argv[1]
	experiment_name = sys.argv[3]
	filtered_read_one = os.path.dirname(read_one) + '/' + 'filtered' + experiment_name + '_R1.fastq'
	dictionary_path = os.path.dirname(read_one) + '/cell_barcode_coordinates.csv'
	start_time = time.time()

	# Main functions
	cell_barcode_coordinates_table = read_matrix (csv_matrix)
	cell_barcode_coordinates_table = filter_read_one (read_one, cell_barcode_coordinates_table, filtered_read_one)
	write_out_dictionary_csv (cell_barcode_coordinates_table, dictionary_path)
