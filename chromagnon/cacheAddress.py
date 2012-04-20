#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Chrome Cache Address
See /net/disk_cache/addr.h for design details
"""

class CacheAddressError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CacheAddress():
    """
    Object representing a Chrome Cache Address
    """
    SEPARATE_FILE = 0
    RANKING_BLOCK = 1
    BLOCK_256 = 2
    BLOCK_1024 = 3
    BLOCK_4096 = 4

    typeArray = [("Separate file", 0),
                 ("Ranking block file", 36),
                 ("256 bytes block file", 256),
                 ("1k bytes block file", 1024),
                 ("4k bytes block file", 4096)]

    def __init__(self, uint_32, path):
        """
        Parse the 32 bits of the uint_32
        """
        if uint_32 == 0:
            raise CacheAddressError("Null Address")

        #XXX Is self.binary useful ??
        self.addr = uint_32
        self.path = path

        # Checking that the MSB is set
        self.binary = bin(uint_32)
        if len(self.binary) != 34:
            raise CacheAddressError("Uninitialized Address")

        self.blockType = int(self.binary[3:6], 2)

        # If it is an address of a separate file
        if self.blockType == CacheAddress.SEPARATE_FILE:
            self.fileSelector = "f_%06x"%int(self.binary[6:], 2)
        else:
            self.entrySize = CacheAddress.typeArray[self.blockType][1]
            self.contiguousBlock = int(self.binary[8:10], 2)
            self.fileSelector = "data_" + str(int(self.binary[10:18], 2))
            self.blockNumber = int(self.binary[18:], 2)

    def __str__(self):
        string = hex(self.addr) + " ("
        if self.blockType != CacheAddress.SEPARATE_FILE:
            string += str(self.contiguousBlock) +\
                      " contiguous blocks in "
        string += CacheAddress.typeArray[self.blockType][0] +\
                  " : " + self.fileSelector + ")"
        return string
