#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Column Output Module
"""

def columnOutput(queryResult, separator=' '):
    """
    Display the data in columns
    """
    if len(queryResult) == 0:
        return

    # Finding width of columns
    size = [max([len(str(line[i])) for line in queryResult])
            for i in range(len(queryResult[0]))]
    # Generating format string (without last separator)
    string = (''.join(["%%-%ds%s" % (x, separator) for x in size]))\
                 [:-len(separator)]
    for line in queryResult:
        print string % tuple(line)
