#!/bin/bash

# Author: Chelsea Liang
# Function: Parses reads (python) and launches alignment (bash)

# This master script launches this pipeline
	# you may exit the shell when following is printed to the terminal:
	# "Completed error checking inputs, pipeline will complete in background"
# run with:
# mkdir -p ${working_dir}
# ./master_script.sh -w ${working_dir} -d ${data_path} -m ${matrix} \
# -b ${desired_barcodes} -i ${indices} -r ${ref_genome} -e &
# disown -h %1

## LOGS AND ERRORS
SECONDS=0					# records time taken by whole pipeline
set -e						# if any error occurs, exit 1

# Default variables (if user chooses not to specify)
threads=8 
delete_fastq=true
output="bigwig"
exist=false
groups=0

## PROGRAM PATHS -- PLEASE CHANGE THESE PATHS TO THE ACTUAL PROGRAM PATHS ON YOUR SYSTEM
STAR_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/STAR-2.5.2b/bin/MacOSX_x86_64/STAR"
BAMCOVERAGE_RUN="/Users/rna/anaconda2/bin/bamCoverage" # deepTools bamCoverage
SAMTOOLS_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools"

## CHECK README.md FILE EXISTS IN THE CURRENT WORKING DIRECTORY
if test ! -f README.md
then
	echo "You have removed the README file for this program. Please move it into the same directory as this script before running it." 1>&3
	exit 1
fi

# getopts specifies what the different flags of the script are
# flags can be passed into commandline in any order and flags
# that have an associated parameter value have a : after them
# in the string below
while getopts "w:d:m:b:i:r:fego:t:h" flag
do
  case $flag in
    w) working_dir=$OPTARG;; # specifies the path of the working/output directories of script
    d) data_path=$OPTARG;; # specifies the path to the input data
    m) matrix=$OPTARG;; # the barcode correspondence matrix CSV file
    b) desired_barcodes=$OPTARG;; # the list of barcodes text file
    i) indices=$OPTARG;; # list of sample indices / library barcodes text file
    r) ref_genome=$OPTARG;; # specifies the path to the reference genome directory
	f) delete_fastq=false;; # option to keep intermediate fastq files at end of run
	e) exist=true;; # specifies whether fastq files already exist in working directory
	g) groups=1;; # specifies whether a desired list of cell groups is provided
	o) output=$OPTARG;; # specifies the output type of the script
	t) threads=$OPTARG;; # the number of threads to be run for script
	h) tail -n46 README.md
		exit 1;;
	?) echo "? option: -$OPTARG" >&2 
		exit 1;;
  esac
done

## ERROR HANDLING INPUTS

# Check valid output option value has been inputted
if [[ "$output" != "bam" && "$output" != "bigwig" && "$output" != "bambw" ]] 
then
	echo "Invalid output specification, please use bam, bigwig or bambw as a parameter for the flag -o."
	echo "Run ./master_script.sh -h to see the possible input options for -o."
	exit 1
fi

# Check all required parameters have been inputted
if [[ ! ("$working_dir" && "$data_path" && "$matrix" && "$desired_barcodes" && "$indices" && "$ref_genome") ]]
then
	echo "One of the required parameters has not been inputted."
	echo "usage: ./master_script.sh -w working_dir -d data_path -m matrix -b desired_barcodes -i indices -r ref_genome [-o output_format] [-f] [-e] [-g] [-t]" 
	exit 1
fi

# Check all the files/paths exist
if [[ (! -e "$working_dir") || (! -e "$data_path") || (! -e "$matrix") || (! -e "$desired_barcodes") || (! -e "$indices") || (! -e "$ref_genome") ]] 
then
	echo "One of the inputted paths or files is incorrect, please check that all inputted paths and files exist." 
	exit 1
fi

# Check all program paths exist
if [[ (! -e "$STAR_RUN") || (! -e "$BAMCOVERAGE_RUN") || (! -e "$SAMTOOLS_RUN") ]]
then
	echo "One of the program paths for either STAR aligner, BamCoverage or SamTools is incorrect."
	echo "Please ensure that the program paths have been changed to their correct paths on your\
 system and that they exist." 
	exit 1
fi

echo ""
echo "threads = " ${threads}
echo "fastqs per index will be deleted = " ${delete_fastq}
echo "output = " ${output}
echo "fastqs already exist = " ${exist}
echo "groups instead of barcodes = " ${groups}
echo ""
echo [$(date)] "Completed error checking inputs, pipeline will complete in background."
echo "Make sure to check pipeline_log.txt before using results in case the script terminated unexpectedly."

# To name files and paths
identify_experiment_name=not_exist
file_regex='^(.+)_(L[0-9]{3})_([RI][12])_.+\.fastq(\.gz)?$'
log=${working_dir}/pipeline_log.txt
exec 3>&1 1>>${log} 2>&1 	# handles printing of messages to log and terminal

echo "===========================================================" >> ${log}
echo [$(date)] "PID: $$" >> ${log}
echo "===========================================================" >> ${log}


## TRANSFER AND DECOMPRESS FASTQS
 for fastq in ${data_path}/*
 	do
	
 	if ${exist}; then echo [$(date)] "Already copied and uncompresseed fastqs" >> ${log}; break; fi

 	# check file is a read file
 	if [[ ${fastq} =~ ${file_regex} ]] && [[ ${BASH_REMATCH[3]} =~ 'R' ]]
 	then
 		file=$(basename ${fastq} .gz)
 		echo [$(date)] "Reading ${file}" >> ${log}
		
		# rsync it over, this way is safer in case fastq is huge
 		rsync -avz ${fastq} ${working_dir}
		
 		# uncompress file in place
 		gunzip ${working_dir}/${file}

		
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
 	fi
 done

 rm -fr ${working_dir}/SORTED_GROUPS/
 rm -fr ${working_dir}/_temp/
 echo [$(date)] "Cleaned directory for new run" >> ${log}

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

 		python3 parse_lane.py ${fastq} ${matrix} ${desired_barcodes} ${groups} ${indices} ${experiment_name} ${append_status} ${threads}

		if [[ $? -eq 0 ]]
		then
			echo [$(date)] "Completed lane: ${lane} " >> ${log}
		else
			echo [$(date)] "${lane} failed to run correctly, see traceback" >> ${log}
			exit 1
		fi
 	fi

 done

 echo [$(date)] "Completed fastq groups for: " >> ${log}
 echo [$(date)] "${experiment_name}" >> ${log}

## ALIGN TO HUMAN GENOME
./genome_align.sh ${working_dir} ${ref_genome} ${indices} $STAR_RUN $SAMTOOLS_RUN
echo [$(date)] "Completed all alignments " >> ${log}

## BAM TO BIGWIG CONVERSION
# only convert to bigwig if bigwig output is wanted or both bam and bigwig output is wanted
if [[ "$output" == "bigwig" || "$output" == "bambw" ]] 
then
	./bam_to_bigwig.sh ${working_dir} $BAMCOVERAGE_RUN
	echo [$(date)] "Completed all bigwig conversions " >> ${log}
fi

echo [$(date)] "Completed FASTQ files in each target cell directory " >> ${log}

## DELETE AND TIDY FILES
if [[  "$output" == "bigwig" ]] # only bigwig files are wanted as output
then
	file_extensions+=('.bam')
	file_extensions+=('.bai')
fi

if $delete_fastq # intermediate fastq files are to be deleted
then
	file_extensions+=('.fastq')
fi

## TIDYING OUTPUT (output desired formats, clean temp files)
echo "File types to be deleted: " ${file_extensions[@]}
./tidy_files.sh ${file_extensions[@]} "${working_dir}"
echo [$(date)] "Finished tidying up outputs" >> ${log}

## PRINTS DURATION OF SCRIPT
duration=${SECONDS}
echo "$((${duration} / 3600)) hours, $(((${duration} / 60) % 60)) minutes and $((${duration} % 60)) seconds elapsed" >> ${log}
echo [$(date)] "COMPLETED PIPELINE for: " >> ${log}
echo "${experiment_name}" >> ${log}
echo "===========================================================" >> ${log}