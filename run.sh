for file in /home/rutger/Desktop/PGP-CANADA/lifted_files/*.vcf
do
        time java -jar build/libs/pharmcat-0.8.0-all.jar -vcf $file -j -o output/trimmed_canada
done
