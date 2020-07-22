#!/bin/bash

# Author: Chelsea Liang
# Function: Parses reads (python) and launches alignments (bash)

#####
# This master script launches this pipeline, run with:
# nohup disowns the process so you can exit ssh session and still run in the background using the & symbol
# nohup ./master_script.sh ${working_dir} ${data_path} ${matrix} ${desired_barcodes} ${indices} ${ref_genome} &
#

# TODO
# getopts to handle argument flags 
# error handling for arguments 
#

# TEST CASES

# full run A1
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/full_run
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index


# full run A2
# make a new fastq so turn off those flags and allow transfer
# write thing to combine negs all into one folder
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A2
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A2.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA2.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A2.txt
# working_dir=/Users/student/BINF6111_2020/test/full_run_A2
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index



# sanity check master script
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/check_master_script
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index


# 100mil
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/100mil_test
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index


# 10 million
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/10mil_run
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index


# VARIABLES
working_dir=${1}
data_path=${2}
matrix=${3}
desired_barcodes=${4}
indices=${5}
ref_genome=${6}
threads=8 #calculate this from getopt (voluntary to change how many threads)
bigwig=true

exist=true #just for testing purposes
log=${working_dir}/pipeline_log.txt
identify_experiment_name=not_exist
file_regex='^(.+)_(L[0-9]{3})_([RI][12])_.+\.fastq(\.gz)?$'

# error handling inputs (LATER)
# translate groups into cell barcodes (LATER/optional)
# get files with the reads in them from directory
echo "===========================================================" >> ${log}
echo [$(date)] "PID: $$" >> ${log}
echo "===========================================================" >> ${log}

for fastq in ${data_path}/*
	do
	fastq=$(basename ${fastq})

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

	# grab name of experiment (everything before the lane number)
	if [[ ${identify_experiment_name} == 'not_exist' ]]
	then
		if [[ ${fastq} =~ ${file_regex} ]]
		then
			experiment_name=${BASH_REMATCH[1]}
		else
			echo [$(date)] "Error: Can't identify experiment name, will name experiment as 'sample_1'" >> ${log}
			experiment_name='sample_1'
		fi

		echo [$(date)] "Running pipeline on experiment: ${experiment_name}" >> ${log}
			identify_experiment_name=true
	fi

	if [[ ${fastq} =~ ${file_regex} ]] && [[ 'R1' == ${BASH_REMATCH[3]} ]] 
	then
		lane=${BASH_REMATCH[2]}
		if [[ ${lane} == "L001" ]]
			then
			append_status=0
		else 
			append_status=1
		fi

		python3 parse_lane.py ${fastq} ${matrix} ${desired_barcodes} ${indices} ${experiment_name} ${append_status} ${threads}

		echo [$(date)] "Completed lane: ${lane} " >> ${log}
	fi

done



## ALIGN TO HUMAN GENOME
 #${ref_genome} ${working_dir}
./genome_align.sh "${working_dir}/SORTED_GROUPS/" ${ref_genome} ${indices}
echo [$(date)] "Completed alignment " >> ${log}


#if 

## BAM TO BIGWIG CONVERSION
./bam_to_bigwig.sh "${working_dir}/SORTED_GROUPS/"
echo [$(date)] "Completed bigwig conversion " >> ${log}

## TIDYING OUTPUT (output desired formats, clean temp files)


echo [$(date)] "Completed pipeline for: ${experiment_name}" >> ${log}
echo "===========================================================" >> ${log}