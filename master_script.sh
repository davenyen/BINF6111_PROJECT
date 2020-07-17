#!/bin/bash

# Author: Chelsea Liang
# Function: Parses reads (python) and launches alignments (bash)

#####
# This master script launches this pipeline, run with:
# ./master_script.sh ${working_dir} ${data_path} ${matrix} ${desired_barcodes} ${indices} ${ref_genome}
#

# TODO
# getopts to handle argument flags 
# error handling for arguments 
# (OPTIONAL) ability to resume the pipeline halfway, so detect 
#	files in output folder already
#

# TEST CASES

# full run
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/test/test_list_barcodes.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/output

# sanity check test
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/test/check_master_script/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/check_master_script

# VARIABLES
working_dir=${1}
data_path=${2}
matrix=${3}
desired_barcodes=${4}
indices=${5}
ref_genome=${6}
log=${working_dir}/pipeline_log.txt

exist=true #just for testing purposes
identify_experiment_name=not_exist
file_regex='^(.+)_(L[0-9]{3})_([RI][12])_.+.fastq[.gz]?$'

# error handling inputs (LATER)
# translate groups into cell barcodes (LATER/optional)
# get files with the reads in them from directory


for fastq in ${data_path}/*
	do
	fastq=$(basename ${fastq})
	
	# grab name of experiment (everything before the lane number)
	if [[ ${identify_experiment_name} == 'not_exist' ]]
	then
		if [[ ${fastq} =~ ${file_regex} ]]
		then
			experiment_name=${BASH_REMATCH[1]}
			echo [$(date)] "Running pipeline on experiment: ${experiment_name}" >> ${log}
			identify_experiment_name=true

		else
			echo [$(date)] "Error: Can't identify experiment name, will name experiment as 'sample_1'" >> ${log}
			experiment_name='sample_1'
			echo [$(date)] "Running pipeline on experiment: ${experiment_name}" >> ${log}
			identify_experiment_name=true  
		fi
	fi

	# Steps are:
		# 1) check which read file
		# 2) uncompress file
		# 3) process reads using python to open file, look for cell barcodes, write reads to new_files


	if ${exist}; then echo [$(date)] "Already copied and uncompresseed fastqs" >> ${log}; break; fi

	# check file is a read file
	if [[ ${fastq} =~ ${file_regex} ]]
	then
		file=$(basename ${fastq} .gz)
		echo [$(date)] "Reading ${file}" >> ${log}
		
		# rsync it over, this way is safer in case fastq is huge
		rsync -avz ${fastq} ${working_dir}
		
		# uncompress file in place
		gunzip ${working_dir}/${file}.qz

		
	# else, go to the next file
	else  
		echo [$(date)] "${fastq} is not a fastq file" >> ${log}
		continue
	fi

done

# iterate through files in working_dir to launch parsing of each lane
for fastq in ${working_dir}/*
	do

	if [[ ${fastq} =~ ${file_regex} ]] && [[ 'R1' == ${BASH_REMATCH[3]} ]] 
	then
		lane=${BASH_REMATCH[2]}
		python3 parse_lane.py ${fastq} ${matrix} ${desired_barcodes} ${indices} ${experiment_name}

		echo [$(date)] "Completed lane: ${lane} " >> ${log}
	fi

done







## CELL ASSIGNMENT

# To do
# 1. Create loop and iterate through Reads (match read1 to read2)
# 2. Run cell_assign for each separate read1 + read2 matches 

#python3 cell_assign.py ${matrix} ${} ${}

# ${experiment_name}_${group_name}

## ALIGN TO HUMAN GENOME
 #${ref_genome} ${working_dir}

## TIDYING OUTPUT (output desired formats, clean temp files)

echo "===========================================================" >> ${log}
echo "" >> ${log}