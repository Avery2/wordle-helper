import re
import sys


if __name__ == '__main__':
    # read file
    with open("possible_words.txt") as possibleWords:
        words = [x.strip() for x in possibleWords.readlines()]

    # command line parsing
    if len(sys.argv) != 4:
        print("usage: helper known included excluded")
        exit(1)

    known = sys.argv[1]
    included = set(sys.argv[2])
    excluded = set(sys.argv[3])

    if len(known) != 5:
        print(f"arg known ({known=} must be of length 5 but was of length {len(known)}")
        exit(1)

    # filter possible words
    all_possible_chars = set('abcdefghijklmnopqrstuvwxyz')
    # exclude excluded characters
    possible_chars = ''.join(list(all_possible_chars - excluded))
    re_str = known.replace('-', f'[{possible_chars}]')
    r = re.compile(re_str)

    matches = list(filter(r.match, words))
    # require included characters
    matches = list(filter(lambda x: False not in [e in x for e in included], matches))
    
    # output to user
    print(f"Show {len(matches)} possible words? [y/n] ", end='')
    if input().strip().lower() in ('yes', 'y'):
        print(*matches, sep="\n")
