# Author:
# Function: Holds functions for cell_assign.py
# Version: 1.4

import sys
import collections
import os
import time
import csv
import mmap
from itertools import islice

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Creates a fastq file with sequences that match read1 coordinates and are in sorted groups based on the target
def create_sorted_fastq_file (read_two_file, barcode_matrix, read1_coordinates_barcodes, dir_name):

	# read2 lines = 1013795888
	# test lines = 200000

	file = open(read_two_file)
	file_set = set()

	with file:
		for line in file:
			# if it's not a header must be a sequence/quality/+  
			# if the coordinate exists in read1, then it will proceed to write the other 2 lines to the file.
			if line[0] != "@":
				if new_header == True:
					sequence = line
					# GET TARGET/GROUP then write a fastq file with read2 data into group/directory
					if coordinates in read1_coordinates_barcodes:
						if read1_coordinates_barcodes[coordinates][9:] in barcode_matrix.keys():
							group_name = barcode_matrix[read1_coordinates_barcodes[coordinates][9:]]
							#barcode_group = read1_coordinates_barcodes[coordinates][0:8]
							# If file and directory exists then append to it
							if os.path.isdir("{}/{}".format(dir_name, group_name)) == True:
								# if errors then add if else "if os.path.isfile("{}/{}/{}.fastq".format(dir_name, group_name, group_name)) == True:"
								# Assumes since directory exists then file must too, so append for speed
								try:
									target_file = ("{}/{}/{}.fastq".format(dir_name, group_name, read2_indice))
									f = open(target_file, "a")
									f.write("{}{}".format(header, sequence))
								except:
									f.write("{}{}".format(header, sequence))
							# If output/(group) doesn't exist then makes it and writes the first 2 lines to it
							else:
								os.makedirs("{}/{}".format(dir_name, group_name))
								# Creates fastq file for respective group 
								try:
									target_file = ("{}/{}/{}.fastq".format(dir_name, group_name, read2_indice))
									f = open(target_file, "w")
									f.write("{}{}".format(header, sequence))
								except:
									f.write("{}{}".format(header, sequence))
								file_set.add(f)
							new_header = False
				else:
					# If the files have incorrect input change group_name below to 'barcode_matrix[read1_coordinates_barcodes[coordinates]]'
					f.write("{}".format(line))
			# Else the line must be the header
			else:
				header = line
				coordinates = ':'.join(line.split(':')[4:6])
				read2_indice = line.split(':')[9].rstrip()
				new_header = True

	return file_set

# Reads matrix csv and returns a data structure (dictionary) for O(1) access time
def read_matrix (csv_matrix):
	barcode_dictionary = {}

	# Reads cell barcode matrix and saves only: barcode + target into dictionary
	with open(csv_matrix, 'r') as file:
	    reader = csv.reader(file)
	    skip_first = True
	    for row in reader:
			# Skips first row because there is no data in the first row
	    	if skip_first == True: 
	    		skip_first = False
	    		continue
    		else:
		        barcode_dictionary[row[1].rstrip()] = row[5]

	return barcode_dictionary

# Creates target/group directories
def create_target_directory (barcode_table, read_two):
	read_two = read_two.split("/")[-1:]
	read_two = read_two[0].split("L")[:-1]
	dir1 = ("/Users/student/BINF6111_2020/test/output/{}SORTED_GROUPS".format(read_two[0]))

	# Creates the directory for the sorted groups to go into
	try:
		os.makedirs(dir1)
	except: #If excepts then the directory already exists 
		command = input("The directory output '{}' already exists, would you like to append to it? (Y/N) (Default will rewrite the directory) ".format(dir1))
		# Appends to current directory
		if command.lower() == "y" or command.lower() == "yes":
			pass
		# Rewrites the directory with new output
		else:
			os.system("rm -r {}".format(dir1))
		pass

	return dir1

# Closes all fastq files at the end 
def close_all_files (files_set):
	for file in files_set:
		file.close()
	pass

# Make a dictionary of read1 where {barcode: coordinate} (USED FOR CELL_ASSIGN.PY)
def coordinates_barcodes_dictionary (read1_file):

	# read1_numlines = 1013795888 (same as read2 apparently?) (half actually because we only rad barcode + coord) 506897944
	read1_dictionary = {}
	file = open(read1_file)

	# Goes through read1 and saves barcode + coordinate into a dictionary for O(1)
	with file:
		for i, line in enumerate(file, 1):
			
			# check line if it is header, save to maybe print later
			if line[0] == "@":
				coordinates = ':'.join(line.split(':')[4:6])
				barcode = ''.join(line.split(':')[9]).rstrip() + ":"
			# if it's not a header must be a sequence
			else:
				# barcode is first 16 bp and idice is first 6
				barcode += line[0:16]
				read1_dictionary[coordinates] = barcode
				
			# will skip lines 3 and 4 for performance
			if not i % 2:
				consume(file, 2)

	file.close()
	return read1_dictionary

# stolen from chelsea
def consume(iterator, n=None):
    "Advance the iterator n-steps ahead. If n is None, consume entirely."
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)

# ERROR CHECKING for cell_assign.py
def error_check (csv_matrix, read1, read2):
	# (1): Exit if arguments not 4 (invalid)
	if len(sys.argv) != 4:
		print("\nInsufficient arguments entered. Input must have: barcode.csv, read1 and read2.\nExiting...\n")
		exit()
	# (2): Exit if the first input is not a csv file (invalid)
	if csv_matrix[-4:] != ".csv":
		print("\nError, '{}' is not a csv file.\nExiting ...\n".format(sys.argv[1]))
		exit()
	# (3): Exit if second input is not a fastq file (invalid)
	if read1[-6:] != ".fastq":
		print("\nError, '{}' is not a fastq file.\nExiting ...\n".format(sys.argv[2]))
		exit()
	# (4): Exit if third input is not a fastq file (invalid)
	if read2[-6:] != ".fastq":
		print("\nError, '{}' is not a fastq file.\nExiting ...\n".format(sys.argv[3]))
		exit()
	pass