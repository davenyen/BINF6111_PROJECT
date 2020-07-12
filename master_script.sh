#!/bin/bash

#####
# This master script launches this pipeline, run with:
# ./master_script.sh ${data_path} ${list_path} ${matrix_path} ${output_path}
#

# TODO
# getopts to handle argument flags 
# error handling for arguments 
# (OPTIONAL) ability to resume the pipeline halfway, so detect 
#	files in output folder already
#

## PROCCESSING INPUT

# test inputs
# data_path='/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1'
# matrix_path='/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv'
# list_path='/Users/student/BINF6111_2020/test/test_list_barcodes.txt'
# output_path='/Users/student/BINF6111_2020/test/output'

# data_path='/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1'
# matrix_path='/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv'
# list_path='/Users/student/BINF6111_2020/test/check_master_script/barcodesA1.csv'
# output_path='/Users/student/BINF6111_2020/test/check_master_script'

# VARIABLES
data_path=${1}
matrix_path=${2}
list_path=${3}
output_path=${4}
ref_genome=${5}
log=${output_path}/log.txt
verbose=true # fix this later, use getopts to parse variable options!
not_exist=false #just for testing purposes



# error handling inputs (LATER)

# translate groups into cell barcodes (LATER/optional)




# get files with the reads in them from directory
en_regex='(.+)_L[0-9]{3}_.+'
read_regex='.+_(L[0-9]{3})_(R[12])_.+.fastq.gz$'

# # test
# en_regex='(test)_.+_L[0-9]{3}_.+'
# read_regex='test_.+_(R[12])_.+.fastq$'
for fastq in ${data_path}/*
	do
	
	# grab name of experiment (everything before the lane number)
	if [[ ${fastq} =~ ${en_regex} ]]
	then
		experiment_name=$(basename ${BASH_REMATCH[1]})
	else
		echo "can't identify experiment name, will name experiment as 'sample_1'" >> ${log}
		experiment_name='sample_1'   
	fi

	# Steps are:
		# 1) check which read file
		# 2) decompress file
		# 3) process reads using python to open file, look for cell barcodes, write reads to new_files

	# check file is a read file
	if [[ ${fastq} =~ ${read_regex} ]]
	then
		file=$(basename ${fastq} .gz)
		if ${verbose}; then echo "Reading ${file}" >> ${log}; fi

		if ${not_exist}
		then
			# rsync it over, this way is safer in case fastq is huge
			rsync -avz ${fastq} ${output_path}
			
			# uncompress file in place
			gunzip ${output_path}/${file}.qz
		fi

		# process read 1 file for the cell barcodes
		if [[ 'R1' == ${BASH_REMATCH[2]} ]] 
		then
			experiment_name='test'
			python3 parse_read_one.py ${output_path}/*${BASH_REMATCH[1]}_R1*.fastq \
			${list_path} ${experiment_name}
		fi

		# delete full fastq after we are done with testing phase

		
	# else, go to the next file
	else  
		if ${verbose}; then echo "Not a read file" >> ${log}; fi
		continue
	fi

done

# print if verbose
if ${verbose}; then echo "Running pipeline on experiment: ${experiment_name}" >> ${log}; fi




## CELL ASSIGNMENT

# To do
# 1. Create loop and iterate through Reads (match read1 to read2)
# 2. Run cell_assign for each separate read1 + read2 matches 

#python3 cell_assign.py ${matrix_path} ${} ${}

# ${experiment_name}_${group_name}

## ALIGN TO HUMAN GENOME
 #${ref_genome} ${output_path}

## TIDYING OUTPUT (output desired formats, clean temp files)

echo "===========================================================" >> ${log}
echo "" >> ${log}