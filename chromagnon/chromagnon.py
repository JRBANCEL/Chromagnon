#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys

from classicalOutput import classicalOutput
from columnOutput import columnOutput
from csvOutput import csvOutput
import cacheParse
import historyInput


# Seems to be weird but if sys module is imported once, the setdefaultencoding
# function is not available. Whatever, set utf-8 for the whole project.
reload(sys)
sys.setdefaultencoding('utf-8')

cacheParse.export()

#classicalOutput(historyInput.parse(), ';')
#csvOutput(queryResult)
