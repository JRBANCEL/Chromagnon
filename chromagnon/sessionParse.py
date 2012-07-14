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

"""
This module parses SNSS session commands used to store session states in chrome
"""

import datetime
import struct
import StringIO
import sys

import chromagnon.pickle as pickle
import chromagnon.types as types

TYPE_DICT = {'0': "CommandSetTabWindow",
             '2': "CommandSetTabIndexInWindow",
             '3': "CommandTabClosed",
             '4': "CommandWindowClosed",
             '5': "CommandTabNavigationPathPrunedFromBack",
             '6': "CommandUpdateTabNavigation",
             '7': "CommandSetSelectedNavigationIndex",
             '8': "CommandSetSelectedTabInIndex",
             '9': "CommandSetWindowType",
             '11': "CommandTabNavigationPathPrunedFromFront",
             '12': "CommandSetPinnedState",
             '13': "CommandSetExtensionAppID",
             '14': "CommandSetWindowBounds3"}

def parse(commandList):
    """
    Given a list of SNSS command, it returns a list of SessionCommand
    """
    output = []

    for command in commandList:
        if TYPE_DICT.has_key(str(command.idType)):
            content = StringIO.StringIO(command.content)
            commandClass = sys.modules[__name__].__dict__.get(\
                           TYPE_DICT[str(command.idType)])
            output.append(commandClass(content))
    return output

class CommandSetTabWindow():
    """
    Set a Tab in a Window
    """
    def __init__(self, content):
        """
        content is a StringIO of the payload
        """
        # Content is Window ID on 8bits and Tab ID on 8bits
        # Strange alignment : two uint8 takes 8Bytes...
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "SetTabWindow - Window: %d, Tab: %d" % \
               (self.windowId, self.tabId)

class CommandSetTabIndexInWindow():
    """
    Set the Index of a Tab
    """
    def __init__(self, content):
        """
        content is a StringIO of the payload
        """
        # Content is Tab ID on 8bits and Index on 32bits
        # But due to alignment Tab ID is on 32bits
        self.tabId = struct.unpack(types.int32, content.read(4))[0]
        self.index = struct.unpack(types.int32, content.read(4))[0]

    def __str__(self):
        return "SetTabIndexInWindow - Tab: %d, Index: %d" % \
               (self.tabId, self.index)

class CommandTabClosed():
    """
    Store closure of a Tab with Timestamp
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Close Time on 64bits
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.closeTime = struct.unpack(types.int64, content.read(8))[0]
        # XXX Investigate on time format
#        closeTime = datetime.datetime(1601, 1, 1) + \
#                    datetime.timedelta(microseconds=closeTime/1000)

    def __str__(self):
        return "TabClosed - Tab: %d, Close Time: %s" % \
               (self.tabId, self.closeTime)

class CommandWindowClosed():
    """
    Store closure of a Window with Timestamp
    """
    def __init__(self, content):
        # Content is Window ID on 8bits and Close Time on 64bits
        self.windowId = struct.unpack(types.uint8, content.read(1))[0]
        self.closeTime = struct.unpack(types.int64, content.read(8))[0]
#        closeTime = datetime.datetime(1601, 1, 1) + \
#                    datetime.timedelta(microseconds=closeTime)

    def __str__(self):
        return "WindowClosed - Window: %d, CloseTime: %s" % \
               (self.windowId, self.closeTime)

class CommandTabNavigationPathPrunedFromBack():
    """
    TODO
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Index on 32bits
        self.tabId = struct.unpack(types.uint8, content.read(1))[0]
        # XXX Strange results...
        self.index = 0#struct.unpack(types.int32, content.read(4))[0]

    def __str__(self):
        return "TabNavigationPathPrunedFromBack - Tab: %d, Index: %d" % \
               (self.tabId, self.index)

class CommandUpdateTabNavigation():
    """
    Update Tab informations
    """
    def __init__(self, content):
        content = pickle.Pickle(content)
        self.tabId = content.readInt()
        self.index = content.readInt()
        self.url = content.readString()
        #print "Title:", content.readString16()
        #print "State:", content.readString()
        #print "Transition:", (0xFF & content.readInt())
        # Content is Window ID on 8bits and Tab ID on 8bits
        # Strange alignment : two uint8 takes 8Bytes...

    def __str__(self):
        return "UpdateTabNavigation - Tab: %d, Index: %d, Url: %s" % \
               (self.tabId, self.index, self.url)

class CommandSetSelectedNavigationIndex():
    """
    TODO
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Index on 32bits
        # But due to alignment Tab ID is on 32bits
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.index = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "SetSelectedNavigationIndex - Tab: %d, Index: %d" % \
               (self.tabId, self.index)

class CommandSetSelectedTabInIndex():
    """
    Set selected Tab in a Window
    """
    def __init__(self, content):
        # Content is Window ID on 8bits and Index on 32bits
        # But due to alignment Window ID is on 32bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.index = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "SetSelectedTabInIndex - Window: %d, Index: %d" % \
               (self.windowId, self.index)

class CommandSetWindowType():
    """
    Set Window Type
    """
    def __init__(self, content):
        # Content is Window ID on 8bits and Window Type on 32bits
        # But due to alignment Window ID is on 32bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.windowType = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "SetWindowType - Window: %d, Type: %d" % \
               (self.windowId, self.windowType)

class CommandTabNavigationPathPrunedFromFront():
    """
    TODO
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Count on 32bits
        # But due to alignment Tab ID is on 32bits
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.count = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "TabNavigationPathPrunedFromFront - Tab: %d, Count: %d" % \
               (self.tabId, self.count)

class CommandSetPinnedState():
    """
    Set Pinned State
    """
    def __init__(self, content):
        # Content is Tab ID on 8bits and Pinned State on 8bits
        # Strange alignment : two uint8 takes 8bits...
        self.tabId = struct.unpack(types.uint32, content.read(4))[0]
        self.pinned = struct.unpack(types.uint32, content.read(4))[0]

    def __str__(self):
        return "SetPinnedState - Tab: %d, Pinned: %d" % \
               (self.tabId, self.pinned)

class CommandSetExtensionAppID():
    """
    TODO
    """
    def __init__(self, content):
        self.content = pickle.Pickle(content)
        self.tabId = content.readInt()
        self.appId = content.readString()

    def __str__(self):
        return "SetExtensionAppID - Tab: %d, " % self.tabId +\
               "Extension: %d" % self.appId

class CommandSetWindowBounds3():
    """
    Set Window size, position and state
    """
    def __init__(self, content):
        # Content is
        #   Window ID on 8bits
        #   x, y, w, h on 32bits
        #   state on 32bits
        # Alignment : Window Id is in the first 32bits
        self.windowId = struct.unpack(types.uint32, content.read(4))[0]
        self.x = struct.unpack(types.int32, content.read(4))[0]
        self.y = struct.unpack(types.int32, content.read(4))[0]
        self.w = struct.unpack(types.int32, content.read(4))[0]
        self.h = struct.unpack(types.int32, content.read(4))[0]
        self.state = struct.unpack(types.int32, content.read(4))[0]

    def __str__(self):
        return "SetWindowBounds3 - Window: %d, x: %d, y: %d, w: %d, h: %d, " % \
               (self.windowId, self.x, self.y, self.w, self.h) + "State: %d" % \
               self.state
