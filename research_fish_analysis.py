#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import csv
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from collections import Counter
from datetime import datetime
import math


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
    return pd.DataFrame(df[colname].value_counts())
    
def produce_count_and_na(df, colname):
    """
    When given a column, returns a count of its unique values
    This ALSO DOES count blank entries - unlike produce_count()
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """
    return pd.DataFrame(df[colname].value_counts(dropna = False))

def get_root_domains(dataframe,colname):
    """
    Takes a df and a column in it which contains urls, then extracts the main domain part (the 'netloc')
    of the url and writes the results into a new df
    :params: a data frame and a column name in the dataframe
    :return: a new df of URL netlocs
    """
#   initialise list
    list_of_rootdomains = list()
    
#   Take the colname column of df, strip out the nans (which break urlparser) and add it to urls
    urls = dataframe[colname].dropna()

#   User urlparse() to strip out the rootdomain (i.e, netloc) and write it to a list
    for i in urls:
        current_url = urlparse(i)
        list_of_rootdomains.append(current_url.netloc)

#   Convert the list into a df so we can use the same functions as are being used to summarise other data
    dataframeurl = pd.DataFrame({'rootdomains': list_of_rootdomains})
    return dataframeurl
    

def get_clean_years(dataframe,colname):
    """
    Takes the year in which submission was made and removes years that are not straighforward, namely
    "Pre-<year>" because it's so ambiguous: could be any year at all before <year>
    :params: a dataframe and a colname of the column in which the years are stored
    :return: a dataframe with only int years and NaNs
    """
#   Go through the rows, if you can't convert the year into an int, write a NaN back into the dataframe   
    for i, row in dataframe.iterrows():
        try:
            int(dataframe[colname][i])
        except:
            dataframe[colname][i] = np.nan
    return dataframe


def plot_bar_charts(dataframe,title,xaxis,yaxis,truncate):
    """
    Takes a two-column dataframe and plots it
    :params: a dataframe with two columns (one labels, the other a count), a title, and titles for the
    two axes (if title is None, then nothing is plotted), and a truncate variable which cuts down the number of
    rows plotted (unless it's 0 at which point all rows are plotted)
    :return: Nothing, just prints a chart
    """
    if truncate > 0:
#       This cuts the dataframe down to the number of rows given in truncate
        dataframe = dataframe.ix[:truncate]

    dataframe.plot(kind='bar')
    plt.title(title)
    if xaxis != None:
        plt.xlabel(xaxis)
    if yaxis != None:
        plt.ylabel(yaxis)
#   This provides more space around the chart to make it prettier        
    plt.tight_layout(True)
    plt.show()
    return


def main():
    """
    Main function to run program
    """
#   Import dataframe from original xls
    df = import_xls_to_df(DATAFILENAME)


#   Clean the years column
    df = get_clean_years(df,'Year First Provided')

#   Get a list of rootdomains (i.e. netloc) of URLs
    rootdomainsdf = get_root_domains(df,"URL")
    
#   Count the unique values in columns to get summaries of open/closed/no licence, which university released outputs
    open_source_licence = produce_count_and_na(df,'Open Source?')
    universities = produce_count_and_na(df,'RO')
    unique_rootdomains = produce_count_and_na(rootdomainsdf,'rootdomains')
    year_of_return = produce_count(df,'Year First Provided')

#    print(year_of_return.sort_values(by='Year First Provided'))
    print(type(year_of_return))

    writer = ExcelWriter('data/researchfish_results.xlsx')
    open_source_licence.to_excel(writer,'Licences')
    universities.to_excel(writer,'Universities')
    unique_rootdomains.to_excel(writer,'Repo domains')
    year_of_return.to_excel(writer,'Year of return')
    writer.save()


#    plot_bar_charts(year_of_return,'In which year were outputs submitted?', 'Year','Number of outputs',0)
#    plot_bar_charts(universities,'Top 30 universities that submit software as ResearchFish outputs',None, 'Number of outputs',30)
#    plot_bar_charts(open_source_licence,'Are ResearchFish outputs open-source licensed?', 'Licence','Number of outputs',0)
#    plot_bar_charts(unique_rootdomains,'Top 30 domains to store ResearchFish outputs', None, 'Number of outputs',30)

    


# OUTPUT

#    print("This is how many unique rootdomains there are: ",len(unique_rootdomains))
#    print(open_source_licence)
#    print(universities)
#    print(year_of_return)


    
#   Having a play with word frequency analysis
#    list_of_impact_sentences = df['Impact'].dropna().tolist()
#    list_of_impact_words = list()
#    for i in list_of_impact_sentences:
#        list_of_impact_words.append(i.split())
#    list_of_impact_words_cleaned = [item for sublist in list_of_impact_words for item in sublist]
#    counts = Counter(list_of_impact_words_cleaned)
#    counts = counts.most_common()
#    print(counts)

if __name__ == '__main__':
    main()
