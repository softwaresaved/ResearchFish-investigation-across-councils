#!/usr/bin/env python
# encoding: utf-8

import pandas
import csv


DATAFILENAME = "./data/Software&TechnicalProducts - ResearchFish.csv"


def import_csv(filename):
    """
    Importing csv into Python
    """
    with open(filename,'r') as csvfile:
        datareader = csv.reader(csvfile)
        for rows in datareader:
            print(rows)
    
def main():
    """
    Main function to run program
    """
    import_csv(DATAFILENAME)


if __name__ == '__main__':
    main()