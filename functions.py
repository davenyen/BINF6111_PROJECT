# Author: TeamA
# Function: Holds functions for parse_lane.py
# Version: 1.8

import os
import re
import sys
import time
import csv
import datetime
import threading
import subprocess
import collections
import typing
from itertools import islice

############################################################################
################################ Classes ###################################
############################################################################

class myThread (threading.Thread):
	""" Threading Class."""
	def __init__(self, threadID, name, read_two_file, barcode_matrix, r_one_coordinates_dict, dir_name, indices_list, file_dic):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.read_two_file = read_two_file
		self.barcode_matrix = barcode_matrix
		self.r_one_coordinates_dict = r_one_coordinates_dict
		self.dir_name = dir_name
		self.indices_list = indices_list
		self.file_dic = file_dic

	""" Thread starts, each thread runs create_sorted_fastq with a split file. """
	def run(self):
		create_sorted_fastq_file(self.read_two_file, self.barcode_matrix, self.r_one_coordinates_dict, self.dir_name, self.indices_list, self.file_dic)

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Creates a fastq file with sequences that match read1 coordinates and are in sorted groups based on the target
def create_sorted_fastq_file (read_two_file: str, barcode_matrix: dict, r_one_coordinates_dict: dict, dir_name: str, indices_list: list, file_dic: dict):
	""" Parameters:
			read_two_file          = the read2 file (R2)
			barcode_matrix         = the barcode_matrix created by read_csv
			r_one_coordinates_dict = the dictionary where {coordinate; barcode} made from R1
			dir_name               = the output directory
			indices_list           = list of indices that should exist
		Attributes:
			file                   = The handle for read_two_file
			new_header             = Determines if each 4 lines is a new record or not
		Description: 
			Creates fastq files for each 4 indices per group, based on whether 
			they match to R1 or not.
	"""
	file = open(read_two_file)
	new_header = True

	for line in file:
		# If the line is not a header
		if line[0] != "@":
			# if new_header is false then it is the 2 other lines != header/sequence
			if new_header == False:
				if line.rstrip() == "+":
					plus = line
				else:
					quality = line
					file_dic[target_file].write("{}{}{}{}".format(header,sequence,plus,quality))
			else:
				# Sequence argument, writes to file in the file_dictionary
				group_name = barcode_matrix[r_one_coordinates_dict[coordinates]]
				if group_name[0:3] == "neg":
					group_name = group_name[0:3]
				target_file = ("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, read_two_indice))
				sequence = line
				new_header = False
		else:
			header = line
			coordinates = (':'.join(line.split(':')[4:7])).split(' ')[0:1][0]
			read_two_indice = line.split(':')[9].rstrip()
			plus = ''
			quality = ''
			# If R2 coordinates or R2 indice does not exist then skip for performance
			if coordinates not in r_one_coordinates_dict.keys() or read_two_indice not in indices_list:
				consume(file, 3)
			elif coordinates in r_one_coordinates_dict.keys() and read_two_indice in indices_list:
				new_header = True

	file.close()
	
# Combines create_fastq_files and coordinates_barcodes_dictionary
def create_coordinates_barcodes_dictionary (read_one: str, barcode_matrix: dict, desired_barcodes, indices_list: list) -> (dict, int):
	"""
		Parameters:
			read_one         = the R1 file
			barcode_matrix   = cell barcode matrix {barcode: target/group}
			desired_barcodes = barcodes that we want (not sure if we're given this chels)
			indices_list     = list of indices that we want
		Attributes:
			read_one_dic     = dictionary to be returned where {r1coords: barcode}
			line_count       = number of lines in R1 used for threading function
			read_one_file    = open read-one files 
		Description:
		Important:
	"""
	read_one_dic = {}
	line_count = 0
	read_one_file = open(read_one, 'r')
	error_read_one_file = open(read_one + '.error', 'a')

	for i, line in enumerate(read_one_file, 1):
		# check line if it is header
		if line[0] == "@":
			line_indice = ''.join(line.split(':')[9]).rstrip()
			# If the record indice doesn't exist then skips for performance
			if line_indice not in indices_list:
				consume(read_one_file, 3)
				line_count += 3
				error_read_one_file.write(line.rstrip() + ':UNKNOWN_INDICE\n')
				continue
			coordinates = (':'.join(line.split(':')[4:7])).split(' ')[0:1][0]
			header = line
		# if it's not a header must be a sequence/+/quality
		else:
			barcode = ''.join(line[0:16])
			if barcode in barcode_matrix.keys() and barcode in desired_barcodes.keys():
			# if it is a desired barcode, match it to read two
				#if barcode in desired_barcodes.keys():
				read_one_dic[coordinates] = barcode 
				#error_read_one_file.write(header.rstrip() + ':CORRECT_BARCODE\n')
			else:
				error_read_one_file.write(header.rstrip() + ':UNKNOWN_BARCODE\n')

		if not i % 2:
			consume(read_one_file, 2)
			line_count += 2

	error_read_one_file.close()
	read_one_file.close()

	return read_one_dic, line_count+i

# Creates target directories (Can remove return value)
def create_target_directory (output_directory: str, append: bool):
	"""
		Parameters:
			output_directory = The directory for program output
			append           = Bool value, true/false
		Attributes:
			log_path         = Path to the log file
		Description:
			Creates the working directory if it does not exist, otherwise
			it can append or rewrite it.
	"""
	log_path = '/'.join(output_directory.split('/')[0:6]) + "/pipeline_log.txt"
	# Creates the directory for the sorted groups to go into
	try:
		os.makedirs(output_directory)
	# Will append groups if append = True else removes prexisting directory 
	except:
		if append == True:
			write_to_log (time.time(), log_path, "Appended existing SORTED_GROUPS")
		else:
			try:
				os.system("rm -r {}".format(output_directory))
				os.makedirs(output_directory)
				write_to_log (time.time(), log_path, "Deleted existing SORTED_GROUPS")
			except:
				pass

# Creates a list given indices as input (assumes file is similar format to symlinks/Indices_A1.txt)
def create_indices_list (indices_file: str) -> list:
	"""Creates and returns a list given indices in a file."""
	indice_list = []
	file = open(indices_file)
	with file:
		# Appends each indice into a list
		for indice in file:
			indice_list.append(indice.rstrip())
	file.close()
	return indice_list

# Creates fastq files and passes a dictionary {filename: file_handle}
def create_fastq_files (dir_name: str, indices_list: list, barcode_matrix: dict) -> dict:
	"""
		Parameters:
			dir_name       = directory name
			indices_list   = list of indices (library barcode)
			barcode_matrix = matrix of {barcode: target}
		Attributes:
			unique_groups   = Set of unique groups used to create fastq files
			file_dictionary = Dictionary of {filename: file_handle} for performance
		Description:
			Returns a dictionary which is passed to the threads so we dont
			exceed the file open limit and achieve synchronised writing
	"""
	unique_groups = set()
	file_dictionary = {}

	# Appends unique group/target names to unique_groups set
	for val in barcode_matrix.values():
		unique_groups.add(val)

	for group_name in unique_groups:
		try:
			if group_name[0:3] == "neg":
				group_name = group_name[0:3]
			os.makedirs("{}/{}".format(dir_name, group_name))
		except:
			pass
		finally:
			for indice in indices_list:
				file = open("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, indice), "a")
				file_dictionary[("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, indice))] = file

	return file_dictionary

# Creates and run N threads (remove file_dic if your thing broke)
def create_threads (split_files: list, barcode_matrix: dict, r1_barcode_dict: dict, dir_name: str, indices_list: list, file_dic: dict):
	""" Parameters:
			split_files         = list of split files
			barcode_matrix      = dictionary of {barcode: target}
			r1_barcode_dict     = dictionary of R1 {coord: barcode}
			dir_name 		    = directory of output path 
			indices_list        = list of indices 
		Attributes:
			threads = List of threads that will be made and running
		Description:
			Makes threads based on number of split files and starts them,
			also joins them so we don not get premature output from the main
			function.
	"""
	threads = []
	# For the number of split files there are, create and run a thread
	for i in range(0, len(split_files)):
		threads.append(i)
		threads[i] = myThread(("{}".format(i+1)), ("Thread {}".format(i+1)), split_files[i], barcode_matrix, r1_barcode_dict, dir_name, indices_list, file_dic)
		threads[i].start()
	# Joins threads to prevent premature output from main program
	for i in range(0, len(threads)):
		threads[i].join()

# Splits Read 2 file and returns list of split files (splits to current directory for now) 
def split_read_two (read_two_file: str, line_count: int, thread_numbers: int) -> (list, str):
	""" Parameters:
			read_two_file  = The R2 file
			line_count     = Number of lines from R1 as (R1 lines = R2 lines)
			thread_numbers = Number of files to be split into (num threads = num of split files)
		Attributes:
			split_files    = list of split files
		Description:
			Used for splitting R2 into thread_numbers, which will return
			a list of split_files. This is then used for multi-threading
			which will significantly speed up the program.
	"""
	split_files = []
	split_dir = "/".join(read_two_file.split("/")[0:-1]) + "/_temp"
	print(split_dir)
	# Calculates the number of lines for each file (fastq is 4 lines per rercord)
	lines_per_file = (line_count/thread_numbers)
	while lines_per_file%4 != 0:
		lines_per_file += 2
	# makes temporary split directory
	os.makedirs("{}".format(split_dir))
	# System command to split into {thread_numbers} files
	os.system("split -l{} {} {}/split_".format(int(lines_per_file), read_two_file, split_dir))
	# Saves each split_file into a list for use in threading
	for split_file in os.listdir(split_dir):
		split_files.append("{}/{}".format(split_dir, split_file))

	return split_files, split_dir

# Reads matrix csv and returns a data structure (dictionary) for O(1) access time
def read_matrix (csv_matrix: str) -> dict:
	"""
		Parameters: 
			csv_matrix = The matrix file to be converted
		Attributes:
			barcode_dictionary = output dictionary where {barcode: target/group}
		Description:
			Reads in a csv matrix and converts it into a dictionary for access
			performance.
	"""
	barcode_dictionary = {}

	# Reads cell barcode matrix and saves only: barcode + target into dictionary
	with open(csv_matrix, 'r') as file:
		reader = csv.reader(file)
		skip_first = True
		for row in reader:
			# Skips first row because there is no data in the first row (only for csv files)
			if skip_first == True and csv_matrix[-4:] == ".csv": 
				skip_first = False
				continue
			else:
				# example: barcode_dictionary[CATACAGAGCACTCGC] = neg4
				try:
					barcode_dictionary[row[1].rstrip()] = row[5]
				# If excepted, then means it's not a csv file
				except:
					barcode_dictionary[row[0].rstrip()] = 1

	return barcode_dictionary

# Closes all open fastq files given a file set
def close_all_files (files_set: set):
	"""Closes all open files in the given set."""
	for file in files_set:
		file.close()

# Append to a dictionary to be read in by other python script (UNUSED)
def write_out_dictionary_csv (table: dict, dictionary_path: str):
	writer = csv.writer(open(dictionary_path, "a+"))
	for key, val in table.items():
		writer.writerow([key, val])

# Writes to a log file
def write_to_log (start_time, log_path, message):
	log_file = open(log_path, "a+")
	log_file.write(str(datetime.datetime.now()))
	run_time = str(datetime.timedelta(seconds=time.time() - start_time))
	log_file.write("\nRuntime = {} h/m/s.\n".format(run_time))
	log_file.write(message +"\n")
	log_file.write("---------------------------------------------\n")
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

# ERROR TESTING FUNCTIONS
def create_correct_list (correct_file: str) -> list:
	"""Creates and returns a list given indices in a file."""
	correct_headers = []
	file = open(correct_file)
	with file:
		# Appends each indice into a list
		for indice in file:
			# testing, appending coordinates only, delete after
			correct_headers.append((':'.join(indice.split(':')[4:7])).split(' ')[0:1][0])
	file.close()
	return correct_headers

# Loops through directories and compares file to error/correct files
def check_correctness (directory: str, correct_file: list) -> bool:
	"""
		Parameters:
		Attributes:
		Description:
			Super inefficient test O(n^3)? i think xD 
	"""
	success = True
	line_count = 0
	# For each directory in group folder
	for item in os.listdir(directory):
		# For each file in the directory that is fastq
		for fastq in os.listdir("{}/{}".format(directory, item)):
			if fastq[-5:] == "fastq":
				tmp = open(("{}/{}/{}".format(directory, item, fastq)), 'r')
				# Loop through each file matching coordinates to correct_headers list
				for i, line in enumerate(tmp, 1):
					# check headers against correct-file headers
					if line[0] == "@":
						coordinates = (':'.join(line.split(':')[4:7])).split(' ')[0:1][0]
						if coordinates.rstrip() not in correct_file:
							success = False
							return success, line_count
					consume(tmp, 3)
					line_count += 3
				line_count += i
	return success, line_count