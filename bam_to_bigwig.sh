#!/bin/bash

# can use star aligner to output both BAM and wiggle
# --outSAMtype BAM Unsorted SortedByCoordinate
# --outWigType wiggle

BEDTOOLS_RUN="/Volumes/MacintoshHD_RNA/Users/rna/PROGRAMS/bedtools2/bin/intersectBed"

$("$BEDTOOLS_RUN" genomecov -bg -ibam PilotCROP_C_1_S1_SORTED_GROUPS/ARPC2/Aligned.out.bam -split -scale 1.0 > test.bedgraph)
$(bedGraphToBigWig test.bedgraph test.fasta.chrom.sizes kent.bw )
$(rm test.bedgraph)