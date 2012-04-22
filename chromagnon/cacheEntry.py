#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Chrome Cache Entry
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import datetime
import struct

import cacheAddress
import cacheData

class CacheEntry():
    """
    See /net/disk_cache/disk_format.h for details.
    """

    def __init__(self, address):
        """
        Parse a Chrome Cache Entry at the given address
        """
        block = open(address.path + address.fileSelector, 'rB')

        # Going to the right entry
        block.seek(8192 + address.blockNumber*address.entrySize)

        # Parsing basic fields
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


        dataSize = []
        for dummy in range(4):
            dataSize.append(struct.unpack('I', block.read(4))[0])

        self.data = []
        for dummy in range(4):
            addr = struct.unpack('I', block.read(4))[0]
            try:
                addr = cacheAddress.CacheAddress(addr, address.path)
                # XXX
                if dummy == 0:
                    self.data.append(cacheData.CacheData(addr, dataSize[dummy],
                                                         True))
                else:
                    self.data.append(cacheData.CacheData(addr, dataSize[dummy]))

            except cacheAddress.CacheAddressError:
                pass

        self.flags = struct.unpack('I', block.read(4))[0]

        # Skipping pad
        block.seek(5*4, 1)

        # Reading local key
        if self.keyAddress == 0:
            self.key = ""
            for dummy in range(self.keyLength):
                self.key += struct.unpack('c', block.read(1))[0]
        # Key stored elsewhere
        else:
            addr = cacheAddress.CacheAddress(self.keyAddress, address.path)

            # It is probably an HTTP header
            self.key = cacheData.CacheData(addr, self.keyLength, True)

        block.close()

    def __str__(self):
        string = "Hash : 0x%08x"%self.hash + '\n'\
                 "Next : 0x%08x"%self.next + '\n'\
                 "Usage Counter : %d"%self.usageCounter + '\n'\
                 "Reuse Counter : %d"%self.reuseCounter + '\n'\
                 "Creation Time : %s"%self.creationTime + '\n'\
                 "Key Length : %d"%self.keyLength + '\n'\
                 "Key Address : 0x%08x"%self.keyAddress + '\n'\
                 "Key : %s"%self.key + '\n'\
                 "Flags : 0x%08x"%self.flags
                 #TODO State
        for data in self.data:
             string += "\nData (%d bytes) at 0x%08x : %s"%(data.size,
                                                           data.address.addr,
                                                           data)
        return string
