#!/bin/bash

EXPERIMENT_DIREC=$1
SUB_DIRECS=$(ls "$EXPERIMENT_DIREC")

for direc in $SUB_DIRECS
do
    rm ${EXPERIMENT_DIREC}/${direc}/*.fastq
done