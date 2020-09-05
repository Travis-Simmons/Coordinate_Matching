# Coordinate_Matching
Coordinate matching script for the Pauli / Lyons Lab the University of Arizona

The purpose of this script is to process data that is produced by the StereoTopRGB phenotyping pipeline.
https://phytooracle.readthedocs.io/en/latest/4_StereoTopRGB_run.html

This script takes in two CSV files, one for each day of scans that need to be processed.

It then itterates over every genotype in the field and matches plants based on how close they are.

If they are the two closest plants they get named the same thing. The naming convention is the last four lettters of the genotype and the order it matched in.
