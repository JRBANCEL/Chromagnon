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

    cache = []
    for key in range(os.path.getsize(path + "index")/4 - 92):
        #TODO
        raw = struct.unpack('I', index.read(4))[0]
        if raw != 0:
#            print "------------------------------------------------------------"
#            print "0x%08x"%key
            e = CacheEntry(CacheAddress(raw, path=path))
            cache.append(e)
#            print e
#            for i in range(len(e.data)):
#                if e.data[i].type == CacheData.UNKNOWN:
#                    e.data[i].save("/tmp/out/" + hex(e.hash) + "_" + str(i))
    return cache

#XXX Filename
def export(inpath="/home/jrb/.cache/chromium/Default/Cache/", outpath="/tmp/chromagnonExport/"):
    """
    Export the cache in html
    """

    # Checking that the directory exists and is writable
    if not os.path.exists(outpath):
       os.makedirs(outpath)

    # Parsing cache
    cache = parse(inpath)

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
