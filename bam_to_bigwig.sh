#!/bin/bash

# pass in the directory to the experiment/sample

# can use star aligner to output both BAM and wiggle
# --outSAMtype BAM Unsorted SortedByCoordinate
# --outWigType wiggle

WORKING_DIR = ${1}
EXPERIMENT_DIREC="${WORKING_DIR}/SORTED_GROUPS/"
BAMCOVERAGE_RUN="/Users/rna/anaconda2/bin/bamCoverage"
SAMTOOLS_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools"

SUB_DIRECS=$(ls "$EXPERIMENT_DIREC")

for direc in $SUB_DIRECS
do
    $BAMCOVERAGE_RUN --normalizeUsing CPM -p 8 -b "${EXPERIMENT_DIREC}/${direc}/${direc}.bam" -of bigwig -o "${EXPERIMENT_DIREC}/${direc}/${direc}.bw" > /dev/null 2>&1
    echo "Completed bam to bw conversion: ${direc}" >> ${WORKING_DIR}/pipeline_log.txt
done

