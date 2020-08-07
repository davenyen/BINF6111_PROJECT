
# Voineagu Pipeline

Launches pipeline to parse CROP-Seq fastq data files into corresponding directories for each perturbation group and aligns reads in each group to the human genome. BigWig files are generated for visualisation in genome browsers.


# USER DOCUMENTATION

## Getting Started

1. Navigate to pipeline directory (contains all scripts)
2. Set variable paths
3. Launch script

### 1. Navigate to pipeline directory (contains all scripts)
To get started, download this repo and make sure you have your input files/directories ready. 

### 2. Set variable paths

#### Sample run (8 minutes, 2000 line fastqs)
sanity check master script
```
data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
working_dir=/Users/student/BINF6111_2020/test/check_master_script
```

#### Sample run (40 minutes, 100M line fastqs)
test 100 million for threading
```
data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
working_dir=/Users/student/BINF6111_2020/test/100mil_test
```

#### Sample full run (5.25 hour, 1B line fastqs)
full run A1
```
data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A1
matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A1.csv
desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA1.txt
indices=/Users/student/BINF6111_2020/data/Indices_A1.txt
working_dir=/Users/student/BINF6111_2020/test/full_run_A1
ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
```

full run A3
```
data_path=/Volumes/Data1/DATA/2020/CRISPRi_pilot_NovaSeq/Processed_FastQ_GOK7724/outs/fastq_path/GOK7724/GOK7724A3
matrix=/Users/student/BINF6111_2020/data/Barcode_Protospacer_Correspondence_GOK7724A3.csv
desired_barcodes=/Users/student/BINF6111_2020/data/barcodesA3.txt
indices=/Users/student/BINF6111_2020/data/Indices_A3.txt
working_dir=/Users/student/BINF6111_2020/test/full_run_A3
ref_genome=/Volumes/MacintoshHD_RNA/Users/rna/REFERENCE/HUMAN/Ensembl_GRCh37_hg19/STAR_genome_index
```


This master script launches this pipeline
- & at the end will run this script in a background process
- you may exit the shell when following is printed to the terminal:
"Completed error checking inputs, pipeline will complete in background"
- basic run:
```
mkdir -p ${working_dir}
./master_script.sh -w ${working_dir} -d ${data_path} -m ${matrix} \
-b ${desired_barcodes} -i ${indices} -r ${ref_genome} &
disown -h %1
```

```
working_dir      = The directory where you want the output
data_path        = The path to the full data directory containing fastqs
matrix           = The group, cell barcode correspondence matrix 
desired_barcodes = A list of desired barcodes, one barcode or group per line
indices          = A list of library indices, one index per line
ref_genome       = Path to the reference genome for STAR aligner
```

# Troubleshooting guide
- After line 111 in the master_script, all stderr and stdout and any conceivable error is piped to the pipeline_log.txt, look in there if something is not running as expected.
- If you would like to introduce a comment into the log file from the bash script do so with:
```
echo "message" >> ${log}
```
e.g.
```
echo [$(date)] "PID: $$" >> ${log}
```
- If you would like to introduce a comment into the log file from the python script do so with:
```
write_to_log (start_time, log_path, message_as_string_format)
```
e.g.
```
write_to_log (time.time(), working_dir + "/pipeline_log.txt", 
	"Creating {} \n for temporarily split files".format(split_dir))
```


# Help Flag
## SYNOPSIS
Launches pipeline to parse CROP-Seq fastq data files into corresponding directories for each perturbation group and aligns reads in each group to the human genome. BigWig files are generated for visualisation in genome browsers

## USAGE
./master_script.sh -w working_dir - d data_path -m matrix -b desired_barcodes -i indices -r ref_genome [-o output_format] [-f] [-e] [-g] [-t]

### Required flags

	-w	PATH to working directory for output 

	-d	PATH to input data

	-m	PATH to barcode correspondence matrix CSV file

	-b	PATH to txt file with list of barcodes

	-i	PATH to txt file with list of sample indices (library barcodes)

	-r	PATH to reference genome directory


### Optional flags
	
	-o		
	 bam		output files only in BAM format
	 bigwig		output files only in BigWig format
	 bambw      output files in BAM and BigWig format
				default: output is BAM and BigWig

	-f		keep fastq files in working directory
		    default: fastq files are deleted from working directory

	-e		fastq files already exist in working directories
			default: false

	-g		list of cell groups have been provided
			default: assumed list of barcodes has been provided

	-t		number of threads used to run for the script
			default: 8

## EXAMPLE
	./master_script.sh -w “experiment/results/” -d “DATA/fastq_path/A1/” -m “DATA/barcode_matrix.csv” -b “DATA/A1_barcodes.txt” -i “DATA/A1_indices.txt” -r “GENOMES/HUMAN/hg19/STAR_genome_index” -o “bigwig”

## AUTHORS
UNSW BINF6111 Team Voineagu 2020 - Caitlin Ramsay, Chelsea Liang, David Nguyen, Michal Sernero, Sehhaj Grewal
