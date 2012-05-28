#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse the Chrome History File
Its a SQLite3 file
"""

import re
import sqlite3
import sys

#XXX hardcoded filename
def parse(filename="../data/History", formatString="itu"):
    """
    Format :
        i : id
        u : url
        t : title
        v : visit count
        c : typed count
        l : last visit time
        h : hidden
        f : favicon id
    """
    requestDict = {'i':("id", "id on database"),
                   'u':("url", "Complete url"),
                   't':("title", "Title of the webpage"),
                   'v':("visit_count", "Visit counter"),
                   'c':("typed_count", "Number of time the url was typed"),
                   'l':("last_visit_time", "Time of last visit"),
                   'h':("hidden", "TODO"),
                   'f':("favicon_id", "TODO")}

    try:
        history = sqlite3.connect(filename)
    except sqlite3.Error, error:
        print "==> Error while opening the history file !"
        print "==> Details :", error.message
        sys.exit("==> Exiting...")

    # Checking if the format string is correct
    if re.match(r"[iutvclhf]+$", formatString) == None:
        print "==> Incorrect format string !"
        print "==> History format specification :"
        for key, value in requestDict.items():
            print "\t{} : {}".format(key, value[1])
        sys.exit("==> Exiting...")

    # Creating the request from the specified format string

    request = ""
    for caracter in formatString[:-1]:
        request += requestDict[caracter][0] + ','
    request += requestDict[formatString[len(formatString) - 1]][0]

    return history.execute("select " + request + " from urls")
