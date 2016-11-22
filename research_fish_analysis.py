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


def main();
    """
    Main function to run program
    """
    dict_data = import_csv_to_dict(DATAFILENAME)


if __name__ == '__main__':
    main()
