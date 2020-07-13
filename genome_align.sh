#!/bin/bash

# commandline arguments: path to main directory with cell group outputs,
                        # path to directory with genome index

# ERROR HANDLING


# for each sub-directory in main experimental directory
    # perform STAR alignment on fastq file in there
    # needs to output to the same sub-directory
    # output needs to be BAM

# if there is a distinct number of adaptor/barcode sequences:
# for each adaptor sequence
    # perform STAR alignment on multiple fastq files
    # ie. every fastq file in each sub-direc associated
    # with the current adaptor sequence and provide
    # read groups for each different cell group
    # generates one BAM file 
    # split BAM file into multiple BAM files by
    # read groups: using samtools split
    # move each BAM file into its cell group directory

# once all smaller BAM files are in each sub-directory:
# merge all the BAM files together into one

#Reference genome "/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index"
EXPERIMENT_DIREC=$1
REFERENCE_GENOME=$2
STAR_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/STAR-2.5.2b/bin/MacOSX_x86_64/STAR"

SUB_DIRECS=$(ls "$EXPERIMENT_DIREC") # get all the names of the sub-directories to go through
FIRST_DIREC=$(echo "$SUB_DIRECS" | head -n1)
LIB_BARCODE_FILES=$(ls "${EXPERIMENT_DIREC}/${FIRST_DIREC}")
LIB_BARCODES=$(echo "$LIB_BARCODE_FILES" | sed 's/\.fastq//g')

for barcode in $LIB_BARCODES
do
    READ_FILES=""
    IDS=""
    for direc in $SUB_DIRECS
    do
        READ_FILES="${READ_FILES}${EXPERIMENT_DIREC}/${direc}/${barcode}.fastq,"
        IDS="${IDS}ID:${direc} , "
    done
    READ_FILES=$(echo "$READ_FILES" | sed 's/,$//')
    IDS=$(echo "$IDS" | sed 's/ , $//')
done

ADAPTOR="GATCGGAAGAGCACACGTCTGAACTCCAGTCAC${barcode}ATCTCGTATGCCGTCTTCTGCTTG"
"$STAR_RUN" --runThreadN 4 \
    --genomeDir "$REFERENCE_GENOME" \
    --readFilesIn "$READ_FILES" \
    --outSAMattrRGline $IDS \
    --clip3pAdapterSeq "$ADAPTOR" \
    --outSAMtype SAM \
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
	--chimSegmentMin 15 \
	--chimScoreMin 15 \
	--chimScoreSeparation 10 \
	--chimJunctionOverhangMin 15
    #/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools index -b "${EXPERIMENT_DIREC}/ARPC2/Aligned.sortedByCoord.out.bam"
    #/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools view -h -o "${EXPERIMENT_DIREC}/ARPC2/out.sam" "${EXPERIMENT_DIREC}/ARPC2/Aligned.sortedByCoord.out.bam"

#i=0
#SUB_DIRECS=$(ls "$1") # get all the names of the sub-directories to go through
# iterate through all sub-directories and perform STAR alignment on each fastq file
#for direc in $SUB_DIRECS
#do
#    if test $i -eq 3
#    then
#        break
#    fi
#    i=$((i+1))
#    "$STAR_RUN" --runThreadN 4 \
#    --genomeDir "$REFERENCE_GENOME" \
#    --readFilesIn "${EXPERIMENT_DIREC}/${direc}/${direc}.fastq" \
#    --outSAMtype BAM Unsorted SortedByCoordinate \
#    --outWigType bedGraph \
#   --outFileNamePrefix "${EXPERIMENT_DIREC}/${direc}/"
#    /Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools index -b "${EXPERIMENT_DIREC}/${direc}/Aligned.sortedByCoord.out.bam"
    # converts the bam file to bai
#done

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


