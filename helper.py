import re
import sys


if __name__ == '__main__':
    # read file
    with open("possible_words.txt") as possibleWords:
        words = [x.strip() for x in possibleWords.readlines()]

    # command line parsing
    if len(sys.argv) != 4:
        print("usage: helper.py known_positions included_characters excluded_characters")
        exit(1)

    known_positions = sys.argv[1]
    included_characters = set(sys.argv[2])
    excluded_characters = set(sys.argv[3])

    if len(known_positions) != 5:
        print(f"arg known_positions ({known_positions=} must be of length 5 but was of length {len(known_positions)}")
        exit(1)

    # filter possible words
    all_possible_chars = set('abcdefghijklmnopqrstuvwxyz')
    # exclude excluded characters
    possible_chars = ''.join(list(all_possible_chars - excluded_characters))
    re_str = known_positions.replace('-', f'[{possible_chars}]')
    r = re.compile(re_str)

    matches = list(filter(r.match, words))
    # require included characters
    matches = list(filter(lambda x: False not in [e in x for e in included_characters], matches))
    
    # output to user
    print(f"Show {len(matches)} possible words? [y/n] ", end='')
    if input().strip().lower() in ('yes', 'y'):
        print(*matches, sep="\n")
