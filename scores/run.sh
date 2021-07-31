#!/bin/bash
for file in /home/rutger/Desktop/PharmCAT-0.8.0/output/trimmed_canada/*report.json 
do
    python3 scores.py $file
done


python3 graph.py

