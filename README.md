# wordle-helper

Possible words list from [3b1b](https://github.com/3b1b/videos/tree/master/_2022/wordle).

3 parameters must be included:

- Known: Characters with known positions as a string of length 5 with `-` as placeholders such as `--xy-`.
- Included: Characters that are included in the word but in unkown location in the form `xyz`.
- Excluded: Characters that are excluded in the word in the form `xyz`.

Example run:

`python helper.py ---o- r canepilt`
