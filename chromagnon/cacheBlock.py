#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse the header of a Chrome Cache File
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import struct

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

    def __init__(self, filename):
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
            for _ in range(4):
                self.empty.append(struct.unpack('I', header.read(4))[0])
            self.position = []
            for _ in range(4):
                self.position.append(struct.unpack('I', header.read(4))[0])
        elif magic == CacheBlock.INDEX_MAGIC:
            self.type = CacheBlock.INDEX
            header.seek(2, 1)
            self.version = struct.unpack('h', header.read(2))[0]
            self.entryCount = struct.unpack('I', header.read(4))[0]
            self.byteCount = struct.unpack('I', header.read(4))[0]
            self.lastFileCreated = "f_%06x" % \
                                       struct.unpack('I', header.read(4))[0]
            header.seek(4*2, 1)
            self.tableSize = struct.unpack('I', header.read(4))[0]
        else:
            header.close()
            raise Exception("Invalid Chrome Cache File")
        header.close()
