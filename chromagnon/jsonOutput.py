#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
JSON Output Module
"""

import json

def jsonOutput(queryResult, separator=''):
    """
    Display the data separated in JSON
    """

    print json.JSONEncoder().encode(queryResult)
