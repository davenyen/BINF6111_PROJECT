# Author:
# Function: This file will be like an autotest 

from functions import *

# Idea: Make smaller data sets and use them as inputs for this function
#       raise exceptions but do not end autotest
#       my inspo is 1511 autotest <3
# note: just made a skeleton for you bc i was bored 

# Input Error Checking
def input_check (csv_matrix, indices):
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

# Checks if tmp files created are removed at the end
def check_rm_temp ():
	correct = 0
	total_tests = 10
	print("{}/{} tests for check_rm_temp passed.\n".format(correct, total_tests))

# Checks if output files match corrrect_headers (last 2 functions from functions.py)
def check_correctness ():
	correct = 0
	total_tests = 10
	print("{}/{} tests for check_correctness passed.\n".format(correct, total_tests))

# Checks if there are 27 directories for a run
def check_directories () -> int:
	correct = 0
	total_tests = 10
	print("{}/{} tests for check_correctness passed.\n".format(correct, total_tests))
	return correct

def check_threading () -> int:
	""" Check if list of threads = number of threads, 
		returns number of passed tests
	"""
	correct = 0
	total_tests = 10
	print("{}/{} tests for check_threading passed.\n".format(correct, total_tests))
	return correct

# These functions will check correctness for each function in functions.py 
# @chelsea delete this if you want but imo this is good?

# Checks functions.py function1 (create_sorted_fastq)
def check_one ():
	pass

# Checks function2 (create_coordinates_barcode_dictionary)
def check_two ():
	""" Checks create_coorrdinates_barcode_dictioanry functionality """
	pass

def check_three ():
	pass

def check_four ():
	pass

def check_five ():
	pass

def check_six

if __name__ == '__main__':

	# Sample test datasets (propose 10K, 100K and 1M)?
	total_tests = 100 
	sum_results = 0

	# can log if you want idk
	print("{}/{} tests passed.\n".format(sum_results, total_tests))