#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse the Chrome History File
Its a SQLite3 file
"""

import datetime
import re
import sqlite3
import sys

#XXX hardcoded filename
def parse(filename="../data/History"):

    # Connecting to the DB
    try:
        history = sqlite3.connect(filename)
    except sqlite3.Error, error:
        print "==> Error while opening the history file !"
        print "==> Details :", error.message
        sys.exit("==> Exiting...")

    # Retrieving all useful data
    result = history.execute("SELECT visits.visit_time, \
                               visits.from_visit, \
                               visits.transition, \
                               urls.url, \
                               urls.title, \
                               urls.visit_count, \
                               urls.typed_count, \
                               urls.last_visit_time \
                               FROM urls,visits \
                               WHERE urls.id=visits.url\
                               ORDER BY visits.visit_time;")
    output = []
    for line in result:
        output.append(HistoryEntry(line).toStr())
    return output

class Transition():
    """Object representing transition between history pages"""

    CORE_STRING = ["Link",\
                   "Typed",\
                   "Auto Bookmark",\
                   "Auto Subframe",\
                   "Manual Subframe",\
                   "Generated",\
                   "Start Page",\
                   "Form Submit",\
                   "Reload",\
                   "Keyword",\
                   "Keywork Generated"]

    def __init__(self, transition):
        """
        Parsing the transtion according to
        content/common/page_transition_types.h
        """
        self.core = transition & 0xFF
        self.qualifier = transition & 0xFFFFFF00

    def __str__(self):
        return Transition.CORE_STRING[self.core]

class HistoryEntry():
    """Object to store database entries"""

    def __init__(self, item):
        """Parse raw input"""
        self.visitTime = datetime.datetime(1601, 1, 1) + \
                         datetime.timedelta(microseconds=\
                         item[0])
        self.fromVisit = item[1]
        self.transition = Transition(item[2])
        self.url = item[3]
        self.title = item[4]
        self.visitCount = item[5]
        self.typedCount = item[6]
        self.lastVisitTime = datetime.datetime(1601, 1, 1) + \
                             datetime.timedelta(microseconds=\
                             item[7])

    def toStr(self):
        return [unicode(self.visitTime),\
                unicode(self.fromVisit),\
                unicode(self.transition),\
                unicode(self.url),\
                unicode(self.title),\
                unicode(self.visitCount),\
                unicode(self.typedCount),\
                unicode(self.lastVisitTime)]
