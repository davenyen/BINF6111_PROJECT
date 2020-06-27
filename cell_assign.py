import sys
import os
from functions import read_matrix, create_target_directory, create_sorted_fastq_file, coordinates_barcodes_dictionary, error_check

# REMOVE COUNTS FROM FUNCTIONS.PY FOR FULL OUTPUT (ATM LIMITED TO 10,000)

# Input: python3 cell_assign.py {matrix.csv} {read1.fastq} {read2.fastq}
# Output: sorted_target_groups/{lots of groups}/group.fastq (for each group)
# Sample run cmd line:
# python3 cell_assign.py /Users/student/BINF6111_2020/data/test_barcode.csv /Users/student/BINF6111_2020/test/output/PilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/output/PilotCROP_C_1_S1_L001_R2_001.fastq

# Read in matrix csv
# - Associate barcode from read one to sequence in read 2
# - When file is list of groups, a list of cell barcodes from those groups are
# 	created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# 	particular group 

# MAIN
if __name__ == '__main__':

	# BLANK SLATE, removes the folder so you can create new sorted files
	if os.path.isdir("sorted_target_groups") == True:
		os.system("rm -r sorted_target_groups")
	
	# VARIABLES
	csv_matrix = sys.argv[1]
	read_one = sys.argv[2]
	read_two = sys.argv[3]
	
	# Run error checking
	error_check (csv_matrix, read_one, read_two)
	
	# Main functions
	barcode_table = read_matrix (csv_matrix)
	create_target_directory (barcode_table)
	coordinates_barcodes = coordinates_barcodes_dictionary (read_one)
	create_sorted_fastq_file (read_two, barcode_table, coordinates_barcodes)

	print("\nCELL ASSIGNMENT SUCCESSFUL\n")

