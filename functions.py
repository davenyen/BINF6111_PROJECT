# Author:
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
from itertools import islice
from Bio import SeqIO

############################################################################
################################ Classes ###################################
############################################################################

# Thread used for cell_assign for now
class myThread (threading.Thread):
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

	def run(self):
		create_sorted_fastq_file(self.read_two_file, self.barcode_matrix, self.r_one_coordinates_dict, self.dir_name, self.indices_list, self.file_dic)

############################################################################
################################ FUNCTIONS #################################
############################################################################

# Creates a fastq file with sequences that match read1 coordinates and are in sorted groups based on the target
def create_sorted_fastq_file (read_two_file, barcode_matrix, r_one_coordinates_dict, dir_name, indices_list, file_dic):
	""" Parameters:
			read_two_file          = the read2 file (R2)
			barcode_matrix         = the barcode_matrix created by read_csv
			r_one_coordinates_dict = the dictionary where {coordinate; barcode} made from R1
			dir_name               = the output directory
			indices_list           = list of indices that should exist
		Description: 
			Changed from previous version, now reads with BioPython and writes records each time
			whereas previous version wrote one line at a time. Theoretically should be faster.
			Also multithreading with one line writes per time, kind of can give a problem
			where you get random lines appending instead of the correct 4 lines each time.
			E.g. thread1 appends header to the same file while thread2 appends quality score to 
			the same file.
		Ideas:
	"""
	coordinates = ''
	files_to_close = set()

	# Experimental Biopython writing (need this for true asynchronous writing)
	seq_files = SeqIO.parse(read_two_file, "fastq")
	for record in seq_files:
		coordinates = ':'.join(record.name.split(':')[4:6])
		read_two_indice = record.description.split(':')[9].rstrip()
		# If R2 coordinate doesnt exist or R2 indice doesnt exist in the dictionary then skip for speed
		if coordinates not in r_one_coordinates_dict.keys() or read_two_indice not in indices_list:
			continue
		# Else record can be matched to read one and R2 indice exists
		elif coordinates in r_one_coordinates_dict.keys() and read_two_indice in indices_list:
			group_name = barcode_matrix[r_one_coordinates_dict[coordinates]]
			target_file = ("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, read_two_indice))
			file_dic[target_file].write("{}".format(record.format("fastq")))
			files_to_close.add(file_dic[target_file])
	pass
	
# Combines create_fastq_files and coordinates_barcodes_dictionary
def create_coordinates_barcodes_dictionary (read_one, barcode_matrix, desired_barcodes, indices_list):
	read_one_dic = {}
	#header = ''
	coordinates = ''
	read_one_file = open(read_one, 'r')
	#error_read_one_file = open(read_one + '.error' , 'a+')
	start_time = time.time()
	line_count = 0

	for i, line in enumerate(read_one_file, 1):

		# check line if it is header
		if line[0] == "@":
			line_indice = ''.join(line.split(':')[9]).rstrip()
			
			# faster if this happens so maybe we should have a flag to turn it on and off?
			if line_indice not in indices_list:
				consume(read_one_file, 3)
				line_count += 3
				#error_read_one_file.write(line)
				continue
			
			coordinates = ':'.join(line.split(':')[4:6])
			#header = line
			
		# if it's not a header must be a sequence/+/quality
		else:
			# barcode is first 16 bp
			barcode = ''.join(line[0:16])
			if barcode in barcode_matrix.keys():

			# if it is a desired barcode, match it to read two
			#if barcode in desired_barcodes.keys():
				#if line_indice in indices_list:
				#error_read_one_file.write(header)
				read_one_dic[coordinates] = barcode 
				#else:
					#error_read_one_file.write(header)
					#error_read_one_file.write(line)
			#else:
				#error_read_one_file.write(header)
				#pass

		if not i % 2:
			consume(read_one_file, 2)
			line_count += 2

	#error_read_one_file.close()
	read_one_file.close()

	log_path = "/Users/student/BINF6111_2020/test/100mil_test/pipeline_log.txt"
	message = []
	write_to_log (start_time, log_path, '\n'.join(message))

	return read_one_dic, line_count+i


# Creates target directories
def create_target_directory (output_directory, append):

	# Creates the directory for the sorted groups to go into
	try:
		os.makedirs(output_directory)
	# Will append groups 
	except:
		if append == True:
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

# Creates fastq files and passes a dictionary {filename: file_handle}
def create_fastq_files (dir_name, indices_list, barcode_matrix):
	"""
		Parameters:
		Description:
			Returns a dictionary which is passed to the threads so we dont
			exceed the file open limit and we truly achieve synchronised writing
	"""
	unique_barcodes = set()
	file_dictionary = {}

	for val in barcode_matrix.values():
		unique_barcodes.add(val)

	for group_name in unique_barcodes:
		try:
			os.makedirs("{}/{}".format(dir_name, group_name))
		except:
			# Folders have already been made
			pass
		finally:
			for indice in indices_list:
				file = open("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, indice), "a")
				file_dictionary[("{}/{}/{}_{}.fastq".format(dir_name, group_name, group_name, indice))] = file

	return file_dictionary
	#close_all_files (files_to_close)

# Creates and run N threads (remove file_dic if your thing broke)
def create_threads (split_files, barcode_matrix, r_one_coordinates_dict, dir_name, indices_list, file_dic):
	""" Parameters:
			split_files            = list of split files
			barcode_matrix         = dictionary of {barcode: target}
			r_one_coordinates_dict = dictionary of R1 {coord: barcode}
			dir_name 			   = directory of output path 
			indices_list           = list of indices 
		Description:
			Makes threads based on number of split files and starts them,
			Also joins them so we don't get premature output
	"""
	threads = []
	for i in range(0, len(split_files)):
		threads.append(i)
		threads[i] = myThread(("{}".format(i+1)), ("Thread {}".format(i+1)), split_files[i], barcode_matrix, r_one_coordinates_dict, dir_name, indices_list, file_dic)
		threads[i].start()
	for i in range(0, len(threads)):
		threads[i].join()
	pass

# Splits Read 2 file and returns list of split files (splits to current directory for now) 
def split_read_two (read_two_file, line_count, thread_numbers, shortcut):
	""" Parameters:
			read_two_file  = The R2 file
			line_count     = Number of lines from R1 as (R1 lines = R2 lines)
			thread_numbers = Number of files to be split into (num threads = num of split files)
			shortcut       = directory of already split files, only for testing, used to avoid running split 
		Description:
			Read 1 lines = Read 2 lines as they are paired reads 
			Probably delete the split directory(s) after in release, 
			for now just keep files so we save ~30 minutes splitting
	"""
	split_files = []

	# SHORTCUT 
	if shortcut:
		for item in os.listdir(shortcut):
			split_files.append("{}/{}".format(shortcut, item))
		return split_files
	else:
		lines_per_file = (line_count/thread_numbers)
		while lines_per_file%4 != 0:
			lines_per_file += 2
		
		# in current dir because this is deleted after 
		try:
			os.makedirs("tmp_split")
		except:
			pass

		os.system("split -l{} {} tmp_split/split_".format(int(lines_per_file), read_two_file))
		for split_file in os.listdir("tmp_split"):
			split_files.append("{}/{}".format("tmp_split", split_file))

	return split_files, "tmp_split"

# Reads matrix csv and returns a data structure (dictionary) for O(1) access time
def read_matrix (csv_matrix):
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
				# repurposing to handle creating a dictionary from a plain text file
				except:
					barcode_dictionary[row[0].rstrip()] = 1

	return barcode_dictionary

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