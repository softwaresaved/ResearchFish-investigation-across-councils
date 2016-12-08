#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import csv
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from collections import Counter
import math
import requests
import httplib2


DATAFILENAME = "./data/Software&TechnicalProducts - ResearchFish.xlsx"
CHART_STORE_DIR = "./charts/"
EXCEL_RESULT_STORE = "./data/researchfish_results.xlsx"
IMPACT_RESULT_STORE = "./data/impact.txt"


def import_xls_to_df(filename):
    """
    Imports an Excel file into a Pandas dataframe
    :params: get an xls file
    :return: a df
    """
    return pd.read_excel(filename,sheetname='Software_TechnicalProducts')


def add_column(dataframe,newcol):
    """
    Adds a new column of NaNs called newcol
    :params: a dataframe and column name
    :return: a dataframe with a new column
    """
    dataframe[newcol] = np.nan
    return dataframe


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


def plot_bar_charts(dataframe,filename,title,xaxis,yaxis,truncate):
    """
    Takes a two-column dataframe and plots it
    :params: a dataframe with two columns (one labels, the other a count), a filename for the resulting chart, a title, and titles for the
    two axes (if title is None, then nothing is plotted), and a truncate variable which cuts down the number of
    rows plotted (unless it's 0 at which point all rows are plotted)
    :return: Nothing, just prints a chart
    """
    if truncate > 0:
#       This cuts the dataframe down to the number of rows given in truncate
        dataframe = dataframe.ix[:truncate]

    dataframe.plot(kind='bar', legend=None)
    plt.title(title)
    if xaxis != None:
        plt.xlabel(xaxis)
    if yaxis != None:
        plt.ylabel(yaxis)
#   This provides more space around the chart to make it prettier        
    plt.tight_layout(True)
    plt.savefig(CHART_STORE_DIR + filename + '.png', format = 'png', dpi = 150)
    plt.show()
    return


def impact_to_txt(dataframe,colname):
    """
    Takes a dataframe, collates all content in the colname column and writes it to a textfile
    """
#   Don't want any of the NaNs, so drop them
    dataframe.dropna(subset=[colname], inplace=True)
#   Open file for writing
    file_for_impacts = open(IMPACT_RESULT_STORE, 'w')
#   Go through dataframe row by row and write the text from the colname column to as a separate line to the text file
    for i, row in dataframe.iterrows():
        file_for_impacts.write("%s\n" % dataframe[colname][i])
    return
    
    
def check_url_status(dataframe, colname, statuscol):
    """
    Takes a dataframe and a column in that dataframe that contains URLs. Pings the URLs to see if they throw
    an exception, then writes the result to another column of the dataframe
    :params: a dataframe, a column (colname) in which URLs are stored and a column (statuscol) in which the 
    URL status will be recorded
    :return: a dataframe with the status of the URLs recorded in a column
    """
#   Don't want any of the NaNs, so drop the rows in which NaN was entered for the URL
    dataframe.dropna(subset=[colname], inplace=True)

    h = httplib2.Http()
    for i, row in dataframe.iterrows():
#        print(dataframe[statuscol][i])
        if math.isnan(dataframe[statuscol][i]) == True:
            try:
                print("Checking " + dataframe[colname][i])
                response, content = h.request(dataframe[colname][i])
                if response.status < 400:
                    dataframe[statuscol][i] = response['date']
#                    print(response['status'])
#                    print(response['date'])
            except: 
                pass
                dataframe[statuscol][i] = "No response"
    return dataframe

def main():
    """
    Main function to run program
    """
#   Import dataframe from original xls
    df = import_xls_to_df(DATAFILENAME)

#   Add a column for URL pinging response
    add_column(df,'URL status')

#   Clean the years column
    df = get_clean_years(df,'Year First Provided')

#   Get a list of rootdomains (i.e. netloc) of URLs
    rootdomainsdf = get_root_domains(df,'URL')

#   Adds data into df about status of the URL at which software is stored
    url_check = check_url_status(df,'URL','URL status')
    url_df = pd.concat([url_check['URL'], url_check['URL status']], axis=1, keys=['URL', 'URL status'])
    print(url_df)
#    url_df = pd.DataFrame(url_check['URL','URL status'])
    
#   Count the unique values in columns to get summaries of open/closed/no licence, which university released outputs, where outputs are being stored and in which year outputs were recorded
    open_source_licence = produce_count_and_na(df,'Open Source?')
    open_source_licence.index = open_source_licence.index.fillna('No response')
    universities = produce_count_and_na(df,'RO')
    unique_rootdomains = produce_count_and_na(rootdomainsdf,'rootdomains')
    year_of_return = produce_count(df,'Year First Provided')
    url_status = produce_count(df,'URL status')
#   Want this to be sorted in year order rather than in order of largest count
    year_of_return.sort_index(inplace = True)

#   Collate all impact statements into a text file for later word cloud generation
    impact_to_txt(df,'Impact')
    
    print(len(unique_rootdomains))


#   Plot results and save charts
#    plot_bar_charts(open_source_licence,'opensource','Is the output under an open-source licence?',None,'No. of outputs',0)
#    plot_bar_charts(universities,'universities','Top 30 universities that register the most outputs',None,'No. of outputs',30)
#    plot_bar_charts(unique_rootdomains,'rootdomain','30 most popular domains for storing outputs',None,'No. of outputs',30)
#    plot_bar_charts(year_of_return,'returnyear','When was output first registered?',None,'No. of outputs',0)


#   Write results to Excel spreadsheet for the shear hell of it
    writer = ExcelWriter(EXCEL_RESULT_STORE)
    open_source_licence.to_excel(writer,'opensource')
    universities.to_excel(writer,'universities')
    unique_rootdomains.to_excel(writer,'rootdomain')
    year_of_return.to_excel(writer,'returnyear')
    url_df.to_excel(writer,'urlstatus')
    url_status.to_excel(writer,'urlstatus_summ')
    writer.save()


if __name__ == '__main__':
    main()
