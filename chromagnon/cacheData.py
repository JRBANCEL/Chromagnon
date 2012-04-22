#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Stores the data fetched in the cache.
Parse the HTTP header if asked.
"""

import os
import re
import struct

import cacheAddress

class CacheData():
    """
    Retrieve data at the given address
    Can save it to a separate file for export
    """

    HTTP_HEADER = 0
    UNKNOWN = 1

    def __init__(self, address, size, isHTTPHeader=False):
        """
        It is a lazy evaluation object : the file is open only if it is
        needed. It can parse the HTTP header if asked to do so.
        See net/http/http_util.cc LocateStartOfStatusLine and
        LocateEndOfHeaders for details.
        """
        self.size = size
        self.address = address
        self.type = CacheData.UNKNOWN

        if isHTTPHeader:
            # Getting raw data
            string = ""
            block = open(self.address.path + self.address.fileSelector, 'rB')
            block.seek(8192 + self.address.blockNumber*self.address.entrySize)
            for dummy in range(self.size):
                string += struct.unpack('c', block.read(1))[0]
            block.close()

            # Finding the beginning of the request
            start = re.search("HTTP", string)
            if start == None:
                return
            else:
                string = string[start.start():]

            # Finding the end (some null characters : verified by experience)
            end = re.search("\x00\x00", string)
            if end == None:
                return
            else:
                string = string[:end.end()-2]

            self.headers = {}
            for line in string.split('\0'):
                stripped = line.split(':')
                self.headers[stripped[0].lower()] = ':'.join(stripped[1:]).strip()
            self.type = CacheData.HTTP_HEADER

    def save(self, filename=None):
        """Save the data to the specified filename"""
        if self.address.blockType == cacheAddress.CacheAddress.SEPARATE_FILE:
           pass
        else:
            output = open(filename, 'wB')
            block = open(self.address.path + self.address.fileSelector, 'rB')
            block.seek(8192 + self.address.blockNumber*self.address.entrySize)
            output.write(block.read(self.size))
            block.close()
            output.close()

    def __str__(self):
        """
        Display the type of cacheData
        """
        if self.type == CacheData.HTTP_HEADER:
            if self.headers.has_key('content-type'):
                return "HTTP Header %s"%self.headers['content-type']
            else:
                return "HTTP Header"
        else:
            return "Data"
