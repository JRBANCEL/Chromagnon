#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse the Chrome Visited Links
Reverse engineered from
  chrome/common/visitedlink_common.*
  chrome/browser/visitedlink/visitedlink_*
"""

import md5
import struct
import sys

VISITED_LINKS_MAGIC = 0x6b6e4c56;

def isVisited(path, urls):
    """
    Return the list of urls given in parameter with a boolean information
    about its presence in the given visited links file
    """
    output = []

    f = open(path, 'rB')

    # Checking file type
    magic = struct.unpack('I', f.read(4))[0]
    if magic != VISITED_LINKS_MAGIC:
        raise Exception("Invalid file")

    # Reading header values
    version = struct.unpack('I', f.read(4))[0]
    length = struct.unpack('I', f.read(4))[0]
    usedItems = struct.unpack('I', f.read(4))[0]

    # Reading salt
    salt = ""
    for dummy in range(8):
        salt += struct.unpack('c', f.read(1))[0]

    for url in urls:
        fingerprint = md5.new()
        fingerprint.update(salt)
        fingerprint.update(url)
        digest = fingerprint.hexdigest()

        # Inverting the result
        # Why Chrome MD5 computation gives a reverse digest ?
        fingerprint = 0
        for i in range(0, 16, 2):
            fingerprint += int(digest[i:i+2], 16) << (i/2)*8
        key = fingerprint % length

        # The hash table uses open addressing
        f.seek(key*8 + 24, 0)
        while True:
            finger = struct.unpack('L', f.read(8))[0]
            if finger == 0:
                output.append((url, False))
                break
            if finger == fingerprint:
                output.append((url, True))
                break
            if f.tell() >= length*8 + 24:
                f.seek(24)
            if f.tell() == key*8 + 24:
                output.append((url, False))
                break
    f.close()
    return output
