#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Classical Output Module
"""

import sys

def classicalOutput(queryResult, separator="\t"):
    """
    Display the data separated by the specified separator
    """

    for line in queryResult:
        for element in line:
            sys.stdout.write(element)
            sys.stdout.write(separator)
        sys.stdout.write('\n')
