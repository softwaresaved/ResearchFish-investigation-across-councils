#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import csv


DATAFILENAME = "./data/Software&TechnicalProducts - ResearchFish.csv"


def import_csv_to_dict(filename):
    """
    Importing csv into Python
    :params: get a str of the filename
    :return: a list() of dict()
    """
    output_list = list()
    with open(filename,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for rows in reader:
            output_list.append(rows)
    return output_list
    # return [rows for rows in reader]

def convert_to_df(dict_list):
    """
    Converts list of dicts into a pd dataframe
    :params: get a list of dicts
    :return: a pd df
    """
    return pd.DataFrame(dict_list)

def drop_column(df, columnname):
    """
    Drops unneeded column from dataframe
    :params: a dataframe and the unneeded column
    :return: a dataframe without the column
    Note the 1 in the function denotes columns
    rather than 0 used to drop rows
    """
    return df.drop(columnname,1)

def main():
    """
    Main function to run program
    """
    dict_data = import_csv_to_dict(DATAFILENAME)
    df = convert_to_df(dict_data)
    print(df.columns)
    df = drop_column(df, None)
    print(df.columns)

if __name__ == '__main__':
    main()
