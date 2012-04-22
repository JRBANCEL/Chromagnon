#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse the Chrome Cache File
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import os
import struct

from cacheAddress import CacheAddress
from cacheBlock import CacheBlock
from cacheData import CacheData
from cacheEntry import CacheEntry


#XXX Filename
def parse(path="/home/jrb/.cache/chromium/Default/Cache/"):
    """
    Reads the whole cache and store the collected data in a table
    """

    cacheBlock = CacheBlock(path + "index")

    # Checking type
    if cacheBlock.type != CacheBlock.INDEX:
        raise Exception("Invalid Index File")

    index = open(path + "index", 'rB')

    # Skipping Header
    index.seek(92*4)

    for key in range(os.path.getsize(path + "index")/4 - 92):
        #TODO
        raw = struct.unpack('I', index.read(4))[0]
        if raw != 0:
            print "------------------------------------------------------------"
            print "0x%08x"%key
            e = CacheEntry(CacheAddress(raw, path=path))
            print e
            for i in range(len(e.data)):
                if e.data[i].type == CacheData.UNKNOWN:
                    e.data[i].save("/tmp/out/" + hex(e.hash) + "_" + str(i))

