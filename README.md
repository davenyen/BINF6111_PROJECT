
# Vpipe (project name)

This pipeline will sort a fastq file into groups based on their barcodes, indices and target/groups. It will then 
align these sorted files to the human genome and visualise it on IGV.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

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

### Prerequisites

Python3

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Have the pipeline folder and run the script.

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **David Nguyen** - *Part A* - [Github](https://github.com/davenyen)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Pydocs
* Stackoverflow
