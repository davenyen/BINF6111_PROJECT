#!/bin/bash

read -a ARGS <<< "${BASH_ARGV[@]}"
EXPERIMENT_DIREC=${ARGS[0]}

for ((i = 1 ; i < ${#ARGS[@]} ; i++))
do
    extension=${ARGS[$i]}
    rm ${EXPERIMENT_DIREC}/*/*${extension}
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