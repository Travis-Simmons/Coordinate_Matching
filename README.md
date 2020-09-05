# Coordinate_Matching
Coordinate matching script for the Pauli / Lyons Lab the University of Arizona

The purpose of this script is to process data that is produced by the StereoTopRGB phenotyping pipeline.
https://phytooracle.readthedocs.io/en/latest/4_StereoTopRGB_run.html

This script takes in two CSV files, one for each day of scans that need to be processed.

It then itterates over every genotype in the field and matches plants based on how close they are.

If they are the two closest plants they get named the same thing. The naming convention is the last four lettters of the genotype and the order it matched in.



How to run the script from the command line:

./coordinate_matching.py "first_day_scan.csv" "second_day_scan.csv" -o "output_directory" -of1 "output_filename_1_no_csv" -of2 "output_filename_2_no_csv"

6 arguments:
1. ./coordinate_matching.py (doesnt change unless you are running it from a separate directory)
2. "first_day_scan.csv" (filepath for the first SteroTopRGB output file you want to process)
3. "second_day_scan.csv" (filepath for the second SteroTopRGB output file you want to process
4. -o "output_directory" (output directory for both the matched csv's)
5. -of1 "output_filename_1_no_csv" (filename for the matched output of the first file DO NOT ADD .CSV to the end)
6. -of2 "output_filename_2_no_csv" (filename for the matched output of the second file DO NOT ADD .CSV to the end)
