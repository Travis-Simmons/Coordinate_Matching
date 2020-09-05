#!/usr/bin/env python3

"""
#Author: Travis Simmons and Emmanuel Gonzalez
#Date: 06/14/2020
#Project: Pair Two Days of Scans
"""
import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib as plt
import math
import itertools
import re
import time

#------------------------------------------------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Rock the Casbah',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('csv_older',
                        metavar='str',
                        help='A CSV')
                        
    parser.add_argument('csv_newer',
                        metavar='str',
                        help='A CSV')

    parser.add_argument('-o',
                        '--outdir',
                        help='Output directory',
                        metavar='str',
                        type=str,
                        default='pointmatch_out')

    parser.add_argument('-of1',
                        '--outfile1',
                        help='Output filename',
                        metavar='str',
                        type=str,
                        default='point_matches')

    parser.add_argument('-of2',
                        '--outfile2',
                        help='Output filename',
                        metavar='str',
                        type=str,
                        default='point_matches')



    return parser.parse_args()
#-------------------------------------------------------------------------------------------
#Defining functions and opening storage lists
def distance(p0, p1):
    return abs(p0[0] - p1[0]) + abs(p0[1] - p1[1])
#-------------------------------------------------------------------------------------------

def main():
    args = get_args()

    #Inputs
    day1 = pd.read_csv(args.csv_older)
    day2 = pd.read_csv(args.csv_newer)

    # Initiating Storage Lists and Naming Integer
    # pnt_match = 0
    distances = []
    a_list_day1 = []
    a_list_day2 = []

    # Creates a list of all unique genotypes in day 2 that we can itterate over.
    geno_list = day2.genotype.unique().tolist()

    # Creates a list of all the unique genotypes in day 1 so we can be sure we dont try to look for matches 
    # from a genotype just in day 2
    geno_list2 = day1.genotype.unique().tolist()

    if 'Green_Towers_BORDER' in geno_list:
        geno_list.remove('Green_Towers_BORDER')
        
    if 'Green_Towers_BORDER' in geno_list2:
        geno_list2.remove('Green_Towers_BORDER')

    #------------------------------------------------------------------------------------------

    # Main Code Block

    # Sends the csv though this half of the code if it has not been matched before
    if not 'plant_name' in day1.columns:
        day1['plant_name'] = 'none'
        day2['plant_name'] = 'none'
        startTime = time.time()

        # Iterates over the genotypes list, so we are only matching one genotype at a time.
        for geno in geno_list:
            print(geno)
            pnt_match = 1
            
            #Checks to be sure the genotype was present both days.
            if geno in geno_list2:
            
                # Separates out the current genotype from the main dataframe
                sub_df1 = day1.set_index('genotype').loc[geno]
                sub_df2 = day2.set_index('genotype').loc[geno]

                # Checks to be sure the genotype isn't just one plant, and then 
                # creates a list of all the corrdinates like (x,y)
                print('length 1:', f'{len(sub_df1)}')
                print('length 2:', f'{len(sub_df2)}')
                if (len(sub_df1) >13) & (len(sub_df2) >13 ):
                    a_list_day1 = list(zip(sub_df1['long'], sub_df1['lat']))
                    a_list_day2 = list(zip(sub_df2['long'], sub_df2['lat']))
                    
                    # Goes through the above lists and combines them in every way possible with no repeat cobinations.
                    # It sends each combination to a stripped down distance formula, and stores it in the list "distances"
                    for a,b in itertools.product(a_list_day1, a_list_day2):
                        how_far = distance(a,b)
                        distances.append(how_far)
                    
                    # Defines what distance constitutes a match
                    short = min(distances)

                    # This is the actual matching codeblock, 
                    # This while loop stops when either of the lists run out of (x,y) points to find the distances of
                    while len(a_list_day2) >= 1 and len(a_list_day1) >=1:
                        
                        print(short)
                        #This is the average radius of whatever plant you are measuring
                        if short <0.06:
                        
                            # Finding the distances between all of the points.
                            for a,b in itertools.product(a_list_day1, a_list_day2):
                                how_far = distance(a,b)

                                # If the distance in between the points is the smallest of all of the distances we know the two
                                # points that produced it are likely the same plant.
                                # When a match is found, it is split up into its component lat and long
                                if how_far == short:
                                    match_1_lat = a[1]
                                    match_1_long = a[0]
                                    match_2_lat = b[1]
                                    match_2_long  = b[0]
                                    print('Match found...')

                                    #Narrows the search area (Genotype Searching)
                                    search1 = day1[day1['genotype'] == geno] 
                                    search2 = day2[day2['genotype'] == geno] 

                                    # This searches through the original day 1 csv to match up the lat and long that 
                                    # produced the first match, with the row that contains that lat and long

                                    #It then names it by the last four characters in the genotype name. 
                                    for index, row in search1.iterrows():
                                        if (day1.lat[index] == match_1_lat) & (day1.long[index] == match_1_long) & (day1.plant_name[index] == 'none'):
                                            day1.plant_name[index] = str(f'{geno[-4:]}'+'_'+ f'{pnt_match}')
                                            print('match 1 name:', f'{geno[-4:]}''_'f'{pnt_match}')
                                            print(day1.plant_name[index])

                                    # This searches through the original day 1 csv to match up the lat and long that 
                                    # produced the first match, with the row that contains that lat and long

                                    # It then adds one to the naming convention
                                    # cleares the distance list
                                    # removes the points that were a match from the lists that it searches through
                                    for index, row in search2.iterrows():
                                        if (day2.lat[index] == match_2_lat) & (day2.long[index] == match_2_long) & (day2.plant_name[index] == 'none'):
                                            day2.plant_name[index] = str(f'{geno[-4:]}'+'_'+ f'{pnt_match}')
                                            print('match 2 name:', f'{geno[-4:]}''_' f'{pnt_match}')
                                            pnt_match += 1
                                            distances.clear()
                                            a_list_day1.remove(a)
                                            a_list_day2.remove(b)
                                            print('Match Finished')
                                            print(f'{len(a_list_day2)}', 'Matches left for this genotype...')

                                            for a,b in itertools.product(a_list_day1, a_list_day2):
                                                how_far = distance(a, b)
                                                distances.append(how_far)

                                            if len(distances) != 0:
                                                short = min(distances)
                                                print ('The match took {0} second ! \n'.format(time.time() - startTime))
                                                startTime = time.time()
                                                
                        #Nothing is close move to the next geno
                        else: 
                                # Finding the distances between all of the points.
                            for a,b in itertools.product(a_list_day1, a_list_day2):
                                how_far = distance(a,b)

                                # If the distance in between the points is the smallest of all of the distances we know the two
                                # points that produced it are likely the same plant.
                                # When a match is found, it is split up into its component lat and long
                                if how_far == short:
                                    match_1_lat = a[1]
                                    match_1_long = a[0]
                                    match_2_lat = b[1]
                                    match_2_long  = b[0]
                                    print('Match found...')
                                    pnt_match += 1
                                    distances.clear()
                                    a_list_day1.remove(a)
                                    a_list_day2.remove(b)
                                    print('Match Finished')
                                    print(f'{len(a_list_day2)}', 'Matches left for this genotype...')

                                    for a,b in itertools.product(a_list_day1, a_list_day2):
                                        how_far = distance(a, b)
                                        distances.append(how_far)

                                    if len(distances) != 0:
                                        short = min(distances)
                                        print ('The match took {0} second ! \n'.format(time.time() - startTime))
                                        startTime = time.time()
                            
    # Everything below this will turn into the "second day matching"
    #-------------------------------------------------------------------------------------------------------
                                        
    else:
        day2['plant_name'] = 'none'
        print('New Matching Pair')
        startTime = time.time()
    # Iterates over the genotypes list, so we are only matching one genotype at a time.
        for geno in geno_list:
            print(geno)
            pnt_match = 1
            
            #Checks to be sure the genotype was present both days.
            if geno in geno_list2:
            
                # Separates out the current genotype from the main dataframe
                sub_df1 = day1.set_index('genotype').loc[geno]
                sub_df2 = day2.set_index('genotype').loc[geno]
                print('starting')

                # Checks to be sure the genotype isn't just one plant, and then 
                # creates a list of all the corrdinates like (x,y)
                print('length 1:', f'{len(sub_df1)}')
                print('length 1:', f'{len(sub_df1)}')
                if (len(sub_df1) >13) & (len(sub_df2) >13 ):
                    a_list_day1 = list(zip(sub_df1['long'], sub_df1['lat']))
                    a_list_day2 = list(zip(sub_df2['long'], sub_df2['lat']))
                    
                    # Goes through the above lists and combines them in every way possible with no repeat cobinations.
                    # It sends each combination to a stripped down distance formula, and stores it in the list "distances"
                    for a,b in itertools.product(a_list_day1, a_list_day2):
                        how_far = distance(a,b)
                        distances.append(how_far)
                        #print(' finding match')
                        #print(len(a_list_day2))
                    
                    # Defines what distance constitutes a match
                    short = min(distances)
                    
                    

                    # This is the actual matching codeblock, 
                    # This while loop stops when either of the lists run out of (x,y) points to find the distances of
                    while len(a_list_day2) >= 1 and len(a_list_day1) >=1:
                        print('check')
                        
                        if short <0.06:
                            
                            # Finding the distances between all of the points.
                            for a,b in itertools.product(a_list_day1, a_list_day2):
                                how_far = distance(a,b)

                                # If the distance in between the points is the smallest of all of the distances we know the two
                                # points that produced it are likely the same plant.
                                # When a match is found, it is split up into its component lat and long
                                if how_far == short:
                                    match_1_lat = a[1]
                                    match_1_long = a[0]
                                    match_2_lat = b[1]
                                    match_2_long  = b[0]
                                    print('Match found...')

                                    #Narrows the search area (Genotype Searching)
                                    search1 = day1[day1['genotype'] == geno] 
                                    search2 = day2[day2['genotype'] == geno] 


                                    for index, row in search1.iterrows():
                                        if (day1.lat[index] == match_1_lat) & (day1.long[index] == match_1_long):
                                            name = day1.plant_name[index]
                                            print(name)

                                    for index, row in search2.iterrows():

                                        if (day2.lat[index] == match_2_lat) & (day2.long[index] == match_2_long) & (day2.plant_name[index] == 'none'):
                                            day2.plant_name[index] = name
                                            pnt_match += 1
                                            print('Match Finished')
                                            print(f'{len(a_list_day1)}', 'Matches Left...')
                                            distances.clear()
                                            a_list_day1.remove(a)
                                            a_list_day2.remove(b)

                                            #Rebuilding the Distance list
                                            for a,b in itertools.product(a_list_day1, a_list_day2):
                                                how_far = distance(a, b)
                                                distances.append(how_far)

                                            if len(distances) != 0:
                                                short = min(distances)
                                                print('Distance between plants was', f'{short}')
                                                print ('The match took {0} second ! \n'.format(time.time() - startTime))
                                                startTime = time.time()
                        
                        else:
                            print('too far!!!!!!!!!!!!!!!!')
                                # Finding the distances between all of the points.
                            for a,b in itertools.product(a_list_day1, a_list_day2):
                                how_far = distance(a,b)

                                # If the distance in between the points is the smallest of all of the distances we know the two
                                # points that produced it are likely the same plant.
                                # When a match is found, it is split up into its component lat and long
                                if how_far == short:
                                    match_1_lat = a[1]
                                    match_1_long = a[0]
                                    match_2_lat = b[1]
                                    match_2_long  = b[0]
                                    print('Match found...')
                                    pnt_match += 1
                                    distances.clear()
                                    a_list_day1.remove(a)
                                    a_list_day2.remove(b)
                                    print('Match Finished')
                                    print(f'{len(a_list_day2)}', 'Matches left for this genotype...')

                                    for a,b in itertools.product(a_list_day1, a_list_day2):
                                        how_far = distance(a, b)
                                        distances.append(how_far)

                                    if len(distances) != 0:
                                        short = min(distances)
                                        print ('The match took {0} second ! \n'.format(time.time() - startTime))
                                        startTime = time.time()
                                    

    print('All Items Matched.')
    out_name1 = args.outfile1 + '.csv'
    out_name2 = args.outfile2 + '.csv'

    if not os.path.isdir(args.outdir):
        os.makedirs(args.outdir)

    out_path1 = os.path.join(args.outdir, out_name1)
    out_path2 = os.path.join(args.outdir, out_name2)
    day1.to_csv(out_path1)
    day2.to_csv(out_path2)

#--------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()


