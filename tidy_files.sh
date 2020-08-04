#!/bin/bash

# Author: Chelsea Liang
# Function: given a list of file extenstions delete any of these file types in given directory

set -e						# if any error occurs, exit 1

read -a ARGS <<< "${BASH_ARGV[@]}" # read in the file extensions given in the inputted list
WORKING_DIR=${ARGS[0]}
EXPERIMENT_DIREC="${WORKING_DIR}/SORTED_GROUPS"

# go through each file extension 
for ((i = 1 ; i < ${#ARGS[@]} ; i++))
do
    extension=${ARGS[$i]}
    rm -f ${EXPERIMENT_DIREC}/*/*${extension} # delete the files of that extension from directory
done
echo [$(date)] "Deleted temp files" >> ${WORKING_DIR}/pipeline_log.txt


# move everything up into "${WORKING_DIR}/SORTED_GROUPS" to enable easy ctrl 
# selection of files for visualisation
mv ${EXPERIMENT_DIREC}/*/* ${EXPERIMENT_DIREC}/

# delete remaining sub-directories
for direc in ${EXPERIMENT_DIREC}/*
do 
    if [[ -d ${direc} ]]
    then
        rm -r ${direc}
    fi
done

echo [$(date)] "Moved output files up to SORTED_GROUPS/" >> ${WORKING_DIR}/pipeline_log.txt
