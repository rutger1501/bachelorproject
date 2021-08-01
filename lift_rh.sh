#!/bin/bash

for filename in vcf_files/*.vcf;
do
        naam=$(basename $filename)
        naam2=${naam%%.*}
        time CrossMap.py vcf hg19ToHg38.over.chain $filename hg38.fa lifted_files/lifted_$naam2.vcf

done
