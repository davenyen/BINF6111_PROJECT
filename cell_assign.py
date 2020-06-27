import sys
import collections
import os
import time
import csv
from itertools import islice
from functions import *

# python3 cell_assign.py /Users/student/BINF6111_2020/data/test_barcode.csv /Users/student/BINF6111_2020/test/output/PilotCROP_C_1_S1_L001_R1_001.fastq /Users/student/BINF6111_2020/test/output/PilotCROP_C_1_S1_L001_R2_001.fastq

# to avoid a stupid error i have to do
__all__ = ["read_matrix", "create_target_directory", "coordinates_barcodes_dictionary", "consume"]

# cmd line -> python3 {matrix} {read1} {read2}

# Read in matrix csv
# - Associate barcode from read one to sequence in read two
# - When file is list of groups, a list of cell barcodes from those groups are
# created
# - Identify cell barcode from read one, allocate sequence from read 2 to a
# particular group 

###### TO DO ######
# 1. match coordinate of read1 with read2
# 2. match read1 barcode with matrix (gets target)
# 3. grab read2 sequence and put into group directory (target) (WILL JUST GRAB HEADER AND SEQUENCE FOR NOW)
#     - quality scores as well and header?
# 4. error cases and handling last!

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Writes to sorted fastq files 
def write_fastq (void):
	pass

# MAIN
if __name__ == '__main__':

	# VARIABLES
	csv_matrix = sys.argv[1]
	read_one = sys.argv[2]
	read_two = sys.argv[3]

	
	barcode_table = read_matrix (csv_matrix)
	create_target_directory (barcode_table)
	coordinates_barcodes = coordinates_barcodes_dictionary (read_one)

	# Matches coordinates read1 - read2
	file = open(read_two)
	coordinates = ''
	sequence = ''
	success_count = 0
	count = 0
	header = ''

	with file:
		for i, line in enumerate(file, 1):
		
			# check line if it is header, save to maybe print later
			if line[0] == "@":
				header = line
				coordinates = ':'.join(line.split(':')[4:6])

			# if it's not a header must be a sequence
			else:
				sequence = ''.join(line[0:])

				# GET TARGET/GROUP then write a fastq file with read2 data into group/directory
				if coordinates in coordinates_barcodes:
					if coordinates_barcodes[coordinates] in barcode_table.keys():
						try:
							target_file = ("sorted_target_groups/{}/{}.fastq".format(barcode_table[coordinates_barcodes[coordinates]], barcode_table[coordinates_barcodes[coordinates]]))
							f = open(target_file, "w")
							f.write("{}\n{}".format(header, sequence))
							f.close()
						except:
							target_file = ("sorted_target_groups/{}/{}.fastq".format(barcode_table[coordinates_barcodes[coordinates]], barcode_table[coordinates_barcodes[coordinates]]))
							f = open(target_file, "a")
							f.write("{}\n{}".format(header, sequence))
							f.close()

						success_count += 1

			count += 1
			if count == 100:
				break

			# will skip lines 3 and 4 for performance
			if not i % 2:
				consume(file, 2)

	print("\nSUCCESS COUNT = {}".format(str(success_count)))



