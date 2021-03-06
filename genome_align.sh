#!/bin/bash

# Author: Team B: Caitlin Ramsay, Michal Sernero, Sehhaj Grewal
# UNSW BINF6111 Team Voineagu 
# Date: August 1 2020

# Function: Aligns fastq reads to human genome in STAR aligner using an adapter sequence
# and then outputs BAM files (and bai index files) for each cell group.

# commandline arguments: path to main directory with cell group outputs,
#                        path to directory with genome index,
#                        file of library barcodes/sample indexes,
#                        path to STAR aligner program,
#                        path to SamTools program

set -e						# if any error occurs, exit 1

WORKING_DIR=$1
EXPERIMENT_DIREC="${WORKING_DIR}/SORTED_GROUPS/" # directory to samples is passed in as the first argument
REFERENCE_GENOME=$2 # directory to reference genome index is passed in as the second argument
LIB_BARCODES=$(<$3) # text file containing library barcodes passed in as third argument + reads contents/stores as string
STAR_RUN=$4 #pathway/directory to run STAR Aligner Program
SAMTOOLS_RUN=$5 #pathway/directory to run SAMTOOLS program

SUB_DIRECS=$(basename `ls -d $EXPERIMENT_DIREC/*/`) # get all the names of the sub-directories to go through

#go through each library barcode (number of runs depends on the number of library barcodes)
for barcode in $LIB_BARCODES
do
    READ_FILES="" # string to store a list of files that need to be read into STAR aligner
    IDS="" # string to store a list of IDs to identify which reads belong to what target cell group
    
    # go through each sub-directory (ie. target cell group directory) in the experiment/sample directory
    for direc in $SUB_DIRECS
    do
        # append each read file corresponding with one of the four library barcodes
        # across all target cell group sub-directories into a string
        READ_FILES="${READ_FILES}${EXPERIMENT_DIREC}/${direc}/${direc}_${barcode}.fastq,"
        
        # using the target cell group name as an ID for each fastq read file
        # the ordering of the IDs corresponds to the ordering of the files in READ_FILES
        # ie. the first ID in IDs is the ID used for the fastq reads in the first target cell group
        IDS="${IDS}ID:${direc} , " 
    done
    READ_FILES=$(echo "$READ_FILES" | sed 's/,$//') # removes final comma from string (not needed)
    IDS=$(echo "$IDS" | sed 's/ , $//') # removes final comma + whitespace from string

    # inserting barcode string into appropriate position in the adaptor sequence
    # This adaptor sequence was given to us by Irina Voineagu's lab (2020)
    ADAPTOR="GATCGGAAGAGCACACGTCTGAACTCCAGTCAC${barcode}ATCTCGTATGCCGTCTTCTGCTTG"

    # run STAR aligner to map all the fastq files across all the target cell sub-directories
    # with the same adaptor sequence and library barcode
    # (STAR is only run depending on the number of library barcodes)
    # --outFileNamePrefix -> output BAM files into sample directory
    echo "STAR RUN for adaptor sequence: ${barcode}" >> ${WORKING_DIR}/pipeline_log.txt
    "$STAR_RUN" --runThreadN 8 \
        --genomeDir "$REFERENCE_GENOME" \
        --readFilesIn "$READ_FILES" \
        --outSAMattrRGline $IDS \
        --clip3pAdapterSeq "$ADAPTOR" \
        --outSAMtype BAM SortedByCoordinate \
        --outFileNamePrefix "${EXPERIMENT_DIREC}/" \
        --outSJfilterOverhangMin 15 15 15 15 \
        --alignSJoverhangMin 15 \
        --alignSJDBoverhangMin 15 \
        --outFilterMultimapNmax 1 \
        --outFilterScoreMin 1 \
        --outFilterMatchNmin 1 \
        --outFilterMismatchNmax 2 \
        --outFilterScoreMinOverLread 0.3 \
        --outFilterMatchNminOverLread 0.3 \
    >> ${WORKING_DIR}/pipeline_log.txt
    
    # splits the big BAM file into the associated target cell group BAM files
    # %!_${barcode} is the pattern for naming the BAM files for each target cell group
    # %! represents the target cell group name
    $SAMTOOLS_RUN split "${EXPERIMENT_DIREC}/Aligned.sortedByCoord.out.bam" -f "${EXPERIMENT_DIREC}/%!_${barcode}.bam" 
    echo [$(date)] "Completed split BAM file into target cell groups for barcode: ${barcode}" >> ${WORKING_DIR}/pipeline_log.txt

    #mv [filename] [dest-dir]
    # move each target cell group BAM file to it's respective directory
    for direc in $SUB_DIRECS
    do
       mv "${EXPERIMENT_DIREC}/${direc}_${barcode}.bam" "${EXPERIMENT_DIREC}/${direc}"
    done
    echo [$(date)] "Completed moving all BAM files into target cell directories for barcode: ${barcode}" >> ${WORKING_DIR}/pipeline_log.txt
done

# Tidy directory and delete intermediary files created from STAR aligner
rm "${EXPERIMENT_DIREC}/Aligned.sortedByCoord.out.bam" "${EXPERIMENT_DIREC}/Log.out" "${EXPERIMENT_DIREC}/Log.final.out" "${EXPERIMENT_DIREC}/Log.progress.out" "${EXPERIMENT_DIREC}/SJ.out.tab"
echo [$(date)] "Completed deleting leftover files from STAR run" >> ${WORKING_DIR}/pipeline_log.txt

# For each target cell group, merge all BAM files (one for each barcode) into 1 large BAM file
for direc in $SUB_DIRECS
do
    BAM_FILES=$(ls ${EXPERIMENT_DIREC}/${direc}/*.bam)
    $SAMTOOLS_RUN merge --threads 8 -c "${EXPERIMENT_DIREC}/${direc}/${direc}.bam" $BAM_FILES
    echo [$(date)] "Completed merging BAM files into one big BAM: ${direc}" >> ${WORKING_DIR}/pipeline_log.txt
    
    # After all BAM files have merged into 1 big BAM file, delete all intermediary BAM files
    rm $BAM_FILES

    # Each target cell group BAM file is indexed so it can be visualised.
    $SAMTOOLS_RUN index -b "${EXPERIMENT_DIREC}/${direc}/${direc}.bam"
    echo [$(date)] "Completed creating index file: ${direc}" >> ${WORKING_DIR}/pipeline_log.txt
done