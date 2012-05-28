#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import textwrap

import cacheParse

# Ideas

def main():
    parser = argparse.ArgumentParser(
             formatter_class=argparse.RawDescriptionHelpFormatter,
             description=textwrap.dedent('''
\033[32mChromagnon Chrome Cache Parser\033[0m

\033[4mTwo input methods\033[0m
   1) A list of urls (usefull if you want to analyse only know urls).
      The entry corresponding to the url is found in the hash table,
      so it is fast.
   2) Parse the whole cash by not specifying urls. Usefull to get
      an exhaustive idea of what is in the cache. Can be slow if the
      cache has numerous entries.

\033[4mTwo output methods\033[0m
   1) Terminal output. Displays main details of each cache entry.
      Stderr is used for error messages.
   2) Export to files. The entries are exported to the given directory
      (specified with \033[1m-o\033[0m option). It is browsable with a web browser.
             '''))
    parser.add_argument("Cache Directory", action='store',
                        help="Chrome Cache Directory")
    parser.add_argument("-o", "-output", action='store',
                        default=None,
                        help="Export cached data to that directory \
                        (created if it doesn't exist)")
    parser.add_argument("-u", "-urls", action='store', nargs="+",
                        help="Use given urls as input")
    args = parser.parse_args()

    # Getting data
    cache = cacheParse.parse(args.__getattribute__("Cache Directory"), args.u)

    if args.o == None:
        for entry in cache:
            print entry
            print "-"*80
    else:
        cacheParse.export(cache, args.o)

if __name__ == "__main__":
    main()
