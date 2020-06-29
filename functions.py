############################################################################
################################ FUNCTIONS #################################
############################################################################

import sys
import collections
import os
import time
import csv
from itertools import islice

############################################################################
################################# DAVID'S ##################################
############################################################################

# Progress bar stolen from stack overflow
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = ' ', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# Creates a fastq file with sequences that match read1 coordinates and are in sorted groups based on the target
# PS REMOVE COUNT IN FINAL VERSION, only using now to limit output because output takes too long
def create_sorted_fastq_file (read_two_file, barcode_matrix, read1_coordinates_barcodes, dir_name):
	file = open(read_two_file)
	count = 0

	num_lines = sum(1 for line in open(file))
	printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
	with file:
		for i, line in enumerate(file, 1):
			# check line if it is header, save to write
			if line[0] == "@":
				header = line
				coordinates = ':'.join(line.split(':')[4:6])
				new_header = True
			# if it's not a header must be a sequence/quality/+  
			# if the coordinate exists in read1, then it will proceed to write the other 2 lines to the file.
			else:
				if new_header == False:
					target_file = ("{}/{}/{}.fastq".format(dir_name, barcode_matrix[read1_coordinates_barcodes[coordinates]], barcode_matrix[read1_coordinates_barcodes[coordinates]]))
					f = open(target_file, "a")
					f.write("{}".format(line))
					f.close()
				else:
					sequence = line
					# GET TARGET/GROUP then write a fastq file with read2 data into group/directory
					if coordinates in read1_coordinates_barcodes:
						if read1_coordinates_barcodes[coordinates] in barcode_matrix.keys():
							if os.path.isfile("{}/{}/{}.fastq".format(dir_name, barcode_matrix[read1_coordinates_barcodes[coordinates]], barcode_matrix[read1_coordinates_barcodes[coordinates]])) == False:
								target_file = ("{}/{}/{}.fastq".format(dir_name, barcode_matrix[read1_coordinates_barcodes[coordinates]], barcode_matrix[read1_coordinates_barcodes[coordinates]]))
								f = open(target_file, "w")
								f.write("{}{}".format(header, sequence))
								f.close()
							else:
								target_file = ("{}/{}/{}.fastq".format(dir_name, barcode_matrix[read1_coordinates_barcodes[coordinates]], barcode_matrix[read1_coordinates_barcodes[coordinates]]))
								f = open(target_file, "a")
								f.write("{}{}".format(header, sequence))
								f.close()

							new_header = False

			printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
			count += 1
			if count == 10000:
				break
	pass

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
	dir1 = ("{}SORTED_GROUPS".format(read_two[0]))

	# Creates the directory for the sorted groups to go into
	try:
		os.makedirs(dir1)
	except: #If excepts then directory already exists 
		#uncomment this if you don't want to append
		#comment this if you want to append to a directory with the same name
		os.system("rm -r {}".format(dir1))
		pass
	
	# Creates a folder for each target/group
	for group in barcode_table:
		iter_dir = ("{}/{}".format(dir1, barcode_table[group]))
		try:
			os.makedirs(iter_dir)
		except:
			pass

	return dir1

# Make a dictionary of read1 where {barcode: coordinate} (USED FOR CELL_ASSIGN.PY)
# REMOVE COUNT IN FINAL VERSION
def coordinates_barcodes_dictionary (read1_file):

	read1_dictionary = {}
	file = open(read1_file)
	count = 0

	# Goes through read1 and saves barcode + coordinate into a dictionary for O(1)
	with file:
		for i, line in enumerate(file, 1):
			
			# check line if it is header, save to maybe print later
			if line[0] == "@":
				coordinates = ':'.join(line.split(':')[4:6])

			# if it's not a header must be a sequence
			else:
				# barcode is first 16 bp
				barcode = ''.join(line[0:16])
				read1_dictionary[coordinates] = barcode
				
			# will skip lines 3 and 4 for performance
			if not i % 2:
				consume(file, 2)

			count += 1
			if count == 10000:
				break

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