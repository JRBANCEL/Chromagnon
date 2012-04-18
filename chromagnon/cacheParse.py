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
from cacheEntry import CacheEntry

class CacheBlock():
    """
    Object representing a block of the cache. It can be the index file or any
    other block type : 256B, 1024B, 4096B, Ranking Block.
    See /net/disk_cache/disk_format.h for details.
    """

    INDEX_MAGIC = 0xC103CAC3
    BLOCK_MAGIC = 0xC104CAC3
    INDEX = 0
    BLOCK = 1

    #XXX Filename
    def __init__(self, filename="../data/Cache"):
        """
        Parse the header of a cache file
        """
        header = open(filename, 'rB')

        # Read Magic Number
        magic = struct.unpack('I', header.read(4))[0]
        if magic == CacheBlock.BLOCK_MAGIC:
            self.type = CacheBlock.BLOCK
            header.seek(2, 1)
            self.version = struct.unpack('h', header.read(2))[0]
            self.header = struct.unpack('h', header.read(2))[0]
            self.nextFile = struct.unpack('h', header.read(2))[0]
            self.blockSize = struct.unpack('I', header.read(4))[0]
            self.entryCount = struct.unpack('I', header.read(4))[0]
            self.entryMax = struct.unpack('I', header.read(4))[0]
            self.empty = []
            for i in range(4):
                self.empty.append(struct.unpack('I', header.read(4))[0])
            self.position = []
            for i in range(4):
                self.position.append(struct.unpack('I', header.read(4))[0])
        elif magic == CacheBlock.INDEX_MAGIC:
            self.type = CacheBlock.INDEX
            header.seek(2, 1)
            self.version = struct.unpack('h', header.read(2))[0]
            self.entryCount = struct.unpack('I', header.read(4))[0]
            self.byteCount = struct.unpack('I', header.read(4))[0]
            self.lastFileCreated = "f_%06x"%struct.unpack('I', header.read(4))[0]
            header.seek(4*3, 1)
            self.tableSize = struct.unpack('I', header.read(4))[0]
        else:
            header.close()
            raise Exception("Invalid Chrome Cache File")
        header.close()

#XXX Filename
def parse(path="../data/Cache/"):
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
            print CacheEntry(CacheAddress(raw, path=path))
