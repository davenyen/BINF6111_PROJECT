#!/bin/bash

#####
# This master script launches this pipeline, run with:
# ./master_script.sh ${data_path} ${list_path} ${matrix_path} ${output_path}
#

## PROCCESSING INPUT

# - Read in path of data directory, output directory, list of barcodes/group, matrix.csv
# - Decompress fastq files
# - Concatenate fastq reads to creating one fastq for read one and one for
# read two containing only reads with cell barcodes from the list
# - Only grab sequences


# test inputs
# data_path='/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1'
# list_path='/Users/student/BINF6111_2020/test/test_list_barcodes.txt'
# matrix_path='/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv'
# output_path='/Users/student/BINF6111_2020/test/output'

# set variables
data_path=${1}
matrix_path=${2}
list_path=${3}
output_path=${4}
verbose=true # fix this later, use getopts to parse variable options!


# error handling inputs (LATER)
echo ""
echo ""
echo ""
echo ""

# translate groups into cell barcodes (LATER/optional)




# get files with the reads in them from directory
en_regex='(.+)_L[0-9]{3}_*'
r1_regex='.+_R1_.+.fastq.gz$'
r2_regex='.+_R2_.+.fastq.gz$'
for fastq in ${data_path}/*
    do
    
    # grab name of experiment (everything before the lane number)
    if [[ ${fastq} =~ ${en_regex} ]]
    then
        experiment_name=$(basename ${BASH_REMATCH[1]})
    else
        echo "can't identify experiment name, will name experiment as 'sample_1'"
        experiment_name='sample_1'   
    fi


    # Steps are:
        # 1) check which read file
        # 2) decompress file
        # 3) process reads using python to open file, look for cell barcodes, write reads to new_files


    # check file is read 1
    if [[ ${fastq} =~ ${r1_regex} ]]
    then
        if ${verbose}; then echo "Reading $(basename ${fastq})"; fi
        
    # check file id read 2
    elif [[ ${fastq} =~ ${r2_regex} ]]
    then
        if ${verbose}; then echo "Reading $(basename ${fastq})"; fi

    # else don't care, go to the next file
    else  
        if ${verbose}; then echo "Not a read file"; fi
        continue
    fi

done

# print if verbose
if ${verbose}; then echo "Running pipeline on experiment: ${experiment_name}"; fi




## CELL ASSIGNMENT


## ALIGN TO HUMAN GENOME


## TIDYING OUTPUT (output desired formats, clean temp files)