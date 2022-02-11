import re
import sys


def allowed_positions_only(word, excluded_positions):
    """Returns if a word doesn't use particular characters in the excluded positions"""
    for ch, ex in zip(word, excluded_positions):
        if ch in ex:
            return False
    return True

def uses_included_characters(word, included_characters):
    """Returns if a word uses all included characters"""
    return False not in [c in word for c in included_characters]

def match_known_positions_exclude_characters(known_positions, excluded_characters):
    """returns function that takes a word and returns if it uses the known positions and doesn't use the excluded characters"""
    # filter possible words
    all_possible_chars = set('abcdefghijklmnopqrstuvwxyz')
    possible_chars = ''.join(list(all_possible_chars - set(excluded_characters)))
    re_str = known_positions.replace('-', f'[{possible_chars}]')
    r = re.compile(re_str)
    return r.match

def filter_possible_words(possible_words, known_positions, included_characters, excluded_characters, excluded_positions=None):
    """Returns filtered possible words using parameters"""

    if included_characters == '-':
        included_characters = ''
    if excluded_characters == '-':
        excluded_characters = ''

    # exclude excluded characters and require known positions
    matches = list(filter(match_known_positions_exclude_characters(known_positions, excluded_characters), possible_words))
    # require included characters
    matches = list(filter(lambda x: uses_included_characters(x, included_characters), matches))
    # filter excluded positions
    if excluded_positions:
        matches = list(filter(lambda x: allowed_positions_only(x, excluded_positions), matches))
    
    return matches

if __name__ == '__main__':
    # read file
    with open("possible_words.txt") as possible_words_file:
        possible_words = [x.strip() for x in possible_words_file.readlines()]

    if not possible_words:
        print("failed to load possible words")
        exit(1)

    # command line parsing
    if len(sys.argv) < 4:
        print("usage: helper.py known_positions included_characters excluded_characters")
        exit(1)

    known_positions = sys.argv[1]
    included_characters = sys.argv[2]
    excluded_characters = sys.argv[3]
    excluded_positions = None

    if len(sys.argv) > 4:
        excluded_positions = sys.argv[4]
        if excluded_positions.count(",") != 4:
            print(f"arg excluded_positions ({excluded_positions}) must be of the form x,y,x,, with exactly 4 ,")
            exit(1)
        excluded_positions = excluded_positions.split(',')

    if len(known_positions) != 5:
        print(f"arg known_positions ({known_positions=} must be of length 5 but was of length {len(known_positions)}")
        exit(1)

    # filter words
    matches = filter_possible_words(possible_words, known_positions, included_characters, excluded_characters, excluded_positions)

    # output to user
    print(f"Show {len(matches)} possible words? [y/n] ", end='')
    if input().strip().lower() in ('yes', 'y'):
        print(*matches, sep="\n")
