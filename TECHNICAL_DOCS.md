
# TECHNICAL DOCUMENTATION

## Installation [TEAM_B]


### Prerequisites [TEAM_B]

* [Python3](https://www.python.org/downloads/)
* Star Aligner
* Linux OS

### master_script.sh setup [TEAM_B]
Change <x> paths in master_script.sh



## Versioning

For the versions available, see the [tags on this repository](https://github.com/cactusjuic3/teamvoineagu/tags). 


## Pipeline Components
All scripts have thorough documentation amongst the code. Below is a summary of the function of each script, dive into the code for specifics of implemenation!

### master_script.sh [TEAM_A]
Explain logic blah blah

### parse_lane.py 
- Create dictionary of form dictionary[16bp_barcode] = x:y:z by iterating through read one fastqs: output is dictionary
- Iterate through corresponding read two fastq, if coordinates exist in dictionary, assign the read to its target group and write reads out separated by their library index: output is one directory for every group with 4 fastqs inside, one for each
- For datasets with fastqs greater than 100 million lines, threading will be enabled to increase performance of pipeline


### genome_align.sh 
- Align fastq files in each cell target group to human genome using STAR aligner: output is BAM file

### bam_to_bigwig.sh 
- Convert BAM file to BigWig using bamCoverage from deepTools: output is BigWig

### tidy_files.sh 
- Deletes unwanted file formats and moves all output files to ${working_dir}/SORTED_GROUPS for easy visualisation

## Expert Functionality [TEAM_A]
- Read ones with erroneous indices will have their header printed to a fastq.error
- Percentage of these erroneous indices is printed in the log per lane
- You may identify these indices and incoporate them in another run
    - Go through read one fastq.error, grab [NNNNNN]
    - Add these indices into the indices list
    - Specify only bam output and rerun pipeline
    - At conclusion of run:
        - combine desired bam files together with samtools
        - convert bams to bigwig with ./bam_to_bigwig.sh
```
rna:check_master_script student$ head *error
==> 2000_PilotCROP_C_1_S1_L002_R1_001.fastq.error <==
@A00152:202:HJN5KDRXX:2:1101:27082:1016 1:N:0:CACTGGAG
@A00152:202:HJN5KDRXX:2:1101:27534:1016 1:N:0:TCCCTCCT
@A00152:202:HJN5KDRXX:2:1101:28782:1016 1:N:0:AGGAATTA
@A00152:202:HJN5KDRXX:2:1101:28908:1016 1:N:0:TCCCTCCT
@A00152:202:HJN5KDRXX:2:1101:31982:1016 1:N:0:ACCCTCCA
@A00152:202:HJN5KDRXX:2:1101:22083:1031 1:N:0:TCCCTCCT
```






## Authors [TEAM_B]

* **Chelsea Liang** - *Part A* - [LinkedIn](https://www.linkedin.com/in/chelsea-liang-03674b140/)
* **David Nguyen** - *Part A* - [Github](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
* **Caitlyn Ramsay** - *Part B* 
* **Michal Sernero** - *Part B* 
* **Sehhaj Grewal** - *Part B*

## License

This project is not licensed. 

## Acknowledgments [TEAM_B]

* Pydocs
* Stackoverflow

