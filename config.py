from helper_classes import BigramsConfig

# Keep this on 2
N_GRAM_LENGTH = 2

# This is the main thing you want to change.
# name:     What you call the language. Could be anything.
# weight:   The percentage of how important this language is. Make sure all weights add up to exactly 100.
# path:     The path to your bigrams-file.
BIGRAMS_CONFIGS = (
    BigramsConfig(
        name = "English",       weight = 100, # %
        path = './bigram_dictionaries/english_bigrams.txt'
    ),
    BigramsConfig(
        name = "German",        weight = 0, # %
        path = './bigram_dictionaries/german_bigrams.txt'
    ),
    BigramsConfig(
        # When using 0%, no optimization will be done using this language.
        # However, you well still be shown stats on how good this layout performs in this language.
        name = "French",        weight = 0, # %
        path = './bigram_dictionaries/french_bigrams.txt'
    )
)

# Define the letters you want to use
LAYER_1_LETTERS = 'etaoinsr'.lower() # All letters for the first cycleNr of calculation, including 'e' (or whatever you put in >staticLetters<)
LAYER_2_LETTERS = 'hldcumfg'.lower() # All letters for the second cycleNr of calculation
LAYER_3_LETTERS = 'pwybvkjx'.lower() # All letters for the third cycleNr of calculation
LAYER_4_LETTERS = 'zq'.lower() # All letters for the fourth cycleNr of calculation

# Define how which of the above letters are interchangeable (variable) between adjacent layers.
# They have to be in the same order as they apear between layer1letters and layer2letters.
# This has a drastic effect on performance. Time for computation skyrockets. This is where the "======>  2 out of X cycleNrs" come from.
#VAR_LETTERS_L1_L2 = 'nsrhld'.lower()
VAR_LETTERS_L1_L2 = ''.lower()

# For layer 1, define that a certain Letter ('e') doesn't change.
# Just pick the most common one in your language.
# You can set it to other letters as well, it doesn't change anything about the quality of the layouts though.
# IF 'e' IS NOT IN YOUR INNERMOST LAYER, PUT ANOTHER LETTER WHERE 'e' IS!!
# ---
# If your rating-system cares about which way layouts are rotated,
# remove 'e' and use {LETTERS_PER_LAYER} empty strings.
STATIC_LETTERS = ('e', '', '', '', '', '', '', '') # the positions go clockwise. 'e' is on the bottom left.
#STATIC_LETTERS = ('', '', '', '', '', '', '', '')

# Define how many layers the layouts you recieve should contain.
NR_OF_LAYERS = 4
# Define how many of the best layer-versions should be used to generate the next layer's layouts.
# This improves Layouts but has a HUGE impact on performance, so be careful.
NR_OF_BEST_LAYOUTS = 500

# Define whether to add a greedy optimization after layers 3 and 4 (recommended)
PERFORM_GREEDY_OPTIMIZATION = True

# Define what information you want to recieve.
SHOW_DATA = True
SHOW_GENERAL_STATS = True
SHOW_TOP_LAYOUTS = 5

# You can use this section to test your custom-made layouts.
TEST_CUSTOM_LAYOUTS = True
# The layout-strings use a different formatting than the XML.
# They are defined, starting fromm the bottom left, going clockwise. Layer per layer, from innermost to outermost.
CUSTOM_LAYOUTS = (
    ('Old / original 8VIM layout', 'nomufv-w eilhkj-- tscdzg-- yabrpxq-'.lower()),
    #('Example Layout', 'ghopwx-- abijqryz cdklst-- efmnuv--'.lower()),
)

# Unless you're trying out a super funky layout with more (or less) than 4 sectors, this should be 8.
LETTERS_PER_LAYER = 8

# Ignore this variable:
DEBUG_MODE = False

# Use Multiprocessing (disable this when using `pypy3 8vim_keyboard_layout_calculator.py`)
USE_MULTIPROCESSING = False

# Symbol used for filling up layer 4. If your alphabet or your bigram-list for some reason contains "-", change - to something else.
FILL_SYMBOL = '-'

# 32 characters that aren't part of your bigram-corpus or your layout. They need to be within the first 256 slots of the ascii-table.
ASCII_REPLACEMENT_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]", "{", "}", "(", ")", "<", ">", "/", "_", ",", "~", "¦", "±", "²", "³", "¶", "¹", "¼", "½", "¾", "¿"]

# Ignore this option.
SCREEN_WIDTH = 100

# The rating-system you want to use. To use a different list of scores,
# replace "KJOETOM_SCORE_LIST" by something else which can be found in
# the `score_list.py`-file.
from score_lists import KJOETOM_SCORE_LIST as SCORE_LIST