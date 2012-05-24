#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import datetime
import sys

import classicalOutput
import columnOutput
import csvOutput
import historyParse

# TODO Remove if intropection
FORMAT_DICT = {'classical': classicalOutput.classicalOutput,
               'csv': csvOutput.csvOutput
              }
class DatetimeAction(argparse.Action):
    """
    This class parses a date given by the user and returns a datetime object
    The two accepted formats are : "%m/%d/%Y %H:%M:%S" and "%m/%d/%Y" where
    %m, %d, %Y, %H, %M, %S are the same as in strftime
    """
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            # Try first format
            value = datetime.datetime.strptime(values, "%m/%d/%Y %H:%M:%S")
        except:
            try:
                # Try second format
                value = datetime.datetime.strptime(values, "%m/%d/%Y")
            except:
                print >> sys.stderr, "Invalid datetime format !"
                sys.exit(-1)
        setattr(namespace, self.dest, value)

def main():
    parser = argparse.ArgumentParser(description="Parse Chrome history file")
    parser.add_argument("-s", "-start", action=DatetimeAction,
                        default=datetime.datetime(1601, 01, 01),
                        help="Low end of the time window : 'm/d/Y H:M:S' or 'm/d/Y'")
    parser.add_argument("-e", "-end", action=DatetimeAction,
                        default=datetime.datetime.now(),
                        help="High end of the time window : 'm/d/Y H:M:S' or 'm/d/Y'")
    parser.add_argument("-f", "-format", action='store',
                        choices=["csv", "column", "classical"])
    parser.add_argument("-d", "-delimiter", action='store', nargs=1,
                        default='\t', help="Delimiter used in output formating")
    parser.add_argument("-c", "-column", action='store', nargs='+',
                        choices=["vt", "fv", "tr", "u", "tl", "vc", "tc", "lv"],
                        help="Choose columns to display", default=["vt", "vc", "u"])
    parser.add_argument("filename", help="Path to History file",
                        action='store', type=str)
    args = parser.parse_args()
    print args

    # Getting data
    data = historyParse.parse(args.filename, args.s, args.e)

    # Creating a table according to chosen columns
    output = []
    for item in data:
        line = []
        for column in args.c:
            line.append(item.columnToStr(column))
        output.append(line)
    # TODO Intropection
    #print __package__.__getattribute__(args.f + "Output")
    #classicalOutput.classicalOutput(output, separator=args.d)
    csvOutput.csvOutput(output)

if __name__ == "__main__":
    main()
