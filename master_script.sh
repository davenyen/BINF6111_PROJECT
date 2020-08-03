#!/bin/bash

# Author: Chelsea Liang
# Function: Parses reads (python) and launches alignments (bash)

#####
# This master script launches this pipeline
	# nohup and & at the end will run this script in a background process
	# you may exit the shell when following is printed to the terminal:
	# "Completed error checking inputs, pipeline will complete in background"
# run with:
# set variables in terminal, see test cases below
# mkdir -p ${working_dir}
# ./master_script.sh -w ${working_dir} -d ${data_path} -m ${matrix} \
# -b ${desired_barcodes} -i ${indices} -r ${ref_genome} -l ${log} -ge &
# disown -h %1



# TEST CASES

# full run A1 
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/full_run_A1
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
# log=${working_dir}/pipeline_log.txt

# full run A1 groups 
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/group_names_A1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# working_dir=/Users/student/BINF6111_2020/test/full_run_A1_groups
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
# log=${working_dir}/pipeline_log.txt

# full run A2
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A2
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A2.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA2.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A2.txt
# working_dir=/Users/student/BINF6111_2020/test/full_run_A2
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
# log=${working_dir}/pipeline_log.txt


# sanity check master script
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
# working_dir=/Users/student/BINF6111_2020/test/check_master_script
# log=${working_dir}/pipeline_log.txt

# test groups flag
# data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
# matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
# desired_barcodes=/Users/student/BINF6111_2020/test/groups_10mil_run/some_groups_A1.txt
# indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
# ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
# working_dir=/Users/student/BINF6111_2020/test/groups_10mil_run
# log=${working_dir}/pipeline_log.txt


## BENCHMARKING AND LOGS
SECONDS=0					# records time taken by whole pipeline
time=$(date +"%m-%d-%Y-%T")
	

# DO NOT CHANGE THE ORDER OF VARIABLE DECLARATION PLEASE
# Default variables (if user chooses not to specify)
threads=8 
delete_fastq=true
output="bigwig"
exist=false
groups=false

while getopts "w:d:m:b:i:r:fego:t:l:" flag
do
  case $flag in
    w) working_dir=$OPTARG;;
    d) data_path=$OPTARG;;
    m) matrix=$OPTARG;;
    b) desired_barcodes=$OPTARG;;
    i) indices=$OPTARG;;
    r) ref_genome=$OPTARG;;
	f) delete_fastq=false;;
	e) exist=true;;
	g) groups=true;;
	o) output=$OPTARG;;
	t) threads=$OPTARG;;
	l) log=$OPTARG;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done

# To name files and paths
identify_experiment_name=not_exist
file_regex='^(.+)_(L[0-9]{3})_([RI][12])_.+\.fastq(\.gz)?$'
exec 3>&1 1>>${log} 2>&1 	# handles printing of messages to log and terminal


# echo "===========================================================" >> ${log}
# echo [$(date)] "PID: $$" >> ${log}
# echo "===========================================================" >> ${log}
# echo "" 1>&3

# ## ERROR HANDLING INPUTS
# if test $output != "bam" -a $output != "bigwig" -a $output != "bambw"
# then
# 	echo "Invalid output specification, please use bam, bigwig or bambw as a parameter for the flag -o." 1>&3
# 	exit 1
# fi


# echo [$(date)] "Completed error checking inputs, pipeline will complete in background" 1>&3



# ## TRANSFER AND DECOMPRESS FASTQS
#  for fastq in ${data_path}/*
#  	do
	
#  	if ${exist}; then echo [$(date)] "Already copied and uncompresseed fastqs" >> ${log}; break; fi

#  	# check file is a read file
#  	if [[ ${fastq} =~ ${file_regex} ]] && [[ ${BASH_REMATCH[3]} =~ 'R' ]]
#  	then
#  		file=$(basename ${fastq} .gz)
#  		echo [$(date)] "Reading ${file}" >> ${log}
		
# 		# rsync it over, this way is safer in case fastq is huge
#  		rsync -avz ${fastq} ${working_dir}
		
#  		# uncompress file in place
#  		gunzip ${working_dir}/${file}

		
#  	# else, go to the next file
#  	else  
#  		echo [$(date)] "${fastq} is not a fastq file" >> ${log}
#  		continue
#  	fi

#  done

# # # prepare working_dir
#  for fastq in ${working_dir}/*
#  	do

# 	if [[ ${fastq} =~ "error" ]]
#  	then
#  		rm ${fastq}
#  	fi
#  done

#  rm -fr ${working_dir}/SORTED_GROUPS/
#  echo [$(date)] "Cleaned directory for new run" >> ${log}

# # # iterate through files in working_dir to launch parsing of each lane
#  for fastq in ${working_dir}/*
#  	do

#  	# grab name of experiment (everything before the lane number)
#  	if [[ ${identify_experiment_name} == 'not_exist' ]]
#  	then
#  		if [[ ${fastq} =~ ${file_regex} ]]
#  		then
#  			experiment_name=${BASH_REMATCH[1]}
# 		else
#  			echo [$(date)] "Error: Can't identify experiment name, will name experiment as 'sample_1'" >> ${log}
#  			experiment_name='sample_1'
#  		fi

#  		echo [$(date)] "Running pipeline on experiment: ${experiment_name}" >> ${log}
#  			identify_experiment_name=true
#  	fi

#  	if [[ ${fastq} =~ ${file_regex} ]] && [[ 'R1' == ${BASH_REMATCH[3]} ]] 
#  	then
#  		lane=${BASH_REMATCH[2]}
#  		if [[ ${lane} == "L001" ]]
#  			then
#  			append_status=false
#  		else 
#  			append_status=true
#  		fi

#  		python3 parse_lane.py ${fastq} ${matrix} ${desired_barcodes} ${groups} ${indices} ${experiment_name} ${append_status} ${threads}

# 		if [[ $? -eq 0 ]]
# 		then
# 			echo [$(date)] "Completed lane: ${lane} " >> ${log}
# 		else
# 			echo [$(date)] "${lane} failed to run correctly, see traceback" >> ${log}
# 			exit 1
# 		fi
#  	fi

#  done

 echo [$(date)] "Completed fastq groups for ${experiment_name}" >> ${log}

## ALIGN TO HUMAN GENOME
./genome_align.sh ${working_dir} ${ref_genome} ${indices}
echo [$(date)] "Completed all alignments " >> ${log}

## BAM TO BIGWIG CONVERSION
if test $output = "bigwig" -o $output = "bambw" 
then
	./bam_to_bigwig.sh ${working_dir}
	echo [$(date)] "Completed all bigwig conversions " >> ${log}
fi

echo [$(date)] "Completed FASTQ files in each target cell directory " >> ${log}


## DELETE AND TIDY FILES
if test $output = "bigwig" 
then
	file_extensions+=('.bam')
	file_extensions+=('.bai')	
elif test $output = "bam" 
then
	file_extensions+=('.bw')
fi
if ${delete_fastq}
then
	file_extensions+=('.fastq')
fi
echo ${file_extensions[@]}
./tidy_files.sh ${file_extensions[@]} "${working_dir}/SORTED_GROUPS"
echo [$(date)] "Finished tidying up outputs" >> ${log}



## TIDYING OUTPUT (output desired formats, clean temp files)

duration=${SECONDS}
echo "$((${duration} / 3600)) hours, $(((${duration} / 60) % 60)) minutes and $((${duration} % 60)) seconds elapsed" >> ${log}
echo [$(date)] "COMPLETED PIPELINE for: ${experiment_name}" >> ${log}
echo "===========================================================" >> ${log}