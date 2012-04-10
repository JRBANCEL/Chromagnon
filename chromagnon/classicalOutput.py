#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

def classicalOutput(queryResult, separator="\t"):
    """
    Display the data separated by the specified separator
    """

    for line in queryResult:
        for element in line:
            os.write(1, unicode(element) + separator)
        os.write(1, '\n')
