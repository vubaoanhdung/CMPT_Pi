#!/bin/bash

if [ "$#" -ne 2 ]
then
    echo "usage: ./change_temperature min_temperature max_temperature"
else
    
    file=cmpt_pi.py
    min_value=$1
    max_value=$2

    #  check min_value
    if [ $min_value -gt $max_value ]
    then
        echo "Error: min_temperature cannot be greater than max_temperature"
        exit
    fi

    # check max_value
    if [ $max_value -lt $min_value ]
    then
        echo "Error: max_temperature cannot be less than min_temperature"
        exit
    fi

    # check temperature range
    if [ $min_value -lt 19 ] || [ $max_value -lt 19 ] || [ $min_value -gt 26 ] || [ $max_value -gt 26 ]
    then
        echo "Error: temperature must be in range [19, 26]"
        exit
    fi

    # if passing all checks, continue the execution
    sed -i "s/min_value =.*/min_value = '$min_value'/" $file
    sed -i "s/max_value =.*/max_value = '$max_value'/" $file

    # kill the current running program
    pkill -9 -f cmpt_pi.py

    # restart the program
    python3 cmpt_pi.py
fi