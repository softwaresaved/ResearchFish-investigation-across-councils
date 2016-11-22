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


def main():
    """
    Main function to run program
    """
    dict_data = import_csv(DATAFILENAME)


if __name__ == '__main__':
    main()
