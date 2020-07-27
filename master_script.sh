#!/bin/bash

# Author: Chelsea Liang
# Function: Parses reads (python) and launches alignments (bash)

#####
# This master script launches this pipeline, run with:
# nohup ./master_script.sh -w ${working_dir} -d ${data_path} -m ${matrix} -b ${desired_barcodes} -i ${indices} -r ${ref_genome} &
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
# working_dir=/Users/student/BINF6111_2020/test/full_run_A1

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
# working_dir=/Users/student/BINF6111_2020/test/team_b_stuff/test_folders/
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
# working_dir=/Users/student/BINF6111_2020/test/check_master_script


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

# benchmarking
SECONDS=0

# VARIABLES
threads=8 #calculate this from getopt (voluntary to change how many threads)
bigwig=true
delete_fastq=true

exist=true #just for testing purposes
log=${working_dir}/pipeline_log.txt

exist=True #just for testing purposes

identify_experiment_name=not_exist
file_regex='^(.+)_(L[0-9]{3})_([RI][12])_.+\.fastq(\.gz)?$'

while getopts "w:d:m:b:i:r:f" flag
do
  case $flag in
    f) delete_fastq=false;;
    w) working_dir=$OPTARG;;
    d) data_path=$OPTARG;;
    m) matrix=$OPTARG;;
    b) desired_barcodes=$OPTARG;;
    i) indices=$OPTARG;;
    r) ref_genome=$OPTARG;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done



# error handling inputs (LATER)
# translate groups into cell barcodes (LATER/optional)

echo "===========================================================" >> ${log}
echo [$(date)] "PID: $$" >> ${log}
echo "===========================================================" >> ${log}

# compulsory inputs exist / getopts handling


 echo [$(date)] "Completed error checking inputs" >> ${log}

	# if ${exist}; then echo [$(date)] "Already copied and uncompresseed fastqs" >> ${log}; break; fi

# translate groups into cell barcodes (LATER/optional)

 for fastq in ${data_path}/*
 	do
 	fastq=$(basename ${fastq})
	
 	# Steps are:
 		# 1) check which read file
 		# 2) uncompress file
 		# 3) process reads using python to open file, look for cell barcodes, write reads to new_files


 	#if ${exist}; then echo [$(date)] "Already copied and uncompresseed fastqs" >> ${log}; break; fi

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

# # prepare working_dir
 for fastq in ${working_dir}/*
 	do

	if [[ ${fastq} =~ "error" ]]
 		then
 		rm ${fastq}
 		echo [$(date)] "Delete ${fastq} for new run" >> ${log}
 	fi

 done


# # iterate through files in working_dir to launch parsing of each lane
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

 echo [$(date)] "Completed fastq groups for ${experiment_name}" >> ${log}

## ALIGN TO HUMAN GENOME
 #${ref_genome} ${working_dir}
./genome_align.sh "${working_dir}/SORTED_GROUPS/" ${ref_genome} ${indices}
echo [$(date)] "Completed all alignments " >> ${log}


## BAM TO BIGWIG CONVERSION
./bam_to_bigwig.sh "${working_dir}/SORTED_GROUPS/"
echo [$(date)] "Completed all bigwig conversions " >> ${log}

## DELETE FASTQ FILES

if $delete_fastq
then
	./delete_fastq.sh "${working_dir}"
fi

## TIDYING OUTPUT (output desired formats, clean temp files)

duration=${SECONDS}
echo "$((${duration} / 3600)) hours, $(((${duration} / 60) % 60)) minutes and $((${duration} % 60)) seconds elapsed" >> ${log}
echo [$(date)] "COMPLETED PIPELINE for: ${experiment_name}" >> ${log}
echo "===========================================================" >> ${log}