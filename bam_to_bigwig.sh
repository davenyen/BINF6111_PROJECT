#!/bin/bash

# pass in the directory to the experiment/sample

# can use star aligner to output both BAM and wiggle
# --outSAMtype BAM Unsorted SortedByCoordinate
# --outWigType wiggle

WORKING_DIR=$1
EXPERIMENT_DIREC="${WORKING_DIR}/SORTED_GROUPS/"
BAMCOVERAGE_RUN=$2
SAMTOOLS_RUN=$3

SUB_DIRECS=$(ls "$EXPERIMENT_DIREC")

for direc in $SUB_DIRECS
do
    $BAMCOVERAGE_RUN --normalizeUsing CPM -p 8 -b "${EXPERIMENT_DIREC}/${direc}/${direc}.bam" -of bigwig -o "${EXPERIMENT_DIREC}/${direc}/${direc}.bw" > /dev/null 2>&1
    echo "Completed bam to bw conversion: ${direc}" >> ${WORKING_DIR}/pipeline_log.txt
done

