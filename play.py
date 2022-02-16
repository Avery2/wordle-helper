from helper import filter_possible_words, find_words


# def setGreen():
#     GREEN = "\u001b[32m"
#     print(GREEN, end='')


# def setYellow():
#     YELLOW = "\u001b[33m"
#     print(YELLOW, end='')


def known_positions_from_guess(guess):
    guess = guess.replace('_', '')
    acc = ''
    next_marked = False
    for c in guess:
        if next_marked:
            acc += c
            next_marked = False
        elif c not in ('*', '_'):
            acc += '-'
        next_marked = c == '*'
    return acc


def excluded_characters_from_guess(guess):
    acc = ''
    next_marked = False
    for c in guess:
        if not next_marked and c not in ('*', '_'):
            acc += c
            next_marked = False
        next_marked = c in ('*', '_')
    return acc


def included_characters_from_guess(guess):
    ex = excluded_characters_from_guess(guess)
    s = set(guess.replace('*', '').replace('_', '')) - set(ex)
    s = ''.join([c for c in s])
    return s


def excluded_positions_from_guess(guess):
    guess = guess.replace('*', '')
    guess = guess.replace('__', '')
    acc = ''
    next_marked = False
    for i, c in enumerate(guess):
        if next_marked:
            acc += c
            next_marked = False
        next_marked = c == '_'
        if not next_marked:
            acc += ','
    acc = acc.replace('_', '')
    return acc[:-1]


def combine_excluded_positions(p1, p2):
    acc = []
    p1 = p1.split(',')
    p2 = p2.split(',')
    for a,b in zip(p1, p2):
        acc.append(a + b)
    return ','.join(acc)


def combine_known_positions(pos1, pos2):
    acc = ''
    for a, b in zip(pos1, pos2):
        if a != '-':
            acc += a
            continue
        if b != '-':
            acc += b
            continue
        acc += '-'
    return acc


if __name__ == '__main__':

    print("Type the response for each wordle guess. Indicate yellow by prepending with one underscore (_) and indicate green by prepending with two underscores (__)")

    known_positions = '-----'
    included_characters = ''
    excluded_characters = ''
    excluded_positions = ',,,,'

    turn = 0
    while turn < 6:
        print("Make guess (1) or use utility (2)? [1/2] ", end="")
        choice = int(input().strip())

        if choice == 1:
            guess = ''
            while len(guess.replace("_", "")) != 5:
                print(f"Guess {turn}: ", end='')
                guess = input().lower()

            guess = guess.replace("__", "*")

            known_positions_ = known_positions_from_guess(guess)
            included_characters_ = included_characters_from_guess(guess)
            excluded_characters_ = excluded_characters_from_guess(guess)
            excluded_positions_ = excluded_positions_from_guess(guess)

            # print(f"{known_positions_=} {included_characters_=} {excluded_characters_=} {excluded_positions_=}")

            known_positions = combine_known_positions(known_positions, known_positions_)
            included_characters += included_characters_
            excluded_characters += excluded_characters_
            excluded_positions = combine_excluded_positions(excluded_positions, excluded_positions_)

            # print(f"{known_positions=} {included_characters=} {excluded_characters=} {excluded_positions=}")

            matches = filter_possible_words(known_positions, included_characters, excluded_characters, excluded_positions)

            inc_c = set(included_characters)
            s = ''.join(matches)
            all_c = set(s)
            d = sorted([(k,s.count(k)) for k in all_c - inc_c], key=lambda x: (x[1], x[0]), reverse=True)

            # output to user
            if len(matches) > 0:
                print(f"Show {len(matches)} possible words? [y/n] ", end='')
                if input().strip().lower() in ('yes', 'y'):
                    print(*matches, sep="\n")
            else:
                print("No possible words")
            if len(d) > 0:
                print(f"Show {len(d)} unused character frequencies? [y/n] ", end='')
                if input().strip().lower() in ('yes', 'y'):
                    print(*d, sep="\n")
            else:
                print("No unused characters")
            
            turn += 1
        elif choice == 2:
            print("[Only one utility currently available]")
            print("Choose characters that must be included in the word. ", end="")
            include_characters = input().strip()
            matches = find_words(include_characters)
            if len(matches) > 0:
                print(f"Show {len(matches)} possible words? [y/n] ", end='')
                if input().strip().lower() in ('yes', 'y'):
                    print(*matches, sep="\n")
            else:
                print("No possible words")

        else:
            print("Invalid option.")
