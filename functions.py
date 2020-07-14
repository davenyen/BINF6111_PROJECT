# Author:
# Function: Holds functions for cell_assign.py and parse_fastq
# Version: 1.4

import sys
import collections
import os
import time
import csv
from itertools import islice

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Creates a fastq file with sequences that match read1 coordinates and are in sorted groups based on the target
def create_sorted_fastq_file (read_two_file, barcode_matrix, r_one_coordinates_dict, dir_name):

	# Opens read2 file to match with read1, file_set used to memorise open files to close later
	file = open(read_two_file)
	file_set = set()
	coordinates = ''
	skipper = True

	with file:
		for line in file:
			# if it's not a header must be a sequence/quality/+  
			# if the coordinate exists in read1, then it will proceed to write the other 2 lines to the file.
			if line[0] != "@" and skipper == False:
				if new_header == False:
					f.write("{}".format(line))
				else:
					sequence = line
					# GET TARGET/GROUP then write a fastq file with read2 data into group/directory
					if r_one_coordinates_dict[coordinates] in barcode_matrix.keys():
						group_name = barcode_matrix[r_one_coordinates_dict[coordinates]]
						#read1_indice = r_one_coordinates_dict[coordinates][0:8]
						# If file and directory exists then append to it
						if os.path.isdir("{}/{}".format(dir_name, group_name)) == True:
							# Assumes since directory exists then file must too, so append for speed
							try:
								target_file = ("{}/{}/{}.fastq".format(dir_name, group_name, read_two_indice))
								f = open(target_file, "a")
								f.write("{}{}".format(header, sequence))
							except:
								f.write("{}{}".format(header, sequence))
						# If output/(group) doesn't exist then makes it and writes the first 2 lines to it
						else:
							os.makedirs("{}/{}".format(dir_name, group_name))
							# Creates fastq file for respective group 
							try:
								target_file = ("{}/{}/{}.fastq".format(dir_name, group_name, read_two_indice))
								f = open(target_file, "w")
								f.write("{}{}".format(header, sequence))
							except:
								f.write("{}{}".format(header, sequence))
							file_set.add(f)
						new_header = False
			# Else the line must be the header
			else:
				header = line
				coordinates = ':'.join(line.split(':')[4:6])
				if coordinates not in r_one_coordinates_dict:
					skipper = True
				else:
					skipper = False
					read_two_indice = line.split(':')[9].rstrip()
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
	dir1 = ("/Users/student/BINF6111_2020/test/sample_input/{}SORTED_GROUPS".format(read_two[0]))

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

# Make a dictionary of read1 where {coordinate: barcode} 
# If read_one barcode does not exist in the matrix then skip (saves time)
def coordinates_barcodes_dictionary (read_one, barcode_matrix):

	read1_dictionary = {}
	file = open(read_one)

	# Goes through read1 and saves barcode + coordinate into a dictionary for O(1)
	with file:
		for i, line in enumerate(file, 1):
			
			# check line if it is header, save to maybe print later
			if line[0] == "@":
				coordinates = ':'.join(line.split(':')[4:6])
				#barcode = ''.join(line.split(':')[9]).rstrip() + ":"
			# if it's not a header must be a sequence
			else:
				# barcode is first 16 bp
				barcode = ''.join(line[0:16])
				# If barcode doesn't exist then skip otherwise adds it to the dictionary
				if barcode in barcode_matrix:
					read1_dictionary[coordinates] = barcode
				else:
					if not i % 2:
						consume(file, 2)
					continue
			# will skip lines 3 and 4 for performance
			if not i % 2:
				consume(file, 2)

	file.close()
	return read1_dictionary

# DUPLICATE FUNCTION
# SUGGESTION IS TO REPLACE ABOVE FUNCTION AND JUST READ IN DICTIONARY CREATED
# IN parse_read1_fastq.py
def filter_read_one (read_one, cell_barcode_coordinates_table, filtered_read_one):
	# x-y coordinates to barcode dictionary to link read 1 and read 2:
	read1_dictionary = {}
	barcodes = cell_barcode_coordinates_table
	fastq_to_append = open(filtered_read_one, "a+")

	# debugging
	filtered_out = open("filtered_out_reads.fastq", "a+")
	
	file = open(read_one)

	with file:
		for i, line in enumerate(file, 1):
			
			# check line if it is header, save to maybe print later
			if line[0] == "@":
				coordinates = ':'.join(line.split(':')[4:6])
				header = line

			# if it's not a header must be a sequence
			else:
				# barcode is first 16 bp
				barcode = ''.join(line[0:16])

				# check if barcode exists in dictionary
				try:
					group_type = barcodes[barcode]
					if group_type:
						read1_dictionary[coordinates] = barcode
						fastq_to_append.write(header)
						fastq_to_append.write(line)
				
				# else, isn't a target barcode
				except:
					filtered_out.write(header)
					filtered_out.write(line)

				
			# will skip lines 3 and 4 for performance
			if not i % 2:
				consume(file, 2)
	file.close()
	return read1_dictionary		

# Closes all fastq files at the end 
def close_all_files (files_set):
	for file in files_set:
		file.close()
	pass

# Append to a dictionary to be read in by other python script
def write_out_dictionary_csv (cell_barcode_coordinates_table, dictionary_path):
	writer = csv.writer(open(dictionary_path, "a+"))
	for key, val in cell_barcode_coordinates_table.items():
		writer.writerow([key, val])

# This will allow iterating through the only header and sequence lines
# to improve performance
# Function taken from the Python Package Index:
# https://docs.python.org/3/library/itertools.html#itertools-recipes
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