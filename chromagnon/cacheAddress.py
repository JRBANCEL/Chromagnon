#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Chrome Cache Address
See /net/disk_cache/addr.h for design details
"""

class CacheAddress():
    """
    Object representing a Chrome Cache Address
    """
    SEPARATE_FILE = 0
    RANKING_BLOCK = 1
    BLOCK_256 = 2
    BLOCK_1024 = 3
    BLOCK_4096 = 4

    typeArray = ["Separate file",
                 "Ranking block file",
                 "256 bytes block file",
                 "1k bytes block file",
                 "4k bytes block file"]

    def __init__(self, uint_32):
        """
        Parse the 32 bits of the uint_32
        """
        self.binary = bin(uint_32)
        self.blockType = int(self.binary[3:6], 2)

        # If it is an address of a separate file
        if self.blockType == CacheAddress.SEPARATE_FILE:
            self.fileSelector = "f_%05X"%int(self.binary[6:], 2)
        else:
            self.contiguousBlock = int(self.binary[8:10], 2)
            self.fileSelector = "data_" + str(int(self.binary[10:18], 2))
            self.blockNumber = int(self.binary[18:], 2)

    def __str__(self):
        return hex(self.binary), CacheAddress.typeArray[self.blockType]
