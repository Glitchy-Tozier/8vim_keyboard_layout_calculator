from helper_classes import BigramsConfig

# This is the main thing you want to change.
# name:     What you call the language. Could be anything.
# weight:   The percentage of how important this language is. Make sure all weights add up to exactly 100(%).
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
        # However, you will still be shown stats on how good this layout performs in this language.
        name = "French",        weight = 0, # %
        path = './bigram_dictionaries/french_bigrams.txt'
    ),
)

# The number of letters from the 1st and 2nd layers that are interchangable
# This only affects the (n) least frequent letters of layer 1 and the (n) most frequent letters of layer 2
# /!\ BIG PERFORMANCE IMPACT /!\
# (0 - fastest, 8 - slowest)
AUTO_LAYER_SWAP_COUNT = 3
# The number of slots that will be kept empty
# Can be used to reserve room for special symbols such as period, comma, ect.
AUTO_LAYER_EMPTY_COUNT = 6
# Characters that will be ignored when generating layers from bigram-files
# Symbols available in the default 8VIM layout
AUTO_LAYER_IGNORE = ' !"#$%&\'()*+,-./0123456789:;<=>?@[\\]^_`{|}~¡¢£¦§©¬®°¶¿÷€₹™⨯'
# Whether the most common character should be fixed at the bottom-right of all layouts.
# If `True, this option fills up the first slot of `FIXATED_LETTERS`, creating less redundant results.
# Set to `False` if your scoring-system cares about layouts's orientation.
FIXATE_MOST_COMMON_LETTER = True

# Manually define the letters you want to use
# This removes all AUTO_LAYER functionality
MANUALLY_DEFINE_LAYERS = False
LAYER_1_LETTERS = 'etaoinsr'.lower() # All letters for the first cycleNr of calculation, including 'e' (or whatever you put in >staticLetters<)
LAYER_2_LETTERS = 'hldcumfg'.lower() # All letters for the second cycleNr of calculation
LAYER_3_LETTERS = 'pwybvkjx'.lower() # All letters for the third cycleNr of calculation
LAYER_4_LETTERS = 'zq'.lower() # All letters for the fourth cycleNr of calculation

# Define how which of the above letters are interchangeable (variable) between adjacent layers.
# They have to be in the same order as they apear between layer1letters and layer2letters.
# This has a drastic effect on performance. Time for computation skyrockets. This is where the "======>  2 out of X cycleNrs" come from.
VAR_LETTERS_L1_L2 = 'nsrhld'.lower()
#VAR_LETTERS_L1_L2 = ''.lower()

# For layer 1, define that a certain Letter ('e') doesn't change.
# Just pick the most common one in your language.
# You can set it to other letters as well, it doesn't change anything about the quality of the layouts though.
# IF 'e' IS NOT IN YOUR INNERMOST LAYER, PUT ANOTHER LETTER WHERE 'e' IS!!
# ---
# If your rating-system cares about which way layouts are rotated,
# remove 'e' and use {LETTERS_PER_LAYER} empty strings.
FIXATED_LETTERS = ('e', '', '', '', '', '', '', '') # the positions go clockwise. 'e' is on the bottom left.
#FIXATED_LETTERS = ('', '', '', '', '', '', '', '')

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
TEST_CUSTOM_LAYOUTS = True

CUSTOM_LAYOUTS = (
    ('Old / original 8VIM layout (flipped/rotated)', 'ayrbxp-q stdcgz-- iehljk-- onumvfw-'.lower()),
    ('Glitchys original best layout (flipped/rotated)', 'rsbojv-- ntmlfy-- aecdpk-q iuhgzw-x'.lower()),
    ('kjoetoms layout 1', 'rsgujb-- ntkmvy-- oecdpz-q iahlwf-x'.lower()),
    ('kjoetoms layout 2', 'dslfjg-- nhucvy-- oemtpz-- iawrkbqx'.lower()),
    ('kjoetoms layout 3', 'tcimjb-- nhuoky-- aepdfv-- rslgzwqx'.lower()),
 # primary rotated version
    ('Old / original 8VIM layout', 'nomufv-w eilhkj-- tscdzg-- yabrpxq-'.lower()),
    ('Glitchys original best layout', 'uighwzx- eadckpq- tnlmyf-- srobvj--'.lower()),
    #('Example Layout', 'ghopwx-- abijqryz cdklst-- efmnuv--'.lower()),
)

# Unless you're trying out a super funky layout with more (or less) than 4 sectors, this should be 8.
LETTERS_PER_LAYER = 8

# Ignore this variable:
DEBUG_MODE = False

# Use Multiprocessing (disable this when using `pypy3 main.py`)
USE_MULTIPROCESSING = False

# Symbol used for filling up layer 4. If your alphabet or your bigram-list for some reason contains "-", change "-"" to something else.
FILL_SYMBOL = '-'

# 32 characters that aren't part of your bigram-corpus or your layout. They need to be within the first 256 slots of the ascii-table.
ASCII_REPLACEMENT_CHARS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]", "{", "}", "(", ")", "<", ">", "/", "_", ",", "~", "¦", "±", "²", "³", "¶", "¹", "¼", "½", "¾", "¿"]

# Ignore this option.
SCREEN_WIDTH = 100

# The rating-system you want to use. To use a different list of scores,
# replace "KJOETOM_SCORE_LIST" by something else which can be found in
# the `score_list.py`-file.
from score_lists import ORIGINAL_SCORE_LIST as SCORE_LIST
