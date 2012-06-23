#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
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
