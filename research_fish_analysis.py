#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import csv


DATAFILENAME = "./data/Software&TechnicalProducts - ResearchFish.csv"


def import_csv_to_dict(filename):
    """
    Importing csv into Python
    """
    with open(filename,'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for rows in reader:
            (rows)
    return data

def convert_to_df(dict_list):
    """
    Converts list of dicts into a pd dataframe
    :params: get a list of dicts
    :return: a pd df
    """
    return pd.DataFrame(dict_list)

def main():
    """
    Main function to run program
    """
    dict_data = import_csv(DATAFILENAME)
    convert_to_df
    

if __name__ == '__main__':
    main()
