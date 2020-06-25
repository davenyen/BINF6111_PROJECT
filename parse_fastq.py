import sys
from itertools import islice
import collections
import os
import time
from progress.bar import IncrementalBar

# run cases
# output_path=/Users/student/BINF6111_2020/test/output
# file=testR1_1.fastq
# list_path='/Users/student/BINF6111_2020/test/test_list_barcodes.txt'
# experiment_name=PilotCROP_C_1_S1
# read=R1
# python3 parse_fastq.py ${output_path}/${file} ${list_path} ${experiment_name} ${read}


# This script will open a file and go through every fourth line
# for loop of every desired cell barcode
# if match
    # write to new file
    # else next


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


# For performance put list of cell barcodes in dictionary

barcodes = {}
with open(sys.argv[2]) as barcode_list:
    for barcode in barcode_list:
        barcodes[barcode.rstrip()] = 1 # just a random number, will replace with the


fastq_to_append = os.path.dirname(sys.argv[1]) + '/' + sys.argv[3] + '_' + sys.argv[4] + '.fastq'
fastq_to_append = open(fastq_to_append, "a")

file = open(sys.argv[1])

with file:
    for i, line in enumerate(file, 1):
        
        # check line if it is header, save to maybe print later
        if line[0] == "@":
            seq_code = line.split(':')[-1]
            header = line

        # if it's not a header must be a sequence
        else:
            # barcode is first 16 bp
            barcode = ''.join(line[0:16])

            # check if barcode exists in dictionary
            try:
                # print("hi")
                check = barcodes[barcode]
                barcodes[barcode] = seq_code
                fastq_to_append.write(header)
                fastq_to_append.write(line)
            
            # else, isn't a target barcode
            except:
                pass
            
        # will skip lines 3 and 4 for performance

        if not i % 2:
            consume(file, 2)