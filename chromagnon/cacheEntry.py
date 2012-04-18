#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Chrome Cache Entry
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import datetime
import struct

class CacheEntry():
    """
    See /net/disk_cache/disk_format.h for details.
    """

    #XXX Filename
    def __init__(self, address):
        """
        Parse a Chrome Cache Entry at the given address
        """
        block = open(address.path + address.fileSelector, 'rB')

        # Going to the right entry
        block.seek(8192 + address.blockNumber*address.entrySize)

        self.hash = struct.unpack('I', block.read(4))[0]
        self.next = struct.unpack('I', block.read(4))[0]
        self.rankingNode = struct.unpack('I', block.read(4))[0]
        self.usageCounter = struct.unpack('I', block.read(4))[0]
        self.reuseCounter = struct.unpack('I', block.read(4))[0]
        self.state = struct.unpack('I', block.read(4))[0]
        self.creationTime = datetime.datetime(1601, 1, 1) + \
                            datetime.timedelta(microseconds=\
                                struct.unpack('L', block.read(8))[0])
        self.keyLength = struct.unpack('I', block.read(4))[0]
        self.keyAddress = struct.unpack('I', block.read(4))[0]

        #XXX Skipping data
        block.seek(4*8, 1)
        self.flags = struct.unpack('I', block.read(4))[0]

    def __str__(self):
        return "Hash : 0x%08x"%self.hash + '\n'\
               "Next : 0x%08x"%self.next + '\n'\
               "Usage Counter : %d"%self.usageCounter + '\n'\
               "Reuse Counter : %d"%self.reuseCounter + '\n'\
               "Creation Time : %s"%self.creationTime + '\n'\
               "Key Length : %d"%self.keyLength + '\n'\
               "Key Address : 0x%08x"%self.keyAddress + '\n'\
               "Flags : 0x%08x"%self.flags
               #TODO State
