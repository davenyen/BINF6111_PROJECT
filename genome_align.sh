#!/bin/bash

# commandline arguments: path to main directory with cell group outputs,
                        # path to directory with genome index

# for each sub-directory in main experimental directory
    # perform STAR alignment on fastq file in there
    # needs to output to the same sub-directory
    # output needs to be BAM

EXPERIMENT_DIREC=$1
REFERENCE_GENOME=$2
STAR_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/STAR-2.5.2b/bin/MacOSX_x86_64/STAR"

i=0
SUB_DIRECS=$(ls "$1") # get all the names of the sub-directories to go through
# iterate through all sub-directories and perform STAR alignment on each fastq file
for direc in $SUB_DIRECS
do
    if test $i -eq 3
    then
        break
    fi
    i=$((i+1))
    #"$STAR_RUN" --runThreadN 4 \
    #--genomeDir "$REFERENCE_GENOME" \
    #--readFilesIn "${EXPERIMENT_DIREC}/${direc}/${direc}.fastq" \
    #--outSAMtype BAM Unsorted SortedByCoordinate \
    #--outWigType bedGraph \
    #--outFileNamePrefix "${EXPERIMENT_DIREC}/${direc}/"
done

# TESTING OF DIFFERENT STAR PARAMETERS

#"$STAR_RUN" --genomeDir "$REFERENCE_GENOME" --genomeLoad LoadAndExit
#"$STAR_RUN" --runThreadN 1 --genomeDir "$REFERENCE_GENOME" --genomeLoad LoadAndKeep --readFilesIn "${EXPERIMENT_DIREC}/ARPC2/ARPC2.fastq" --outSAMtype BAM Unsorted --outFileNamePrefix "${EXPERIMENT_DIREC}/ARPC2/"
#"$STAR_RUN" --runThreadN 1 --genomeDir "$REFERENCE_GENOME" --genomeLoad LoadAndKeep --readFilesIn "${EXPERIMENT_DIREC}/ATP1B3/ATP1B3.fastq" --outSAMtype BAM Unsorted --outFileNamePrefix "${EXPERIMENT_DIREC}/ATP1B3/"
#"$STAR_RUN" --runThreadN 1 --genomeDir "$REFERENCE_GENOME" --genomeLoad LoadAndKeep --readFilesIn "${EXPERIMENT_DIREC}/BLM/BLM.fastq" --outSAMtype BAM Unsorted --outFileNamePrefix "${EXPERIMENT_DIREC}/BLM/"
#"$STAR_RUN" --genomeDir "$REFERENCE_GENOME" --genomeLoad Remove 

#"$STAR_RUN" --runThreadN 4 \
#--runMode alignReads \
#--genomeLoad LoadAndKeep \
#--genomeDir "$REFERENCE_GENOME" \
#--readFilesIn "${EXPERIMENT_DIREC}/ARPC2/ARPC2.fastq" \
#--outSAMtype BAM Unsorted SortedByCoordinate \
#--outWigType bedGraph \
#--outFileNamePrefix "${EXPERIMENT_DIREC}/ARPC2/"


#"$STAR_RUN" --runThreadN 4 \
##--genomeDir "$REFERENCE_GENOME" \
##--readFilesIn "${EXPERIMENT_DIREC}/ATP1B3/ATP1B3.fastq" \
#--outSAMtype BAM Unsorted SortedByCoordinate \
#--outWigType bedGraph \
#--outFileNamePrefix "${EXPERIMENT_DIREC}/ATP1B3/"

#"$STAR_RUN" --runThreadN 4 \
#--genomeDir "$REFERENCE_GENOME" \
#--readFilesIn "${EXPERIMENT_DIREC}/BLM/BLM.fastq" \
#--outSAMtype BAM Unsorted \
#--outFileNamePrefix "${EXPERIMENT_DIREC}/BLM/"


