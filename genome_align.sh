#!/bin/bash

# commandline arguments: path to main directory with cell group outputs,
                        # path to directory with genome index

# for each sub-directory in main experimental directory
    # perform STAR alignment on fastq file in there
    # needs to output to the same sub-directory
    # output needs to be BAM