
# Voineagu Pipeline

This pipeline will sort a fastq file into groups based on their barcodes, indices and target/groups. It will then 
align these sorted files to the human genome and visualise it on IGV.

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

### Prerequisites

* [Python3](https://www.python.org/downloads/)
* Star Aligner
* Linux OS

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

* **Chelsea Liang** - *Part A* 
* **David Nguyen** - *Part A* - [Github](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
* **Caitlyn Ramsay** - *Part B* 
* **Michal Sernero** - *Part B* 
* **Sehhaj Grewal** - *Part B*

## License

This project is not licensed. 

## Acknowledgments

* Pydocs
* Stackoverflow

## OLD README DELETE LATER?
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
