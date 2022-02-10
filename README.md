# wordle-helper

Possible words list from [3b1b](https://github.com/3b1b/videos/tree/master/_2022/wordle).

usage: helper.py known_positions included_characters excluded_characters

- `known_positions`: Characters with known positions as a string of length 5 with `-` as placeholders such as `--xy-`.
- `included_characters`: Characters that are included in the word but in unkown location in the form `xyz`.
- `excluded_characters`: Characters that are excluded in the word in the form `xyz`.

Example run with `o` locked in, `r` in an unknown location, and the letters `canepilt` not contained.

`python helper.py ---o- r canepilt`
