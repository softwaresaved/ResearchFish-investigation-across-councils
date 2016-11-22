#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import csv
import matplotlib.pyplot as plt
from urllib.parse import urlparse


DATAFILENAME = "./data/Software&TechnicalProducts - ResearchFish.xlsx"


def import_xls_to_df(filename):
    """
    Imports an Excel file into a Pandas dataframe
    :params: get an xls file
    :return: a df
    """
    return pd.read_excel(filename,sheetname='Software_TechnicalProducts')

def produce_count(df, colname):
    """
    When given a column, returns a count of its unique values
    This DOES NOT count blank entries - see produce_count_and_na
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """
    return df[colname].value_counts()
    
def produce_count_and_na(df, colname):
    """
    When given a column, returns a count of its unique values
    This also counts blank entries
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """
    return df[colname].value_counts(dropna = False)

def extract_URL_netloc(list):
    """
    Takes a list of URLs, then extracts the main domain part (the 'netloc')
    :params: a data frame and a column name in the dataframe
    :return: a list of URL netlocs
    """
    
    return 


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


def main():
    """
    Main function to run program
    """
#   Import dataframe from original xls
    df = import_xls_to_df(DATAFILENAME)

#    print(df.columns)



    """
    Need to count the unique values in columns to get summaries of the data
    1. Open/closed/no licence
    2. Which university released outputs
    """
    open_source_licence = produce_count_and_na(df,'Open Source?')
    universities = produce_count_and_na(df,'RO')
#   print(open_source_licence)
#    print(universities)

#   How many URLs are provided (need to find df length then subtract non_na count of URL column)
    missing_URLs = len(df) - df['URL'].count()

#    parsed = urlparse('http://netloc/path;parameters?query=argument#fragment')
#    print(parsed.netloc)
#    print(urls)

#    urls = df['URL']
#    cleaned_urls = urls[urls.URL.notnull()]
#    for i in urls:
#        print(i)
#        current_url = urlparse(i)
#        print(current_url)

    print(cleaned_urls)

if __name__ == '__main__':
    main()
