#!/bin/bash

# Author: Chelsea Liang
# Function: given a list of file extenstions delete any of these file types in given directory

read -a ARGS <<< "${BASH_ARGV[@]}" # read in the file extensions given in the inputted list
EXPERIMENT_DIREC=${ARGS[0]}

# go through each file extension 
for ((i = 1 ; i < ${#ARGS[@]} ; i++))
do
    extension=${ARGS[$i]}
    rm -f ${EXPERIMENT_DIREC}/*/*${extension} # delete the files of that extension from directory
done

# move everything up into "${WORKING_DIR}/SORTED_GROUPS" to enable easy ctrl 
# selection of files for visualisation
mv ${EXPERIMENT_DIREC}/*/* ${EXPERIMENT_DIREC}/

for direc in ${EXPERIMENT_DIREC}/*
do 
    if [[ -d ${direc} ]]
    then
        rm -r ${direc}
    fi
done