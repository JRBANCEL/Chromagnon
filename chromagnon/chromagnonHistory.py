#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import datetime
import sys
import textwrap

import classicalOutput
import columnOutput
import csvOutput
import jsonOutput
import historyParse

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
    # Dirty !!!!!!!!!!!
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # TODO


    parser = argparse.ArgumentParser(
             formatter_class=argparse.RawDescriptionHelpFormatter,
             description=textwrap.dedent('''
\033[32mChromagnon Chrome History Parser\033[0m

\033[4mInput File\033[0m
    The input file of this program is the Chrome history file. It is a simple
    SQLite3 file. It's usual name is 'History'.

\033[4mTime Window\033[0m
    It is possible to filter the entries by a Time Window specified by the -e
    and -s flags. The date format is either 'm/d/Y H:M:S' or 'm/d/Y'.

\033[4mOutput Format\033[0m
    Four output formats are available. csv and json is what you expect to be.
    Classical is a format where fields are separated by a \\t and column is a
    format where every fields are displayed in columns. You can specify the
    format using the -f flags. Moreover, the delimiter can be change with -d
    flag.

\033[4mColumn Selection\033[0m
    To select which field to display, use the -c flag with the following options
        vt : Visit Time
        fv : Previous Page
        tr : Transition Description
        u :  Url
        tl : Page Title
        vc : Visit Counter
        tc : Typed Counter
        lv : Last Visit Time
        cc : Is Present in the Cache (Need to specify cache directory via -cache)
             '''))
    parser.add_argument("-s", "-start", action=DatetimeAction,
                        default=datetime.datetime(1601, 01, 01),
                        help="Low end of the time window : 'm/d/Y H:M:S' or "
                        "'m/d/Y'")
    parser.add_argument("-e", "-end", action=DatetimeAction,
                        default=datetime.datetime.now(),
                        help="High end of the time window : 'm/d/Y H:M:S' or "
                        "'m/d/Y'")
    parser.add_argument("-f", "-format", action='store', default="classical",
                        choices=["csv", "column", "classical", "json"])
    parser.add_argument("-d", "-delimiter", action='store',
                        help="Delimiter used in output formating")
    parser.add_argument("-c", "-column", action='store', nargs='+',
                        choices=["vt", "fv", "tr", "u", "tl", "vc", "tc", "lv",
                        "cc"], help="Choose columns to display",
                         default=["vt", "vc", "u"])
    parser.add_argument("-cache", action='store',
                        help="Cache directory to check if the pages are cached",
                        default=False)
    parser.add_argument("filename", help="Path to History file",
                        action='store', type=str)
    args = parser.parse_args()

    # Getting data
    if "cc" in args.c and not args.cache:
        print >> sys.stderr,\
                 "\033[31mIf you want to use 'cc' column you must specify the"\
                 "cache directory with -cache flag\033[0m"
        parser.print_help()
        sys.exit(-1)
    elif "cc" in args:
        data = historyParse.parse(args.filename, args.s, args.e, True,
                                  args.cache)
    else:
        data = historyParse.parse(args.filename, args.s, args.e, False, "")

    # Creating a table according to chosen columns
    output = []
    for item in data:
        line = []
        for column in args.c:
            line.append(item.columnToStr(column))
        output.append(line)

    # Printing table
    if args.d == None:
        sys.modules[args.f + "Output"].__getattribute__(args.f + "Output")\
            (output)
    else:
        sys.modules[args.f + "Output"].__getattribute__(args.f + "Output")\
            (output, separator=args.d)

if __name__ == "__main__":
    main()
