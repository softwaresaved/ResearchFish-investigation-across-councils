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
import logging


DATAFILENAME = "./data/Software&TechnicalProducts - ResearchFish.xlsx"
CHART_STORE_DIR = "./charts/"
EXCEL_RESULT_STORE = "./data/researchfish_results.xlsx"
IMPACT_RESULT_STORE = "./data/impact.txt"
LOGGERLOCATION = "./log/ResearchFishLog.log"


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


def clean_data(dataframe,colname):
    """
    Cleans the dataframe based on advice we have been given by EPSRC:
    1. Remove the tech products that don't actually relate to software
    2. Remove duplicate records (where a duplicate is defined as a record with the same 'Impact' and 'Tech product' as another record)
    1. Cleans the year in which submission was made and removes years that are not straighforward, namely "Pre-<year>" because it's ambiguous:
    could be any year at all before <year>
    2. Remove earlier years of data. Only 2012-2016 are reliable enough to include in the study
    3. Removes 'Type of tech product' that shouldn't have been included in the original data we were given. Only 'Software', 'Grid Application',
    'e-Business Platform' and 'Webtool/Application' should have been included.
    :params: a dataframe and a colname of the column in which the years are stored
    :return: a dataframe with only int years and NaNs
    """
    
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#   Want some metrics on how many records are being dropped. Set up a variable to store length of dataframe before each cleaning operation
    length_start = len(dataframe)

#   Drop all outputs that aren't related to the four products that are classed as software
    dataframe = dataframe[(dataframe['Type of Tech Product'] == 'Software') | (dataframe['Type of Tech Product'] == 'Grid Application') | (dataframe['Type of Tech Product'] == 'e-Business Platform') | (dataframe['Type of Tech Product'] == 'Webtool/Application')]

    length_tech_product = len(dataframe)
    
#   Remove duplicate entries where duplication occurs in the 'Impact' AND the 'Tech Product' fields
    dataframe.drop_duplicates(subset = ['Impact', 'Tech Product'], keep = 'first', inplace = True)

    length_dupes = len(dataframe)
    
#   Remove data from years where EPSRC are less certain that the data is accurate
    lost_years = ['2006', '2007', '2008', '2009', '2010', '2011']
    for year in lost_years:
        dataframe.drop(dataframe[dataframe[colname] == year].index, inplace = True)

    length_years = len(dataframe)
    
#   Go through the rows, if you can't convert the year into an int (i.e. the entry includes the text "Pre-"), write a NaN back into the dataframe 
    for i, row in dataframe.iterrows():
        try:
            int(dataframe[colname][i])
        except:
            dataframe[colname][i] = np.nan
    
#   Drop any data which lacks a info on Year First Provided because we're unsure of its provenance
    dataframe.dropna(subset=[colname], inplace=True)
    
    length_final = len(dataframe)

#   Print details on the changes to the dataframe length during cleaning
    logger.info("Records dropped during tech product cleaning: " + repr(length_start - length_tech_product))
    logger.info("Records dropped during duplicate cleaning: " + repr(length_tech_product - length_dupes))
    logger.info("Records dropped when cleaning years outside 2012-2016: " + repr(length_dupes - length_years))       
    logger.info("Records dropped during non-valid-year cleaning: " + repr(length_years - length_final))
    logger.info("Records left in cleaned data set: " + repr(length_final))
    
    return dataframe
    

def produce_count(dataframe, colname):
    """
    When given a column, returns a count of its unique values
    This DOES NOT count blank entries - unlike produce_count_and_na()
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """
    
    dataframe = pd.DataFrame(dataframe[colname].value_counts())
    
#   Add a column for percentages
    dataframe['percentage'] = dataframe[colname]/dataframe[colname].sum()
    
    return dataframe

    
def produce_count_and_na(dataframe, colname):
    """
    When given a column, returns a count of its unique values
    This ALSO DOES count blank entries - unlike produce_count()
    Special measures need to be employed for the 'Open source' column, because that question is only asked for 'Tech product' of the 
    'Software variety' hence the if statement
    :params: a data frame and a column name in the dataframe
    :return: a table of unique names and their count
    """

#   Employ special measures as discussed above for 'Open Source?' field
    if colname == 'Open Source?':
        temp_dataframe = dataframe[dataframe['Type of Tech Product'] == 'Software']
        dataframe = pd.DataFrame(temp_dataframe[colname].value_counts(dropna = False))
#        pd.DataFrame(dataframe[(dataframe['Tech Product'] == 'Software') & (dataframe[colname])].value_counts(dropna = False))
    else:
        dataframe = pd.DataFrame(dataframe[colname].value_counts(dropna = False))

#   Add a column for percentages
    dataframe['percentage'] = dataframe[colname]/dataframe[colname].sum()

    return dataframe


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
    :params: a dataframe and a column (colname) containing impact statements
    :return: write a text file containing all impact statements combined
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
    
#   Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(LOGGERLOCATION)
    handler.setLevel(logging.INFO)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Starting...')
#    logger.debug('Does this go to the screen?') 
    
#   I write back to the original dataframe and pandas warns about that, so turning off the warning    
    pd.options.mode.chained_assignment = None 
    
#   Import dataframe from original xls
    df = import_xls_to_df(DATAFILENAME)

    logger.info('Raw dataframe length before any processing: ' + repr(len(df)))

#   Add a column for URL pinging response
    add_column(df,'URL status')

#   Clean the dataframe
    df = clean_data(df,'Year First Provided')

#   Get a list of rootdomains (i.e. netloc) of URLs
    rootdomainsdf = get_root_domains(df,'URL')

#   Adds data into df about status of the URL at which software is stored
#    url_check = check_url_status(df,'URL','URL status')
#    url_df = pd.concat([url_check['URL'], url_check['URL status']], axis=1, keys=['URL', 'URL status'])
#    print(url_df)
    
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
    
    print(df.columns)


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
#    url_df.to_excel(writer,'urlstatus')
#    url_status.to_excel(writer,'urlstatus_summ')
    writer.save()


if __name__ == '__main__':
    main()
