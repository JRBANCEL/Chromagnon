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
Frontend script using Chrome Visited Links parsing library
"""

import argparse
import textwrap

import chromagnon.columnOutput
import chromagnon.visitedLinks

def main():
    parser = argparse.ArgumentParser(
             formatter_class=argparse.RawDescriptionHelpFormatter,
             description=textwrap.dedent('''
\033[32mChromagnon Chrome Visited Links\033[0m

Since the visited links are stored in a salted hash table, it is not possible
to extract the item of the hash table. It only possible to verify if a given
list is in the hash table.
             '''),
             epilog=textwrap.dedent('''
\033[4mExamples\033[0m
     > python chromagnonVisitedKinks.py ".config/chromium/Default/Visited Links" "http://www.google.fr/"
                     '''))
    parser.add_argument("visited_links_file", action='store',
                        help="Path to Chrome Visited Links File")
    parser.add_argument("urls", action='store', nargs="+",
                        help="Urls to check")
    args = parser.parse_args()

    result = chromagnon.visitedLinks.isVisited(args.__getattribute__(
                "visited_links_file"), args.urls)

    chromagnon.columnOutput.columnOutput(result)

if __name__ == "__main__":
    main()
