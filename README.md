# wordle-helper

Words lists from [3b1b](https://github.com/3b1b/videos/tree/master/_2022/wordle).

Warning: Docs are slightly out of date. Everything below is correct but there are undocumented features.

## Usage

### `helper.py`

usage: `helper.py known_positions included_characters excluded_characters`

- `known_positions`: Characters with known positions as a string of length 5 with `-` as placeholders such as `--xy-`.
- `included_characters`: Characters that are included in the word but in unkown location in the form `xyz`. Use `-` if there are none.
- `excluded_characters`: Characters that are excluded in the word in the form `xyz`. Use `-` if there are none.
- `excluded_positions`: Characters with known positinois where they do not exist with `,` seperating each position such as `,x,y,,xy`

### `play.py`

Type the response for each wordle guess. Press the same character multiple times to change it's color. Press enter to lock in that character.

## Examples

Example of wordle and matching command:

<img src="https://user-images.githubusercontent.com/53503018/153552829-753d0ffd-82ac-4fc2-8e89-19a4a796104c.jpeg" width="50%"></img>

```
❯ python helper.py ----- cre an c,er,r,c,e
Show 1 possible words? [y/n] y
ulcer
```

```
❯ python play.py
Type the response for each wordle guess. Indicate yellow by prepending with one underscore (_) and indicate green by prepending with two underscores (__)
Guess 0: _c_ran_e
Show 10 possible words? [y/n] n
Guess 1: p_e_r_ch
Show 1 possible words? [y/n] y
ulcer
```
