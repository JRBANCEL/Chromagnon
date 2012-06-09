#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Column Output Module
"""

def columnOutput(queryResult, separator=' '):
    """
    Display the data in columns
    """

    # Finding width of columns
    size = [max([len(line[i]) for line in queryResult])
            for i in range(len(queryResult[0]))]
    # Generating format string
    string = (''.join(["%%-%ds%s"%(x, separator) for x in size]))[:-len(separator)]
    for line in queryResult:
        print string%tuple(line)
