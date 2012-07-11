#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012, Jean-Rémy Bancel <jean-remy.bancel@telecom-paristech.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Chromagon Project nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Jean-Rémy Bancel BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
import struct
import StringIO

"""
Reverse engineered from chrome/browser/sessions/*
"""


SNSS_MAGIC = 0x53534E53

def parse(path):
    """
    Parses SNSS files and returns a list of SNSS command objects
    """

    output = []

    f = open(path, 'rB')
    magic = struct.unpack('I', f.read(struct.calcsize('I')))[0]
    if magic != SNSS_MAGIC:
        raise Exception("Incorrect file type!")
    version = struct.unpack('I', f.read(struct.calcsize('I')))[0]

    while True:
#        try:
        # commandSize is a uint8
        commandSize = struct.unpack('h', f.read(struct.calcsize('h')))[0]
        if commandSize < 0:
            break

        # idType is a uint16
        idType = struct.unpack('B', f.read(struct.calcsize('B')))[0]

        # Size of idType is included in commandSize
        content = f.read(commandSize - struct.calcsize('B'))
        output.append(SNSSCommand(idType, commandSize, content))
#        except:
#            break

    f.close()
    return output

class SNSSCommand():

    commandSetTabWindow = 0
    commandSetTabIndexInWindow = 2
    commandWindowClosed = 4

    def __init__(self, idType, commandSize, content):
        self.idType = idType
        self.commandSize = commandSize
        self.content = content
        buf = StringIO.StringIO(self.content)

        if self.idType == SNSSCommand.commandWindowClosed:
            idType = struct.unpack('B', buf.read(struct.calcsize('B')))[0]
            closeTime = struct.unpack('Q', buf.read(struct.calcsize('Q')))[0]
            dateTime = datetime.datetime(1601, 1, 1) + \
                       datetime.timedelta(microseconds=closeTime)
            print idType, closeTime, dateTime
        elif self.idType == SNSSCommand.commandSetTabWindow:
            # Content is a WindowID on 8bits and an TabID on 8bits
            windowId = struct.unpack('h', buf.read(struct.calcsize('h')))[0]
            tabId = struct.unpack('h', buf.read(struct.calcsize('h')))[0]
            print "Window: %d, Tab: %d" % (windowId, tabId)
        elif self.idType == SNSSCommand.commandSetTabIndexInWindow:
            # Content is a TabID on 8bits and an index on 32bits
            tabID = struct.unpack('h', buf.read(struct.calcsize('h')))[0]
            index = struct.unpack('I', buf.read(struct.calcsize('I')))[0]
            print "TabId: %d, Index %d" % (tabID, index)


    def __str__(self):
        return "%s, %s" % (self.idType, self.commandSize)

if __name__ == "__main__":
    parse("/home/jrb/.config/chromium/Default/Last Session")
#    for item in parse("/home/jrb/.config/chromium/Default/Last Session"):
#        print item
