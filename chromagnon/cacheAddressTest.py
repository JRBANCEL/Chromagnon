#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import cacheAddress

class CacheAddressTest(unittest.TestCase):

    def testFileType(self):
        """Parse Block Type From Address"""
        address = cacheAddress.CacheAddress(0x8000002A)
        self.assertEqual(address.blockType,
                         cacheAddress.CacheAddress.SEPARATE_FILE)
        address = cacheAddress.CacheAddress(0x9DFF0000)
        self.assertEqual(address.blockType,
                         cacheAddress.CacheAddress.RANKING_BLOCK)
        address = cacheAddress.CacheAddress(0xA0010003)
        self.assertEqual(address.blockType,
                         cacheAddress.CacheAddress.BLOCK_256)
        address = cacheAddress.CacheAddress(0xBDFF0108)
        self.assertEqual(address.blockType,
                         cacheAddress.CacheAddress.BLOCK_1024)
        address = cacheAddress.CacheAddress(0xCDFF0108)
        self.assertEqual(address.blockType,
                         cacheAddress.CacheAddress.BLOCK_4096)

    def testFilename(self):
        """Parse Filename from Address"""
        address = cacheAddress.CacheAddress(0x8000002A)
        self.assertEqual(address.fileSelector,
                         "f_0002A")
        address = cacheAddress.CacheAddress(0xA001135C)
        self.assertEqual(address.fileSelector,
                         "data_1")

if __name__ == "__main__":
    unittest.main()
