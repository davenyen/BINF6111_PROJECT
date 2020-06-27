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

# Reads matrix csv and saves as a data structure (dictionary) for O(1) access time
def read_matrix (csv_matrix):
	barcode_dictionary = {}

	# Reads cell barcode matrix and saves only: barcode + target into dictionary
	with open(csv_matrix, 'r') as file:
	    reader = csv.reader(file)
	    skip_first = True
	    for row in reader:
	    	if skip_first == True:
	    		skip_first = False
	    		continue
    		else:
		        barcode_dictionary[row[1].rstrip()] = row[5]

	return barcode_dictionary

# Creates target/group directories
def create_target_directory (barcode_table):
	dir1 = 'sorted_target_groups'

	# Creates the directory for the sorted groups to go into
	try:
		os.makedirs(dir1)
	except:
		pass

	# Creates a folder for each target/group
	for group in barcode_table:
		iter_dir = ("{}/{}".format(dir1, barcode_table[group]))
		try:
			os.makedirs(iter_dir)
		except:
			pass

	pass

# Make a dictionary of read1 where {barcode: coordinate} (USED FOR CELL_ASSIGN.PY)
def coordinates_barcodes_dictionary (read1_file):

	read1_dictionary = {}
	coordinates = ''
	barcode = ''
	count = 0

	file = open(read1_file)

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
		
			count += 1
			if count == 5000:
				break
				
			# will skip lines 3 and 4 for performance
			if not i % 2:
				consume(file, 2)

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