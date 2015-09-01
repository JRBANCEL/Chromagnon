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
Reverse engineered from chrome/browser/sessions/*
"""

import os
import struct

import types

SNSS_MAGIC = 0x53534E53

def parse(path):
    """
    Parses SNSS files and returns a list of SNSS command objects
    """
    output = []

    f = open(path, 'rb')
    f.seek(0, os.SEEK_END)
    end = f.tell()
    f.seek(0, os.SEEK_SET)
    magic = struct.unpack(types.int32, f.read(4))[0]
    if magic != SNSS_MAGIC:
        raise Exception("Invalid file header!")
    version = struct.unpack(types.int32, f.read(4))[0]

    while (end - f.tell()) > 0:
        # commandSize is a uint16
        commandSize = struct.unpack(types.uint16, f.read(2))[0]
        if commandSize == 0:
            raise Exception("Corrupted File!")
        # idType is a uint8
        idType = struct.unpack(types.uint8, f.read(1))[0]

        # Size of idType is included in commandSize
        content = f.read(commandSize - 1)
        output.append(SNSSCommand(idType, content))

    f.close()
    return output

class SNSSCommand():
    """
    A SNSS command :
        - An Id to identify the content of the payload
        - The payload
    """

    def __init__(self, idType, content):
        self.idType = idType
        self.content = content
