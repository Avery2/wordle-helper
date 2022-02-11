# wordle-helper

Possible words list from [3b1b](https://github.com/3b1b/videos/tree/master/_2022/wordle).

usage: `helper.py known_positions included_characters excluded_characters`

- `known_positions`: Characters with known positions as a string of length 5 with `-` as placeholders such as `--xy-`.
- `included_characters`: Characters that are included in the word but in unkown location in the form `xyz`.
- `excluded_characters`: Characters that are excluded in the word in the form `xyz`.
- `excluded_positions`: Characters with known positinois where they do not exist with `,` seperating each position such as `,x,y,,xy`

Example run with `o` locked in, `r` in an unknown location, and the letters `canepilt` not contained.

`python helper.py ---o- r canepilt`

Example run with `o` locked in, `r` in an unknown location, and the letters `canepilt` not contained, and `r` is not in the first position.

`python helper.py ---o- r canepilt r----`

Example of wordle matched with command:

`python helper.py ----- cre an c,er,r,c,e`