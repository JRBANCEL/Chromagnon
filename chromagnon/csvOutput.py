#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
CSV Output Module
"""

import csv
import sys

def csvOutput(queryResult, separator=',', quote='"'):
    """
    Display the data according to csv format
    """
    csvWriter = csv.writer(sys.stdout, delimiter=separator, quotechar=quote,
                           quoting=csv.QUOTE_MINIMAL)
    for line in queryResult:
        csvWriter.writerow(line)
