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
    This DOES NOT count blank entries - unlike produce_count_and_na()
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """
    return df[colname].value_counts()
    
def produce_count_and_na(df, colname):
    """
    When given a column, returns a count of its unique values
    This ALSO DOES count blank entries - unlike produce_count()
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """
    return df[colname].value_counts(dropna = False)

def get_root_domains(df,colname):
    """
    Takes a df and a column in it which contains urls, then extracts the main domain part (the 'netloc')
    of the url and writes the results into a new df
    :params: a data frame and a column name in the dataframe
    :return: a df of URL netlocs
    """
    list_of_rootdomains = list()
    
#   Take the colname column of df, strip out the nans (which break urlparser) and add it to urls
    urls = df[colname].dropna()

#   User urlparse() to strip out the rootdomain (i.e, netloc) and write it to a list
    for i in urls:
        current_url = urlparse(i)
        list_of_rootdomains.append(current_url.netloc)

#   Convert the list into a df so we can use the same functions as are being used to summarise other data
    dfurl = pd.DataFrame({'rootdomains': list_of_rootdomains})
    return dfurl

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

#   Get a list of rootdomains (i.e. netloc) of URLs
    rootdomains = get_root_domains(df,"URL")
    
#   Count the unique values in columns to get summaries of open/closed/no licence and which university released outputs
    open_source_licence = produce_count_and_na(df,'Open Source?')
    universities = produce_count_and_na(df,'RO')
    unique_rootdomains = produce_count_and_na(rootdomains,'rootdomains')
    
    print(type(unique_rootdomains))
    print("This is how many unique rootdomains there are: ",len(unique_rootdomains))
    for_printing = unique_rootdomains.ix[:30]   
    for_printing.plot(kind='bar')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
