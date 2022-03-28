import os

from soupsieve import match

if os.name == "nt":
    import msvcrt
else:
    import sys, tty, termios

from shutil import move
from helper import filter_possible_words, find_words


def setGreen():
    GREEN = "\u001b[32m"
    print(GREEN, end="")


def setYellow():
    YELLOW = "\u001b[33m"
    print(YELLOW, end="")


def moveleft(n=1000):
    """Returns unicode string to move cursor left by n"""
    return "\u001b[{}D".format(n)


def known_positions_from_guess(guess):
    guess = guess.replace("_", "")
    acc = ""
    next_marked = False
    for c in guess:
        if next_marked:
            acc += c
            next_marked = False
        elif c not in ("*", "_"):
            acc += "-"
        next_marked = c == "*"
    return acc


def excluded_characters_from_guess(guess):
    acc = ""
    next_marked = False
    for c in guess:
        if not next_marked and c not in ("*", "_"):
            acc += c
            next_marked = False
        next_marked = c in ("*", "_")
    return acc


def included_characters_from_guess(guess):
    ex = excluded_characters_from_guess(guess)
    s = set(guess.replace("*", "").replace("_", "")) - set(ex)
    s = "".join([c for c in s])
    return s


def excluded_positions_from_guess(guess):
    guess = guess.replace("*", "")
    guess = guess.replace("__", "")
    acc = ""
    next_marked = False
    for i, c in enumerate(guess):
        if next_marked:
            acc += c
            next_marked = False
        next_marked = c == "_"
        if not next_marked:
            acc += ","
    acc = acc.replace("_", "")
    return acc[:-1]


def combine_excluded_positions(p1, p2):
    acc = []
    p1 = p1.split(",")
    p2 = p2.split(",")
    for a, b in zip(p1, p2):
        acc.append(a + b)
    return ",".join(acc)


def combine_known_positions(pos1, pos2):
    acc = ""
    for a, b in zip(pos1, pos2):
        if a != "-":
            acc += a
            continue
        if b != "-":
            acc += b
            continue
        acc += "-"
    return acc


RESET = "\x1b[0m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
GREY = "\u001B[0m"


def getColor(x):
    if x == 0:
        return RESET
    if x == 1:
        return YELLOW
    if x == 2:
        return GREEN


def getKey():
    if os.name == "nt":
        return msvcrt.getch().decode("utf-8")
    else:
        # https://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def conv2avry(list):
    ret = ""
    for let, color in list:
        if color == GREY:
            ret += let
        elif color == YELLOW:
            ret += "_" + let
        elif color == GREEN:
            ret += "*" + let
    return ret


def getGuess():
    x = 0
    oldKey = ""
    c_list = []
    while True:
        # get keypress
        key = getKey()

        # pop last word if backspace
        if key == "\b" and len(c_list) > 0:
            c_list.pop()

        # if its enter key, add the key onto string
        if key == "\r" and oldKey != "\r":
            c_list.append((oldKey, getColor(x)))
            x = 0  # reset color
            oldKey = ""
            if len(c_list) == 5:
                # flush output
                print(RESET, end="\n")
                break
            else:
                continue
        # make a new string for all chars + colors
        ns = ""
        for char, color in c_list:
            ns += color + char + RESET

        # if same key was pressed, update color
        if oldKey == key:
            x = (x + 1) % 3
        else:
            x = 0

        # print new key
        if key != "\b":
            ns += getColor(x) + key

        # flush spaces after (for backspace)
        ns += "\0" * (5 - len(c_list))

        print(" " + ns, end="\r")
        print(RESET, end="")

        oldKey = key
    return conv2avry(c_list)


def find_matches(guess, known_positions, included_characters, excluded_characters, excluded_positions):
    """Returns matches and dictionary of unused characters"""
    known_positions_ = known_positions_from_guess(guess)
    included_characters_ = included_characters_from_guess(guess)
    excluded_characters_ = excluded_characters_from_guess(guess)
    excluded_positions_ = excluded_positions_from_guess(guess)

    known_positions = combine_known_positions(known_positions, known_positions_)
    included_characters += included_characters_
    excluded_characters += excluded_characters_
    excluded_positions = combine_excluded_positions(
        excluded_positions, excluded_positions_
    )

    matches, l = filter_possible_words(
        known_positions,
        included_characters,
        excluded_characters,
        excluded_positions,
    )

    # calculate unused word dictonary
    inc_c = set(included_characters)
    s = "".join(matches)
    all_c = set(s)
    unused_characters = sorted(
        [(c, sum([1 if c in m else 0 for m in matches])) for c in all_c - inc_c], # results in list of tuples where first value is some character and the second value is the number of words it is in (from matches)
        key=lambda x: (x[1], x[0]),
        reverse=True,
    )

    return matches, l, unused_characters, known_positions, included_characters, excluded_characters, excluded_positions


def find_words_using_characters(unused_characters):
    unused_characters = {k: v for k,v in unused_characters}
    print("Choose characters that must be included in the word. ", end="")
    include_characters = input().strip()
    matches = find_words(include_characters)
    extra_characters = [set(match) - set(include_characters) for match in matches]
    sort_matches = list(zip(matches, [sum(unused_characters[c] for c in m if c in unused_characters) for m in extra_characters]))
    sort_matches.sort(key=lambda x: x[1], reverse=True)
    matches = sort_matches
    if len(matches) > 0:
        print(f"Show {len(matches)} possible words? [y/n] ", end="")
        if input().strip().lower() in ("yes", "y"):
            print(*matches, sep="\n")
    else:
        print("No possible words")


if __name__ == "__main__":

    known_positions = "-----"
    included_characters = ""
    excluded_characters = ""
    excluded_positions = ",,,,"
    unused_characters = []

    turn = 0
    while turn < 6:
        print("Make guess (1), use utility (2), or quit (q): ", end="")
        try:
            choice = input().strip()
            if choice.lower() in ("q", "quit"):
                break
            choice = int(choice)
        except:
            continue

        if choice == 1:
            guess = getGuess()
            matches, l, unused_characters, known_positions, included_characters, excluded_characters, excluded_positions = find_matches(guess, known_positions, included_characters, excluded_characters, excluded_positions)

            # output matches
            if len(matches) > 0:
                print(f"Show {len(matches)} possible words? [y/n] ", end="")
                if input().strip().lower() in ("yes", "y"):
                    # print(*l, sep="\n")
                    for (word, (num_overlap_char, num_overlap_word)) in l:
                        print(f"{word}: {num_overlap_word} {num_overlap_char}")
            else:
                print("No possible words")

            # output unused characters
            if len(unused_characters) > 0:
                print(
                    f"Show {len(unused_characters)} unused character frequencies? [y/n] ",
                    end="",
                )
                if input().strip().lower() in ("yes", "y"):
                    print(*unused_characters, sep="\n")
            else:
                print("No unused characters")

            turn += 1
        elif choice == 2:
            # words with character utility
            find_words_using_characters(unused_characters)
        else:
            print("Invalid option.")
