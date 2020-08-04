
# Voineagu Pipeline

Launches pipeline to parse CROP-Seq fastq data files into corresponding directories for each perturbation group and aligns reads in each group to the human genome. BigWig files are generated for visualisation in genome browsers


# USER DOCUMENTATION

## Getting Started

To get started, download this repo and make sure you have your input files/directories ready. 

To run the pipeline, enter this in your terminal
```
./master_script.sh ${working_dir} ${data_path} ${matrix} ${desired_barcodes} ${indices} ${ref_genome}
```
Where the files are:
```
Working_dir      = The directory where you want the output
Data_path        = The path to the full experiment data file
Matrix           = The barcode correspondence matrix 
Desired_barcodes = A list of desired barcodes
Indices          = A list of sample-indices or library barcodes 
Ref_genome       = The reference genome
```

## Pipeline Components

### master_script.sh
Explain logic blah blah

### parse_lane.py


### genome_align.sh

### bam_to_bigwig.sh

### tidy_files.sh


interests
# long walks on the beach


multithreading
flags to chose your output and inputs 
summary statistics
highly human readable logs
Irina is highly interested in the customisation of the normalisation from bam to bigwig cpm and other features

# TECHNICAL DOCUMENTATION

## Installation

### Prerequisites

* [Python3](https://www.python.org/downloads/)
* Star Aligner
* Linux OS

### master_script.sh setup
Change <x> paths in master_script.sh

## Running the tests

Testing is run via;

```
./test.sh 
```

### Break down into end to end tests

Explain what these tests test and why

```
Tests here
```

### And coding style tests

Explain what these tests test and why

```
Example here
```

## Deployment

Have the pipeline folder and run the script.

## Built With

* [IGV](link to igv here)
* [Python](https://www.python.org/)

## Versioning

For the versions available, see the [tags on this repository](https://github.com/cactusjuic3/teamvoineagu/tags). 

## Authors

* **Chelsea Liang** - *Part A* - [LinkedIn](https://www.linkedin.com/in/chelsea-liang-03674b140/)
* **David Nguyen** - *Part A* - [Github](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
* **Caitlyn Ramsay** - *Part B* 
* **Michal Sernero** - *Part B* 
* **Sehhaj Grewal** - *Part B*

## License

This project is not licensed. 

## Acknowledgments

* Pydocs
* Stackoverflow



# HELP FLAG
master_script

SYNOPSIS:
Launches pipeline to parse CROP-Seq fastq data files into corresponding directories for each perturbation group and aligns reads in each group to the human genome. BigWig files are generated for visualisation in genome browsers

USAGE:
./master_script.sh -w working_dir - d data_path -m matrix -b desired_barcodes -i indices -r ref_genome [-o output_format] [-f] [-e] [-g] [-t]

Required flags:
	-w	PATH to working directory for output 

	-d	PATH to input data

	-m	PATH to barcode correspondence matrix CSV file

	-b	PATH to txt file with list of barcodes

	-i	PATH to txt file with list of sample indices (library barcodes)

	-r	PATH to reference genome directory


Optional flags:
	-o		
	 bam		output files only in BAM format
	 bigwig		output files only in BigWig format
	 bambw          output files in BAM and BigWig format
			default: output is BAM and BigWig

	-f		keep fastq files in working directory
		        default: fastq files are deleted from working directory

	-e		fastq files already exist in working directories
			default: false

	-g		list of cell groups have been provided
			default: assumed list of barcodes has been provided

	-t		number of threads used to run for the script
			default: 8

EXAMPLE:
./master_script.sh -w “experiment/results/” -d “DATA/fastq_path/A1/” -m “DATA/barcode_matrix.csv” -b “DATA/A1_barcodes.txt” -i “DATA/A1_indices.txt” -r “GENOMES/HUMAN/hg19/STAR_genome_index” -o “bigwig”

AUTHORS:
UNSW BINF6111 Team Voineagu 2020 - Caitlin Ramsay, Chelsea Liang, David Nguyen, Michal Sernero, Sehhaj Grewal
