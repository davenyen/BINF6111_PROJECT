# Author:
# Function: Holds functions for parse_lane.py
# Version: 1.7

import os
import re
import sys
import time
import csv
import datetime
import threading
import subprocess
import collections
from itertools import islice

############################################################################
################################ Classes ###################################
############################################################################

# Thread used for cell_assign for now
class myThread (threading.Thread):
	def __init__(self, threadID, name, read_two_file, barcode_matrix, r_one_coordinates_dict, dir_name, indices_list):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.read_two_file = read_two_file
		self.barcode_matrix = barcode_matrix
		self.r_one_coordinates_dict = r_one_coordinates_dict
		self.dir_name = dir_name
		self.indices_list = indices_list

	def run(self):
		print("Starting " + self.name)
		create_sorted_fastq_file(self.read_two_file, self.barcode_matrix, self.r_one_coordinates_dict, self.dir_name, self.indices_list)
		print("Exiting " + self.name)

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Creates a fastq file with sequences that match read1 coordinates and are in sorted groups based on the target
def create_sorted_fastq_file (read_two_file, barcode_matrix, r_one_coordinates_dict, dir_name, indices_list):

	# Opens read2 file to match with read1, file_set used to memorise open files to close later
	file = open(read_two_file)
	coordinates = ''
	new_header = True
	test_list = []
	files_to_close = set()

	for line in file:
		# if it's not a header must be a sequence/quality/+  
		# if the coordinate exists in read1, then it will proceed to write the other 2 lines to the file.

		if line[0] != "@":
			if new_header == False:
				f.write("{}".format(line))
			elif coordinates in r_one_coordinates_dict.keys():
				sequence = line
				# GET TARGET/GROUP then write a fastq file with read2 data into group/directory
				if r_one_coordinates_dict[coordinates] in barcode_matrix.keys():
					group_name = barcode_matrix[r_one_coordinates_dict[coordinates]]
					# If file and directory exists then append to it
					if os.path.isdir("{}/{}".format(dir_name, group_name)) == True:
						# Assumes since directory exists then file must too, so append for speed
						#try:
						target_file = ("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, read_two_indice))
						f = open(target_file, "a")
						files_to_close.add(f)
							#f.write("{}{}".format(header, sequence))
						#except:
						f.write("{}{}".format(header, sequence))
					# If output/(group) doesn't exist then makes it and writes the first 2 lines to it
					#else:
						#os.makedirs("{}/{}".format(dir_name, group_name))
						# Creates fastq file for respective group 
						#try:
							#target_file = ("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, read_two_indice))
							#f = open(target_file, "w")
							#f.write("{}{}".format(header, sequence))
						#except:
							#f.write("{}{}".format(header, sequence))
					new_header = False
		# Else the line must be the header
		else:
			header = line
			coordinates = ':'.join(line.split(':')[4:6])
			read_two_indice = line.split(':')[9].rstrip()
			if coordinates not in r_one_coordinates_dict.keys() or read_two_indice not in indices_list:
				test_list.append(line)
				
				consume(file, 3)
			else:
				#skipper = False
				new_header = True

	close_all_files(files_to_close)
	



# Combines create_fastq_files and coordinates_barcodes_dictionary
def create_coordinates_barcodes_dictionary (read_one, barcode_matrix, desired_barcodes, indices_list):
	read_one_dic = {}
	header = ''
	coordinates = ''
	read_one_file = open(read_one, 'r')
	error_read_one_file = open(read_one + '.error' , 'a+')

	for i, line in enumerate(read_one_file, 1):

		# check line if it is header
		if line[0] == "@":
			line_indice = ''.join(line.split(':')[9]).rstrip()
			
			# faster if this happens so maybe we should have a flag to turn it on and off?
			# if line_indice not in indices_list:
			# 	consume(read_one_file, 3)
			# 	continue
			
			coordinates = ':'.join(line.split(':')[4:6])
			header = line
			

		# if it's not a header must be a sequence/+/quality
		else:
			# barcode is first 16 bp
			barcode = ''.join(line[0:16])

			# if it is a desired barcode, match it to read two
			if barcode in desired_barcodes:
				if line_indice in indices_list:
					read_one_dic[coordinates] = barcode 
				else:
					error_read_one_file.write(header)
					error_read_one_file.write(line)


		if not i % 2:
			consume(read_one_file, 2)

	error_read_one_file.close()
	read_one_file.close()

	return read_one_dic


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
				# example: barcode_dictionary[CATACAGAGCACTCGC] = neg4
				try:
					barcode_dictionary[row[1].rstrip()] = row[5]
				# repurposing to handle creating a dictionary from a plain text file
				except:
					barcode_dictionary[row[0].rstrip()] = 1

	return barcode_dictionary

# Creates target directories and opens fastq files for impending appending
def create_target_directory (output_directory, append):

	# Creates the directory for the sorted groups to go into
	try:
		os.makedirs(output_directory)
	# Will append groups 
	except:
		if append:
			pass
		else:
			try:
				os.system("rm -r {}".format(output_directory))
			except:
				pass


	return output_directory


# Creates a list given indices as input (assumes file is similar format to symlinks/Indices_A1.txt)
def create_indices_list (indices_file):
	indice_list = []
	file = open(indices_file)
	with file:
		for indice in file:
			indice_list.append(indice.rstrip())
	file.close()
	return indice_list

# Creates fastq files and prepares for appending
def create_fastq_files (dir_name, indices_list, barcode_matrix):

	unique_barcodes = set()
	files_to_close = set()

	for val in barcode_matrix.values():
		unique_barcodes.add(val)

	for group_name in unique_barcodes:
		try:
			os.makedirs("{}/{}".format(dir_name, group_name))
			for indice in indices_list:
				file = open("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, indice), "a")
				files_to_close.add(file)
		except:
			# Folders have already been made
			pass

	close_all_files (files_to_close)

# Closes all fastq files at the end 
def close_all_files (files_set):
	for file in files_set:
		file.close()
	pass

# Append to a dictionary to be read in by other python script
def write_out_dictionary_csv (table, dictionary_path):
	writer = csv.writer(open(dictionary_path, "a+"))
	for key, val in table.items():
		writer.writerow([key, val])


def write_to_log (start_time, log_path, message):
	log_file = open(log_path, "a+")
	log_file.write(str(datetime.datetime.now()))
	run_time = str(datetime.timedelta(seconds=time.time() - start_time))
	log_file.write("\nRuntime = {} h/m/s.\n".format(run_time))
	log_file.write(message +"\n")
	log_file.close()

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

# Count number of lines in file QUICKLY
def count_lines(filename):
	return int(subprocess.check_output(['wc', '-l', filename]).split()[0])

# ERROR CHECKING for cell_assign.py
def error_check (csv_matrix, read1, read2, indices):
	# (1): Exit if arguments not 4 (invalid)
	if len(sys.argv) != 5:
		print("\nInsufficient arguments entered. Input must have: barcode.csv, read1, read2 and indices.\nExiting...\n")
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