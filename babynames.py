#!/usr/bin/env python2

import sys
import re
import argparse

__author__ = "Clinton Johnson"


def extract_names(filename):
    '''This is returning an alphabetized list of ranked names'''
    print("Extracting names from: {}".format(filename))
    names = []
    with open(filename) as f:
        text = f.read()
    year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)

    if not year_match:
        print('Couldn\'t find the year!\n')
        sys.exit(1)
    year = year_match.group(1)
    names.append(year)
    tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>', text)
    names_to_rank =  {}

    for rank, boyname, girlname in tuples:
        if boyname not in names_to_rank:
            names_to_rank[boyname] = rank
        if girlname not in names_to_rank:
            names_to_rank[girlname] = rank

    sorted_names = sorted(names_to_rank.keys())

    for name in sorted_names:
        names.append(name + " " + names_to_rank[name])

    return names


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args:
        print 'usage: [--summaryfile] file [file ...]'
        sys.exit(1)

    for filename in args.files:
        names = extract_names(filename)
        text = '\n'.join(names)

        if args.summaryfile:
            with open(filename + '.summary', 'w') as outf:
                outf.write(text + '\n')
        else:
            print text

if __name__ == '__main__':
    main()