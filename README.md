# 8vim_keyboard_layout_calculator

This is a small python script to calculate the best possible layout for https://github.com/flide/8VIM/.

The discussion regarding this program can be found here: https://github.com/flide/8VIM/discussions/138

## Usage
1. Download this project or clone it:
```sh
git clone https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator.git
```
2. Add a [bigram-file](#bigrams) inside the folder [`bigram_dictionaries`](https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator/tree/main/bigram_dictionaries)
3. Open `config.py` and edit the config-parameters to match your language. The most important ones are:
    - `BIGRAMS_CONFIGS`
    - `LAYER_1_LETTERS`
    - `LAYER_2_LETTERS`
    - `LAYER_3_LETTERS`
    - `LAYER_4_LETTERS`
    - `VAR_LETTERS_L1_L2`
    - `NR_OF_BEST_LAYOUTS` (has a big impact on speed)
4. Start the script:
    - _(Install a recent version of [Python](https://www.python.org/))_
    - Navigate to this project's root directory and run the script.  

Recommended: Use [`pypy`](https://www.pypy.org/) (needs to be installed)
```sh
pypy3 main.py
```
If for whatever reason you can't use pypy, to at least benefit from *some* speed improvement, open the `config.py` and enable `USE_MULTIPROCESSING`. Then start the script the regular way:
```sh
python3 main.py
```

### Bigrams
Due to copyrigiht-reasons, I won't add bigram-files to this repository. Please add them yourself. A great resource is [this website](http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/).
Read [this](https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator/blob/main/bigram_dictionaries/readme.txt) for more information.

## Future to-do's (PRs are welcome)
- [ ] If on Windows, don't show results in Terminal. Instead log them to a `results.txt` file. This might prevent crashes when optimizing for non-ascii alphabets.
