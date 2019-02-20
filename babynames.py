import sys
import re
import argparse


def extract_names(filename):
  names = []
  f = open(filename, 'rU')
  text = f.read()
  year_match = re.search(r'Popularity\sin\s(\d\d\d\d)', text)

  if not year_match:
    sys.stderr.write('Couldn\'t find the year!\n')
    sys.exit(1)
  year = year_match.group(1)
  names.append(year)
  tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
  names_to_rank =  {}

  for rank_tuple in tuples:
    (rank, boyname, girlname) = rank_tuple
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
  args = sys.argv[1:]

  if not args:
    print 'usage: [--summaryfile] file [file ...]'
    sys.exit(1)

  summary = False
  if args[0] == '--summaryfile':
    summary = True
    del args[0]

  for filename in args:
    names = extract_names(filename)
    text = '\n'.join(names)
    if summary:
      outf = open(filename + '.summary', 'w')
      outf.write(text + '\n')
      outf.close()
    else:
      print text

if __name__ == '__main__':
  main()