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

import cacheParse

#XXX hardcoded filename
def parse(filename, start, end, checkCache=False, cachePath="/home/jrb/.cache/chromium/Default/Cache/"):
    """
    filename: path to the history file
    start: beginning of the time window
    end: end of the time window
    checkCache: check if each page in the history is in the cache
    """

    # Connecting to the DB
    try:
        history = sqlite3.connect(filename)
    except sqlite3.Error, error:
        print "==> Error while opening the history file !"
        print "==> Details :", error.message
        sys.exit("==> Exiting...")

    reference = datetime.datetime(1601, 1, 1)

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
                               AND visits.visit_time>%d\
                               AND visits.visit_time<%d\
                               ORDER BY visits.visit_time;"%\
                               (int((start-reference).total_seconds()*1000000),\
                               int((end-reference).total_seconds()*1000000)))\

    # Parsing cache
    cache = None
    if checkCache:
        cache = cacheParse.parse(cachePath)

    output = []
    for line in result:
        output.append(HistoryEntry(line, cache))
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

class HistoryEntry(object):
    """Object to store database entries"""
    COLUMN_STR = {'vt': "visitTime",
                  'fv': "fromVisit",
                  'tr': "transition",
                  'u':  "url",
                  'tl': "title",
                  'vc': "visitCount",
                  'tc': "typedCount",
                  'lv': "lastVisitTime"}

    def __init__(self, item, cache):
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

        # Searching in the cache if there is a copy of the page
        # TODO use a hash table to search instead of heavy exhaustive search
        if cache != None:
            for item in cache:
                if item.keyToStr() == self.url:
                    self.inCache = item
                    break
            self.inCache = None

    def toStr(self):
        return [unicode(self.visitTime),\
                unicode(self.fromVisit),\
                unicode(self.transition),\
                unicode(self.url),\
                unicode(self.title),\
                unicode(self.visitCount),\
                unicode(self.typedCount),\
                unicode(self.lastVisitTime)]

    def columnToStr(self, column):
        """Returns column content specified by argument"""
        return unicode(self.__getattribute__(HistoryEntry.COLUMN_STR[column]))
