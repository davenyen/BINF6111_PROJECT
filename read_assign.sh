#!/bin/bash

# /Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1/

# /Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A2/

# - Read in path of data directory, output directory, list of barcodes/group, matrix.csv
# - Decompress fastq files
# - Concatenate fastq reads to creating one fastq for read one and one for
# read two containing only reads with cell barcodes from the list
# - Only grab sequences


# test inputs
data_path = '/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1/'
matrix_path = '/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv'
list_path = '/Users/student/BINF6111_2020/test/test_list_barcodes.txt'
output_path = '/Users/student/BINF6111_2020/test/output'

# real inputs
data_path = 
matrix_path =
list_path = 
output_path = 


# error handling inputs