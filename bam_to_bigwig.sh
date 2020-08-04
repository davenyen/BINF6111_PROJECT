#!/bin/bash

# UNSW BINF6111 Team Voineagu
# Authors: Caitlin Ramsay, Michal Sernero, Sehhaj Grewal
# Date: 2 August 2020

# Function: Converts BAM files into BigWig files using the bamCoverage function of deepTools
# Version of deepTools used in this version: 3.3.0

# commandline arguments: path to main directory with cell group outputs,
#                        path to BamCoverage program

# For more information on bamCoverage, use the link below:
# https://deeptools.readthedocs.io/en/develop/content/tools/bamCoverage.html

set -e						# if any error occurs, exit 1

#Directories of the Working Directory and the pathway to deepTools bamCoverage are given as arguments
WORKING_DIR=$1
EXPERIMENT_DIREC="${WORKING_DIR}/SORTED_GROUPS/"
BAMCOVERAGE_RUN=$2

SUB_DIRECS=$(basename `ls -d $EXPERIMENT_DIREC/*/`)

# Goes through each directory for each sample, and given a BAM and indexed BAM file
# run bamCoverage on the BAM file in the directory
# where -b, --bam is the input BAM file
# -o, --outFileName is the filename given for the Output file
# -of, --outFileFormat is the format of the Output file
# currently conversion chosen is bigwig
# can also be converted to bedgraph if chosen
# --normalizeUsing allows for normalization on the reads to be performed
# currently being normalised with CPM
# other options available include: RPKM, BPM, RPGC, None
# -p, --numberofProcessors allows for the use of multiple processors to be used
# current amount being used is 8

for direc in $SUB_DIRECS
do
    # Convert BAM to BigWig if the BAM file has reads
    if $BAMCOVERAGE_RUN --normalizeUsing CPM -p 8 -b "${EXPERIMENT_DIREC}/${direc}/${direc}.bam" -of bigwig -o "${EXPERIMENT_DIREC}/${direc}/${direc}.bw" > /dev/null 2>&1
    then
        echo "Completed bam to bw conversion: ${direc}" >> ${WORKING_DIR}/pipeline_log.txt
    else
        echo "BigWig file not created - no reads in BAM file: ${direc}" >> ${WORKING_DIR}/pipeline_log.txt
    fi
done

