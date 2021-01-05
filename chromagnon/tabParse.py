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
This module parses SNSS tab commands used to store session states in chrome
"""

import datetime
import struct
import StringIO
import sys

import chromagnon.pickle as pickle
import chromagnon.types as types

TYPE_DICT = {'1': "CommandUpdateTabNavigation",
             '2': "CommandRestoredEntry",
             '3': "CommandWindow",
             '4': "CommandSelectedNavigationInTab",
             '5': "CommandPinnedState",
             '6': "CommandSetExtensionAppID"}

def parse(commandList):
    """
    Given a list of SNSS command, it returns a list of Tab Command
    """
    output = []

    for command in commandList:
        if TYPE_DICT.has_key(str(command.idType)):
            content = StringIO.StringIO(command.content)
            commandClass = sys.modules[__name__].__dict__.get(\
                           TYPE_DICT[str(command.idType)])
            output.append(commandClass(content))
    return output


class CommandUpdateTabNavigation():
    """
    Set a Tab in a Window
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

class CommandRestoredEntry():
    """
    TODO
    """
    def __init__(self, content):
        self.entryId = struct.unpack(types.int32, content.read(4))[0]

    def __str__(self):
        return "RestoredEntry - Entry: %d" % self.entryId

class CommandWindow():
    """
    TODO
    """
    def __init__(self, content):
        self.windowId = struct.unpack(types.int32, content.read(4))[0]
        self.selectedTabIndex = struct.unpack(types.int32, content.read(4))[0]
        self.numTab = struct.unpack(types.int32, content.read(4))[0]
        self.timestamp = struct.unpack(types.int64, content.read(8))[0]

    def __str__(self):
        return "CreateWindow - Window: %d, " % self.windowId +\
               "SelectedIndex: %d, " % self.selectedTabIndex +\
               "NumTab: %d, " % self.numTab +\
               "Time: %s" % self.timestamp

class CommandSelectedNavigationInTab():
    """
    TODO
    """
    def __init__(self, content):
        self.tabId = struct.unpack(types.int32, content.read(4))[0]
        self.index = struct.unpack(types.int32, content.read(4))[0]
        self.timestamp = struct.unpack(types.int64, content.read(8))[0]

    def __str__(self):
        return "SelectedNavigationInTab - Tab: %d, " % self.tabId +\
               "Index: %d, " % self.index +\
               "Time: %s" % self.timestamp

class CommandPinnedState():
    """
    TODO
    """
    def __init__(self, content):
        self.pinned = struct.unpack(types.int32, content.read(1))[0]

    def __str__(self):
        return "PinnedState - Pinned: %d" % self.pinned

class CommandSetExtensionAppID():
    """
    TODO
    """
    def __init__(self, content):
        content = pickle.Pickle(content)
        self.tabId = content.readInt()
        self.appId = content.readString()

    def __str__(self):
        return "SetExtensionAppID - Tab: %d, " % self.tabId +\
               "Extension: %s" % self.appId
