#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Parse the Chrome Cache File
See http://www.chromium.org/developers/design-documents/network-stack/disk-cache
for design details
"""

import gzip
import os
import struct
import sys

import SuperFastHash

from cacheAddress import CacheAddress
from cacheBlock import CacheBlock
from cacheData import CacheData
from cacheEntry import CacheEntry


def parse(path, urls=None):
    """
    Reads the whole cache and store the collected data in a table
    or find out if the given list of urls is in the cache. If yes it
    return a list of the corresponding entries.
    """

    cacheBlock = CacheBlock(path + "index")

    # Checking type
    if cacheBlock.type != CacheBlock.INDEX:
        raise Exception("Invalid Index File")

    index = open(path + "index", 'rB')

    # Skipping Header
    index.seek(92*4)

    cache = []
    # If no url is specified, parse the whole cache
    if urls == None:
        print "Whole cache"
        for key in range(cacheBlock.tableSize):
            raw = struct.unpack('I', index.read(4))[0]
            if raw != 0:
                e = CacheEntry(CacheAddress(raw, path=path))
                cache.append(e)
    else:
        # Find the entry for each url
        for url in urls:
            # Compute the key and seeking to it
            hash = SuperFastHash.superFastHash(url)
            key = hash & (cacheBlock.tableSize - 1)
            index.seek(92*4 + key*4)

            addr = struct.unpack('I', index.read(4))[0]
            # Checking if the address is initialized (i.e. used)
            if addr & 0x80000000 == 0:
                print >> sys.stderr,\
                      "\033[32m%s\033[31m is not in the cache\033[0m"%url
                print >> sys.stderr, '-'*80

            # Follow the chained list in the bucket
            else:
                entry = CacheEntry(CacheAddress(addr, path=path))
                while entry.hash != hash and entry.next != 0:
                    entry = CacheEntry(CacheEntry(CacheAddress(entry.next,
                                                  path=path)))
                if entry.hash == hash:
                    cache.append(entry)
    return cache

def export(cache, outpath):
    """
    Export the cache in html
    """

    # Checking that the directory exists and is writable
    if not os.path.exists(outpath):
       os.makedirs(outpath)

    index = open(outpath + "index.html", 'w')
    index.write("<UL>")

    for entry in cache:
        # Adding a link in the index
        if entry.keyLength > 100:
            name = entry.keyToStr()[:100] + "..."
        else:
            name = entry.keyToStr()
        index.write('<LI><a href="%08x">%s</a></LI>'%(entry.hash, name))

        # Creating the entry page
        page = open(outpath + "%08x"%entry.hash, 'w')
        page.write("""<!DOCTYPE html>
                      <html lang="en">
                      <head>
                      <meta charset="utf-8">
                      </head>
                      <body>""")

        # Details of the entry
        page.write("<b>Hash</b>: 0x%08x<br />"%entry.hash)
        page.write("<b>Usage Counter</b>: %d<br />"%entry.usageCounter)
        page.write("<b>Reuse Counter</b>: %d<br />"%entry.reuseCounter)
        page.write("<b>Creation Time</b>: %s<br />"%entry.creationTime)
        page.write("<b>Key</b>: %s<br>"%entry.keyToStr())

        page.write("<hr>")
        if len(entry.data) == 0:
            page.write("No data associated with this entry :-(")
        for i in range(len(entry.data)):
            if entry.data[i].type == CacheData.UNKNOWN:
                # Extracting data into a file
                name = outpath + hex(entry.hash) + "_" + str(i)
                entry.data[i].save(name)

                if entry.httpHeader != None and \
                   entry.httpHeader.headers.has_key('content-encoding') and\
                   entry.httpHeader.headers['content-encoding'] == "gzip":
                    # XXX Highly inefficient !!!!!
                    input = gzip.open(name, 'rb')
                    output = open(name + "u", 'w')
                    output.write(input.read())
                    input.close()
                    output.close()
                    page.write('<a href="%su">%s</a>'%(name ,
                               entry.keyToStr().split('/')[-1]))
                else:
                    page.write('<a href="%s">%s</a>'%(name ,
                               entry.keyToStr().split('/')[-1]))


                # If it is a picture, display it
                if entry.httpHeader != None:
                    if entry.httpHeader.headers.has_key('content-type') and\
                       "image" in entry.httpHeader.headers['content-type']:
                        page.write('<br /><img src="%s">'%(name))
            # HTTP Header
            else:
                page.write("<u>HTTP Header</u><br />")
                for key, value in entry.data[i].headers.items():
                    page.write("<b>%s</b>: %s<br />"%(key, value))
            page.write("<hr>")
        page.write("</body></html>")
        page.close()

    index.write("</UL>")
    index.close()
