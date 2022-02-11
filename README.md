# wordle-helper

Possible words list from [3b1b](https://github.com/3b1b/videos/tree/master/_2022/wordle).

## Usage

usage: `helper.py known_positions included_characters excluded_characters`

- `known_positions`: Characters with known positions as a string of length 5 with `-` as placeholders such as `--xy-`.
- `included_characters`: Characters that are included in the word but in unkown location in the form `xyz`. Use `-` if there are none.
- `excluded_characters`: Characters that are excluded in the word in the form `xyz`. Use `-` if there are none.
- `excluded_positions`: Characters with known positinois where they do not exist with `,` seperating each position such as `,x,y,,xy`

## Examples

### Example run with `o` locked in, `r` in an unknown location, and the letters `canepilt` not contained.

`python helper.py ---o- r canepilt`

### Example run with `o` locked in, `r` in an unknown location, and the letters `canepilt` not contained, and `r` is not in the first position.

`python helper.py ---o- r canepilt r----`

### Example of wordle and matching command:

<img src="https://user-images.githubusercontent.com/53503018/153552829-753d0ffd-82ac-4fc2-8e89-19a4a796104c.jpeg" width="50%"></img>

`python helper.py ----- cre an c,er,r,c,e`
