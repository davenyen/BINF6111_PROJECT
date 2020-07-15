#!/bin/bash

# commandline arguments: path to main directory with cell group outputs,
                        # path to directory with genome index
                        # file of library barcodes/sample indexes
# ./genome_align.sh ../test/output/PilotCROP_C_1_S1_SORTED_GROUPS/ /Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index ../test/team_b_stuff/A1_sample_indices.txt

# ERROR HANDLING
    # make sure input library barcode file is in correct format

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
        # samtools split Aligned.out.bam -f '%!.{$barcode}'
        # %! means the read group name so the file will be
        # named with each cell group
    # move each BAM file into its cell group directory

# once all smaller BAM files are in each sub-directory:
# merge all the BAM files together into one

# Reference genome "/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index"
# Sample library indexes "../test/team_b_stuff/A1_sample_indices.txt"
EXPERIMENT_DIREC=$1
REFERENCE_GENOME=$2
LIB_BARCODES=$(<$3)
STAR_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/STAR-2.5.2b/bin/MacOSX_x86_64/STAR"

SUB_DIRECS=$(ls "$EXPERIMENT_DIREC") # get all the names of the sub-directories to go through

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

    ADAPTOR="GATCGGAAGAGCACACGTCTGAACTCCAGTCAC${barcode}ATCTCGTATGCCGTCTTCTGCTTG"
    "$STAR_RUN" --runThreadN 4 \
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
    
    # splits the big BAM file into the associated cell group BAM files
    /Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools split "${EXPERIMENT_DIREC}/Aligned.sortedByCoord.out.bam" -f "${EXPERIMENT_DIREC}/%!.${barcode}.bam"

    #mv [filename] [dest-dir]
    for direc in $SUB_DIRECS
    do
       mv "${EXPERIMENT_DIREC}/${direc}.${barcode}.bam" "${EXPERIMENT_DIREC}/${direc}"
    done
done



#/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools index -b "${EXPERIMENT_DIREC}/ARPC2/Aligned.sortedByCoord.out.bam"
#/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/samtools-1.3.1/samtools view -h -o "${EXPERIMENT_DIREC}/ARPC2/out.sam" "${EXPERIMENT_DIREC}/ARPC2/Aligned.sortedByCoord.out.bam"
