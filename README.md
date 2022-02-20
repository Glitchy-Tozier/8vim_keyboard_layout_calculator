# 8vim_keyboard_layout_calculator

This is a small python script to calculate the best possible layout for https://github.com/flide/8VIM/.

The discussion regarding this program can be found here: https://github.com/flide/8VIM/discussions/138

## Setting everything up
1. Download this project or clone it:
```sh
git clone https://github.com/Glitchy-Tozier/8vim_keyboard_layout_calculator.git
```
2. Add a bigram-file inside the folder bigram_dictionaries
3. Open the python-file and edit the config-parameters to match your language. The most important ones are:
    - layer1letters
    - layer2letters
    - layer3letters
    - layer4letters
    - varLetters_L1_L2
    - nrOfBestPermutations (has a big impact on speed)
    - bigramTxt
4. Start the script:
Navigate to this project's root directory and run the script.  
Recommended: Use [pypy](https://www.pypy.org/)
```sh
pypy3 8vim_keyboard_layout_calculator.py
```
If for whatever reason you can't use pypy, to at least benefit from *some* speed improvement, open the python-file and enable `useMultiProcessing`. Then start the script the regular way:
```sh
python3 8vim_keyboard_layout_calculator.py
```

### Bigrams
Due to the fear of being sued, I won't add bigram-files to this repository. Please add them yourself. A great resource is [this website](http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/).
I'm sure there also are other amazing websites out there, but I'm quite happy with it. You should be able to use most of their bigram-files with **8vim_keyboard_layout_calculator**.
