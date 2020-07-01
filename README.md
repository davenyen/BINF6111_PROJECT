# teamvoineagu

Path for the files:
/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1

Bedtools and STAR can be found in these directories:
/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/bedtools2/
/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/STAR-2.5.2b/

The script to collect protospacer/barcode correspondences information from a bam file is at 
/Volumes/Data1/PROJECTS/CROPseq/Pilot/Scripts/getProtospacers.py
An example of its usage is at: 
cd /Volumes/Data1/PROJECTS/CROPseq/Pilot/hnPCR/iSeq_Script.txt
The original source is https://github.com/shendurelab/single-cell-ko-screens
TruSeq Read 1 is used to sequence 16 bp 10x Barcodes and 12 bp UMI

# ideas
add total_progress = {number of steps in the program} \n
Create progress bar with total_progress so we know how long the whole thing is going to take!\n
add a "man" function for parameters? cause it looks neat and clean
