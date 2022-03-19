import os.path
import itertools
from copy import deepcopy
import math
import random
import time
import multiprocessing
from functools import partial
import platform

from score_lists import KJOETOM_SCORE_LIST as SCORE_LIST

start_time = time.time()


def main():
    global N_GRAM_LENGTH
    global BIGRAMS_PATH
    global testingCustomLayouts
    global DEBUG_MODE
    global USE_MULTIPROCESSING
    global replacedWithAscii
    global asciiReplacementCharacters
    global FILL_SYMBOL

    global LETTERS_PER_LAYER
    global NR_OF_LAYERS
    global nrOfBestPermutations


    # Define bigram-stuff
    N_GRAM_LENGTH = 2
    BIGRAMS_PATH = './bigram_dictionaries/english_bigrams.txt' # <- This is the main thing you want to change. Name it whatever your bigrams-corpus is called.


    # Define the letters you want to use
    layer1letters = 'etaoinsr'.lower() # All letters for the first cycleNr of calculation, including 'e' (or whatever you put in >staticLetters<)
    layer2letters = 'hldcumfg'.lower() # All letters for the second cycleNr of calculation
    layer3letters = 'pwybvkjx'.lower() # All letters for the third cycleNr of calculation
    layer4letters = 'zq'.lower() # All letters for the fourth cycleNr of calculation

    # Define how which of the above letters are interchangeable (variable) between adjacent layers.
    # They have to be in the same order as they apear between layer1letters and layer2letters.
    # This has a drastic effect on performance. Time for computation skyrockets. This is where the "======>  2 out of X cycleNrs" come from.
    varLetters_L1_L2 = ''.lower()
    #varLetters_L1_L2 = 'nsrhld'.lower()

    # For layer 1, define that a certain Letter ('e') doesn't change.
    # Just pick the most common one in your language.
    # You can set it to other letters as well, it doesn't change anything about the quality of the layouts though.
    # IF 'e' IS NOT IN YOUR INNERMOST LAYER, PUT ANOTHER LETTER WHERE 'e' IS!!
    #staticLetters = ['e', '', '', '', '', '', '', ''] # the positions go clockwise. 'e' is on the bottom left. 
    staticLetters = ['', '', '', '', '', '', '', '']

    # Define how many layers the layouts you recieve should contain.
    NR_OF_LAYERS = 4
    # Define how many of the best layer-versions should be. This has a HUGE impact on how long this program will take, so be careful.
    nrOfBestPermutations = 100


    # Define what information you want to recieve.
    SHOW_DATA = True
    SHOW_GENERAL_STATS = True
    NR_OF_TOP_LAYOUTS = 5

    # You can use this section to test your custom-made layouts.
    TEST_CUSTOM_LAYOUTS = True
    customLayoutNames = [
        'Example Layout',
        'Old / original 8VIM layout',
        ]
    customLayouts = [
        # Uses a different formatting than the XML.
        # They are defined, starting fromm the bottom left, going clockwise. Layer per layer, from innermost to outermost.
        'abcdefghijklmnopqrstuvwxyz------',
        'eitsyanolhcdbrmukjzgpxfv----q--w',
        ]

    # Unless you're trying out a super funky layout with more (or less) than 4 sectors, this should be 8.
    LETTERS_PER_LAYER = 8

    # Ignore this variable:
    DEBUG_MODE = False

    # Use Multiprocessing (disable this when using `pypy3 8vim_keyboard_layout_calculator.py`)
    USE_MULTIPROCESSING = False

    # Symbol used for filling up layer 4. If your alphabet or your bigram-list for some reason contains "-", change - to something else.
    FILL_SYMBOL = '-'


    # 32 characters that aren't part of your bigram-corpus. They need to be within the first 255 slots of the ascii-table.
    replacedWithAscii = dict()
    asciiReplacementCharacters = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "[", "]", "{", "}", "(", ")", "<", ">", "/", "_", ",", "~", "¦", "±", "²", "³", "¶", "¹", "¼", "½", "¾", "¿"]

    ###########################################################################################################################
    ###########################################################################################################################
    ################################################### Start of the script ###################################################
    ###########################################################################################################################
    ############################## (There's no need to read or change anything after this line) ###############################
    ###########################################################################################################################
    ###########################################################################################################################

    # Make sure staticLetters and customLayouts are lowercase
    staticLetters = lowercaseList(staticLetters)
    customLayouts = lowercaseList(customLayouts)

    # Validate the main error-hotspots in settings
    if validateSettings(layer1letters, layer2letters, layer3letters, layer4letters, varLetters_L1_L2, staticLetters) is True:
        print("Starting opitimzation with bigrams-file:", BIGRAMS_PATH)
    else:
        # If something is wrong, stop execution
        return
    
    # Asciify all necessary strings
    layer1letters = asciify(layer1letters)
    layer2letters = asciify(layer2letters)
    layer3letters = asciify(layer3letters)
    layer4letters = asciify(layer4letters)
    varLetters_L1_L2 = asciify(varLetters_L1_L2)
    for idx, l in enumerate(staticLetters):
        if l is not '':
            staticLetters[idx] = asciify(l)
    for idx, customLayout in enumerate(customLayouts):
        customLayouts[idx] = asciify(customLayout)

    # Create the asciiArray
    asciiArray = [0]*256

    # Get the letters for the layers possible with the letters you specified.
    firstLayers, secondLayers = getLayerCombinations(layer1letters, layer2letters, varLetters_L1_L2)
    #secondLayers, thirdLayers = getLayers(layer2letters, layer3letters, varLetters_L2_L3)
    nrOfCycles = len(firstLayers)

    # Prepare variables for later.
    finalLayoutList = []
    finalScoresList = []

    tempLayoutList = []
    tempScoresList = []

    testingCustomLayouts = False

    # Start the actual testing process
    for cycleNr, letters_L1 in enumerate(firstLayers):
        letters_L2 = secondLayers[cycleNr]
        ####################################################################################################################
        ################################# Calculate the first Layer

        if nrOfCycles > 0:
            print ('\n======> ', cycleNr+1, 'out of', nrOfCycles, 'cycles')
        if cycleNr == 1:
            print('\nEstimated time needed for all cycles:', round(nrOfCycles*(time.time() - start_time), 2), 'seconds')
            print("Those only are the cycles for layer 1 and 2 though. Don't worry however; Layer 3 (and 4) should be calculated quicker.")
        print("\n------------------------ %s seconds --- Started with layouts for layer 1" % round((time.time() - start_time), 2))
        

        # get the letters in layer 1 that can actually move.
        varLetters = getVariableLetters(letters_L1, staticLetters)


        # Get all layouts for each Layer with the current layer-letters.
        layouts_L1, layouts_L2, layouts_L3, layouts_L4 = getLayouts(varLetters, staticLetters, letters_L2, layer3letters, layer4letters)

        # Test the layer 1 - layouts
        goodLayouts_L1, goodScores_L1 = testLayouts(layouts_L1, asciiArray)


        print("------------------------ %s seconds --- Got best layouts for layer 1" % round((time.time() - start_time), 2))
        
        
        # If the user says so, calculate the second layer.
        if NR_OF_LAYERS >= 2:
            ####################################################################################################################
            ################################  Calculate the second Layer

            print("\n------------------------ %s seconds --- Started with layouts for layer 2" % round((time.time() - start_time), 2))

            # Sort the best layer-1 layouts and only return the best ones
            bestLayouts_L1, bestScores_L1 = getTopScores(goodLayouts_L1, goodScores_L1)

            # Combine the layouts of layer 1 and layer 2 to all possible variants
            layouts_L1_L2 = combinePermutations(bestLayouts_L1, layouts_L2)


            # Test the the combined layouts of layer 1 and layer2
            goodLayouts_L1_L2, goodScores_L1_L2 = testLayouts(layouts_L1_L2, asciiArray, bestScores_L1)


            print("------------------------ %s seconds --- Got best layouts for layer 2" % round((time.time() - start_time), 2))

            layoutList, scoresList = goodLayouts_L1_L2, goodScores_L1_L2

        else:
            layoutList, scoresList = goodLayouts_L1, goodScores_L1

        # Add the found layouts to the list (which will later be displayed)
        tempLayoutList.extend(layoutList)
        tempScoresList.extend(scoresList)
    

    if NR_OF_LAYERS >= 3:
        ####################################################################################################################
        ################################  Calculate the third Layer

        print("\n------------------------ %s seconds --- Started with layouts for layer 3" % round((time.time() - start_time), 2))

        nrOfBestPermutations = nrOfBestPermutations * 2

        # Sort the best layer-1 layouts and only return the best ones
        bestLayouts_L1_L2, bestScores_L1_L2 = getTopScores(tempLayoutList, tempScoresList)


        # Combine the layouts of layer 1 and layer 2 to all possible variants
        layouts_L1_L2_L3 = combinePermutations(bestLayouts_L1_L2, layouts_L3)


        # Test the the combined layouts of layers 1&2 and layer 3
        initialGoodLayouts_L1_L2_L3, initialGoodScores_L1_L2_L3 = testLayouts(layouts_L1_L2_L3, asciiArray, bestScores_L1_L2)
        # Do an additional hillclimbing-optimization
        goodLayouts_L1_L2_L3, goodScores_L1_L2_L3 = greedyOptimization(initialGoodLayouts_L1_L2_L3, initialGoodScores_L1_L2_L3, asciiArray)

        print("------------------------ %s seconds --- Got best layouts for layer 3" % round((time.time() - start_time), 2))

        if NR_OF_LAYERS >= 4:
            ####################################################################################################################
            ################################  Calculate the fourth Layer

            print("\n------------------------ %s seconds --- Started with layouts for layer 4" % round((time.time() - start_time), 2))

            nrOfBestPermutations = nrOfBestPermutations * 5

            # Sort the best layer-1 layouts and only return the best ones
            bestLayouts_L1_L2_L3, bestScores_L1_L2_L3 = getTopScores(goodLayouts_L1_L2_L3, goodScores_L1_L2_L3)


            # If layer 4 isn't completely filled with letters, fill the remaining slots of layer 4 with blanks.
            if len(layer4letters) < LETTERS_PER_LAYER:
                pass
                

            # Combine the layouts of layer 1 and layer 2 to all possible variants
            layouts_L1_L2_L3_L4 = combinePermutations(bestLayouts_L1_L2_L3, layouts_L4)


            # Test the the combined layouts of layers 1&2 and layer 3
            goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4 = testLayouts(layouts_L1_L2_L3_L4, asciiArray, bestScores_L1_L2_L3)

            # Do an additional hillclimbing-optimization, then
            # add the found layouts to the list (which will later be displayed)
            finalLayoutList, finalScoresList = greedyOptimization(goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4, asciiArray)

            print("------------------------ %s seconds --- Got best layouts for layer 4" % round((time.time() - start_time), 2))

        else:
            # Do an additional hillclimbing-optimization, then
            # add the found layouts to the list (which will later be displayed)
            finalLayoutList, finalScoresList = goodLayouts_L1_L2_L3, goodScores_L1_L2_L3
    else:
        # Add the found layouts to the list (which will later be displayed). This happens if there is no layer 3 or 4.
        finalLayoutList = tempLayoutList[:]
        finalScoresList = tempScoresList[:]


    # Calculate what the perfect score would be (when including )
    perfectLayoutScore = getPerfectLayoutScore(layer1letters, layer2letters, layer3letters, layer4letters)

    print("\n------------------------ %s seconds --- Done computing" % round((time.time() - start_time), 2))

    testingCustomLayouts = TEST_CUSTOM_LAYOUTS
    if testingCustomLayouts is True:
        customScores = []
        customSizeLayouts = []
        for layout in customLayouts:

            # If yout're only testing a certain nuber of layers, only use that amount of layers of the custom layouts.
            if len(layout) > (NR_OF_LAYERS*LETTERS_PER_LAYER):
                layoutName = layout[:NR_OF_LAYERS*LETTERS_PER_LAYER] + "... (+ more letters that weren't tested. Change nrOfLayers to the correct number to test all of them.)"
                customSizeLayouts.append(layoutName)
            else:
                customSizeLayouts.append(layout)

            # Get the scores for the custom layouts.
            customScore = testSingleLayout(layout[:NR_OF_LAYERS*LETTERS_PER_LAYER], ''.join(sorted(layout[:NR_OF_LAYERS*LETTERS_PER_LAYER])), asciiArray)
            customScores.append(customScore)

        # Display the data in the terminal.
        showDataInTerminal(finalLayoutList, finalScoresList, customLayoutNames, customSizeLayouts, customScores, perfectLayoutScore, SHOW_DATA, SHOW_GENERAL_STATS, NR_OF_TOP_LAYOUTS)
    
    else:
        # Display the data in the terminal.
        showDataInTerminal(finalLayoutList, finalScoresList, [], [], [], perfectLayoutScore, SHOW_DATA, SHOW_GENERAL_STATS, NR_OF_TOP_LAYOUTS)


def validateSettings(layer1letters, layer2letters, layer3letters, layer4letters, varLetters_L1_L2, staticLetters) -> bool:
    """Checks the user's input for common errors. If everything is correct, returns `True`"""

    layout = layer1letters + layer2letters + layer3letters + layer4letters
    # Check for duplicate letters
    for char in layout:
        if (char is not FILL_SYMBOL) and (layout.count(char) > 1):
            print("Duplicate letters found:", char, "\nCheck layer1letters, layer2letters, layer3letters, and layer4letters")
            return False
    # Check whether varLetters_L1_L2's letters are contained in the layers 1 & 2
    for char in varLetters_L1_L2:
        if char not in layer1letters + layer2letters:
            print('"', char, '" was defined in varLetters_L1_L2, but is not part of layer 1 or 2')
            return False
    # Check whether fixed_letters's letters are contained in the ferst layers
    for char in staticLetters:
        if char not in layer1letters:
            print('"', char, '" was defined in staticLetters, but is not part of the first layer')
            return False
    # Check if bigram-file exists
    if os.path.exists(BIGRAMS_PATH) is False:
        print("The bigram-path you provided does not point to an existing file.")
        print(BIGRAMS_PATH)
        return False
    return True

def asciify(string: str) -> str:
    """Take a string and replace all non-ascii-chars with ascii-versions of them"""
    result = list(string)
    for idx, char in enumerate(string):
        try: char.encode('ascii')
        except UnicodeEncodeError:
            if char in replacedWithAscii:
                result[idx] = replacedWithAscii[char]
            else:
                replacedWithAscii[char] = asciiReplacementCharacters[-1]
                asciiReplacementCharacters.pop()
                result[idx] = replacedWithAscii[char]
    return ''.join(result)

def deAsciify(string: str) -> str:
    """Take turn all replacement-ascii-chars and turn them back into their original forms."""
    result = list(string)
    for idx, char in enumerate(string):
        for replacedChar, asciiChar in replacedWithAscii.items():
            if char is asciiChar:
                result[idx] = replacedChar
    return ''.join(result)

def getLayerCombinations(layer1letters: str, layer2letters: str, varLetters_L1_L2: str):
    """Creates all possible layer-combinations with the letters you specified.
    This includes "varLetters_L1_L2" and "varLetters_L2_L3"
    It always returns two List (of strings)."""

    if varLetters_L1_L2: # Only do all this stuff if there actually exist variable letters.

        L1_Layers = []
        L2_Layers = []

        nrFlexLetters_L1 = int(round(len(varLetters_L1_L2)/2))
        nrFlexLetters_L2 = len(varLetters_L1_L2) - nrFlexLetters_L1

        fixLetters_L1 = layer1letters[:-nrFlexLetters_L1]
        fixLetters_L2 =layer2letters[nrFlexLetters_L2:]

        j=0
        for combination in itertools.permutations(varLetters_L1_L2): # Go through every combination of (variable) letters
            addCombination = True

            combination = ''.join(combination)
            varLetters_L1 = sorted(combination[:nrFlexLetters_L1])
            varLetters_L1 = ''.join(varLetters_L1)

            for prevCombination in L1_Layers: # Scan for whether there already exists a versions of the same layer.
                if varLetters_L1 == prevCombination[-nrFlexLetters_L1:]:
                    addCombination = False
                    break

            if addCombination is True: # Only add letter-combinations that are new.
                L1_LayerLetters = fixLetters_L1 + varLetters_L1 
                L2_LayerLetters = combination[nrFlexLetters_L1:] + fixLetters_L2

                L1_Layers.append(L1_LayerLetters)
                L2_Layers.append(L2_LayerLetters)
                
                if DEBUG_MODE is True:
                    print(L1_Layers[j], L2_Layers[j])

                j+=1
        return L1_Layers, L2_Layers

    else: # if there are no variable letters between layer 1 and 2, do nothing.
        return [layer1letters], [layer2letters]

def getVariableLetters(fullLayer: str, staticLetters: str) -> str:
    """Extracts the non-fix letters for the first layer."""
    varLetters='' 

    if staticLetters:
        for i in range(len(fullLayer)):
            if not fullLayer[i] in staticLetters:
                varLetters += fullLayer[i]
    else:
        varLetters = fullLayer

    return varLetters

bigramCache = dict()
def getBigramList(sortedLetters: str) -> list:
    """This opens the bigram-list (the txt-file) and returns the letters and the frequencies of the required bigrams."""
    try: return bigramCache[sortedLetters]
    except KeyError:
        fullBigramArray = []
        bigrams = []
        
        # Prepare the bigram-letters
        for bigram in itertools.permutations(sortedLetters, N_GRAM_LENGTH):
            fullBigramArray.append(''.join(bigram))
        for letter in sortedLetters:
            fullBigramArray.append(letter+letter)
            
        # Filter out the bigrams that contain the predefined filler-symbol.
        bigramArray = [ b for b in fullBigramArray if FILL_SYMBOL not in b ]
        
        # Make sure we also will get the replaced letters from the dictionary.
        for i, bigram in enumerate(bigramArray):
            bigramArray[i] = deAsciify(bigram)

        # Read the file for the frequencies of the bigrams.
        for currentBigram in bigramArray:
            with open(BIGRAMS_PATH, 'r') as corpus:
                for line in corpus:
                    line = line.lower()
                    if currentBigram == line[0:N_GRAM_LENGTH]:
                        bigrams.append(Bigram(currentBigram, int(line[line.find(' ')+1:])))
                        break

        bigramCache[sortedLetters] = bigrams
        return bigrams

def getAbsoluteBigramCount() -> int:
    """This returns the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers."""
    
    frequencySum = 0
    with open(BIGRAMS_PATH, 'r') as corpus:
        for line in corpus:
            frequencySum += int(line[line.find(' ')+1:]) # Add up the frequencies of ALL bigrams
    return int(frequencySum)

def filterBigrams(bigrams: list, requiredLetters=[]) -> list:
    """Trims the bigram-list to make getPermutations() MUCH faster.
    It basically removes all the bigrams that were already tested.""" # I'm amazing.
    
    trimmedBigrams = deepcopy(bigrams)
    j=0
    for bigram in bigrams:
        bigramLetters = bigram.getAsciifiedLetters()

        keepBigram = True
        for letterGroup in requiredLetters:
            foundALetter = False
            for letter in letterGroup:
                if letter in bigramLetters:
                    foundALetter = True
            if foundALetter is False:
                keepBigram = False
                break

        if keepBigram is False: # Remove the redundant bigrams
            trimmedBigrams.pop(j)
            j-=1
        j+=1

    return trimmedBigrams

def lowercaseList(lst: list) -> list:
    """Takes any list and turns its uppercase letters into lowercase ones."""
    for j, element in enumerate(lst):
        lst[j] = element.lower()
    return lst

def getLayouts(varLetters: str, staticLetters: list, layer2letters: str, layer3letters: str, layer4letters: str):
    """Creates and returns a list of layouts."""

    layer1layouts = getPermutations(varLetters, staticLetters)
    layer2layouts = ['']
    layer3layouts = ['']
    layer4layouts = ['']
    
    if NR_OF_LAYERS >= 2:
        if len(layer2letters) == LETTERS_PER_LAYER:
            layer2layouts = getPermutations(layer2letters)
        elif len(layer2letters) < LETTERS_PER_LAYER:
            layer2layouts = fillAndPermuteLayout(layer2letters)
        else:
            print("Error: too many letters in second layer")
    if NR_OF_LAYERS >= 3:
        if len(layer3letters) == LETTERS_PER_LAYER:
            layer3layouts = getPermutations(layer3letters)
        elif len(layer3letters) < LETTERS_PER_LAYER:
            layer3layouts = fillAndPermuteLayout(layer3letters)
        else:
            print("Error: too many letters in third layer")
    if NR_OF_LAYERS == 4:
        if len(layer4letters) == LETTERS_PER_LAYER:
            layer4layouts = getPermutations(layer4letters)
        elif len(layer4letters) < LETTERS_PER_LAYER:
            layer4layouts = fillAndPermuteLayout(layer4letters)
        else:
            print("Error: too many letters in fourth layer")

    return layer1layouts, layer2layouts, layer3layouts, layer4layouts

def getPermutations(varLetters: str, staticLetters=[]) -> list:
    """Returns all possible letter-positions (permutations) with the input letters."""

    layouts = ['']*math.factorial(len(varLetters))

    if len(staticLetters) > 0: # this only activates for layer 1 (that has static letters)
        for layoutIteration, letterCombination in enumerate(itertools.permutations(varLetters)): # try every layout
            j=0
            for letterPlacement in range(LETTERS_PER_LAYER):
                if staticLetters[letterPlacement] is not '':
                    layouts[layoutIteration] += staticLetters[letterPlacement]
                else:
                    layouts[layoutIteration] += letterCombination[j]
                    j+=1

    else: # This is used for all layers except for layer 1
        for layoutIteration, letterCombination in enumerate(itertools.permutations(varLetters)): # try every layout
            layouts[layoutIteration] = ''.join(letterCombination)

    return layouts

def fillAndPermuteLayout(letters: str) -> list:
    """Creates full layouts out of only a few letters, while avoiding redundancy.
    It is primarily used for layer 4, which many alphabets do not completely fill with letters."""
    newLetters = letters + (FILL_SYMBOL * (LETTERS_PER_LAYER-len(letters)))

    permutations = itertools.permutations(newLetters) # Get permutations
    layouts = set([''.join(letterList) for letterList in permutations]) # Remove all duplicates

    return list(layouts)

def testLayouts(layouts, asciiArray, prevScores=None):
    """Calculates the best layouts and returns them (and their scores)."""

    # Combine the Letters for the layer 1 and layer 2
    layoutLetters = layouts[0]
    # Get the letters of the last layer calculated. (if you're only calculating one layer, this is what you get.)
    lastLayerLetters = layoutLetters[-LETTERS_PER_LAYER:]

    if DEBUG_MODE is True:
        print(lastLayerLetters)

    # Get the bigrams for the input letters 
    bigrams = getBigramList(''.join(sorted(layoutLetters)))

    if (len(layoutLetters) > LETTERS_PER_LAYER) & (testingCustomLayouts == False): # Filter out the previous bigrams if there are any that need filtering.
        bigrams = filterBigrams(bigrams, [lastLayerLetters])
    

    if USE_MULTIPROCESSING is True:
        if prevScores:
            if len(prevScores) > 1:
                goodLayouts = []
                goodScores = []
                # Prepare the group-sizes of the layout-groups for multiprozessing
                groupBeginnings = []
                for j in range(len(prevScores)):
                    groupBeginnings.append(int((len(layouts) / len(prevScores)) * j)) # Prepare the iterables for the later "pool.map"
                groupSize = groupBeginnings[1]

                # Prepare the layout-testing-function and its "static parameters"
                testingFunction = partial(getLayoutScores_multiprocessing, [layouts, asciiArray[:], bigrams, prevScores, groupSize])
                
                # Using multithreading, test the layouts for their flow. Only test <= 20 at once.
                maxNrProcesses = 15 # Max number of simuntaneous processes
                j=0
                while j < len(prevScores):
                    resultsList = []

                    # Using multithreading, test the layouts for their flow
                    with multiprocessing.Pool(processes=len(prevScores[j:j+maxNrProcesses])) as pool:
                        resultsList = pool.map(testingFunction, groupBeginnings[j:j+maxNrProcesses])

                    # Add the results to the goodLayouts- and goodScores-lists
                    for results in resultsList:
                        goodLayouts.extend(results[0])
                        goodScores.extend(results[1])
                    j += maxNrProcesses

            else:
                # Test the layouts for their flow
                goodLayouts, goodScores = getLayoutScores(layouts, asciiArray, bigrams, prevScores)
        else:
            # Test the layouts for their flow
            goodLayouts, goodScores = getLayoutScores(layouts, asciiArray, bigrams, prevScores)
    else:
        # Test the layouts for their flow
        goodLayouts, goodScores = getLayoutScores(layouts, asciiArray, bigrams, prevScores)
    
    return goodLayouts, goodScores

def testSingleLayout(layout: str, orderedLetters: str, asciiArray: list) -> int:
    """A toned-down version of testLayouts() and is only tests one layout per call."""

    # Get the bigrams that contain [orderedLetters]
    bigrams = getBigramList(orderedLetters)
    return getLayoutScores([layout], asciiArray, bigrams)

def getLayoutScores(layouts: list, asciiArray: list, bigrams: list, prevScores=None):
    """Tests the layouts and return their scores. It's only used when single-threading."""

    # Create the empty scoring-list
    scores = [0]*len(layouts)

    # Test the flow of all the layouts.
    for k, layout in enumerate(layouts):

        for j, letter in enumerate(layout):
            asciiArray[ord(letter)] = j # Fill up asciiArray
    
        for bigram in bigrams: # Go through every bigram and see how well it flows.
            firstLetterPlacement = asciiArray[bigram.letter1AsciiCode]
            secondLetterPlacement = asciiArray[bigram.letter2AsciiCode]
            scores[k] += bigram.frequency * SCORE_LIST[firstLetterPlacement][secondLetterPlacement]

    if prevScores:
        # Add the previous layouts' scores. (which weren't tested here. It would be redundant.)
        for j in range(len(prevScores)):
            groupSize = int((len(layouts) / len(prevScores)))
            groupBeginning = groupSize * j
            groupEnding = groupSize * (j+1)
            
            for k in range(groupBeginning, groupEnding):
                scores[k] += prevScores[j]

    if len(scores) == 1: return scores[0]
    else:
        goodLayouts, goodScores = getTopScores(layouts, scores, 500)
        return goodLayouts, goodScores

def getLayoutScores_multiprocessing(*args):
    """This function tests the layouts and return their scores.
    Only use this function when using multiprocessing. Otherwise, use [getLayoutScores]"""

    # Rename the input arguments
    staticArgs = args[0]
    mapArgs = args[1]

    groupSize = staticArgs[4]

    groupBeginning = mapArgs
    groupEnding = groupBeginning + groupSize

    allLayouts = staticArgs[0]
    asciiArray = staticArgs[1]
    # Pre-enumerate the bigrams for performance-reasons
    bigrams = staticArgs[2]
    prevScore = staticArgs[3][int(groupBeginning/groupSize)]

    scores = [0]*groupSize
    layouts = allLayouts[groupBeginning : groupEnding]

    # Test the flow of all the layouts.
    for k, layout in enumerate(layouts):
    
        for j, letter in enumerate(layout):
            asciiArray[ord(letter)] = j # Fill up asciiArray
    
        for bigram in bigrams: # go through every bigram and see how well it flows.
            firstLetterPlacement = asciiArray[bigram.letter1AsciiCode]
            secondLetterPlacement = asciiArray[bigram.letter2AsciiCode]
            scores[k] += bigram.frequency * SCORE_LIST[firstLetterPlacement][secondLetterPlacement]
        scores[k] += prevScore
    
    # Only use the best scores (and layouts) for performance-reasons
    goodLayouts, goodScores = getTopScores(layouts, scores, 500)

    return goodLayouts, goodScores

def getPerfectLayoutScore(layer1letters: str, layer2letters: str, layer3letters: str, layer4letters: str) -> int:
    """Creates the score a perfect (impossible) layout would have, just for comparison's sake."""

    best_score_matrix = [] # A matrix that contains the best values for any combination of two layers
    for _ in range(NR_OF_LAYERS):
        best_score_matrix.append([0]*NR_OF_LAYERS)

    for letter1_idx, scores in enumerate(SCORE_LIST):
        layer1_idx = math.trunc(letter1_idx/LETTERS_PER_LAYER)
        for layer2_idx in range(layer1_idx, NR_OF_LAYERS):
            scores_for_Lj_Lk = scores[LETTERS_PER_LAYER*layer2_idx : LETTERS_PER_LAYER*layer2_idx+LETTERS_PER_LAYER]
            if max(scores_for_Lj_Lk) > best_score_matrix[layer1_idx][layer2_idx]:
                best_score_matrix[layer1_idx][layer2_idx] = max(scores_for_Lj_Lk)

    best_score_matrix.insert(0, [0]*NR_OF_LAYERS) # Add empty rows so that we can access the values with the layer-numbers instead of the layer-indices
    for i in range(len(best_score_matrix)):
        best_score_matrix[i].insert(0, 0)

    bigrams_L1_L1 = getBigramList(''.join(sorted(layer1letters)))
    # print("bigramLetters_L1_L1", bigramLetters_L1_L1)
    perfectScore = sum([bigram.frequency for bigram in bigrams_L1_L1]) * best_score_matrix[1][1]
    
    if NR_OF_LAYERS > 1:
        bigrams_L2 = getBigramList(''.join(sorted(layer1letters+layer2letters)))
        bigrams_L1_L2 = filterBigrams(bigrams_L2, [layer1letters, layer2letters])
        bigrams_L2_L2 = getBigramList(''.join(sorted(layer2letters)))
        # print("bigramLetters_L1_L2", bigramLetters_L1_L2)
        # print("bigramLetters_L2_L2", bigramLetters_L2_L2)
        perfectScore += sum([bigram.frequency for bigram in bigrams_L1_L2]) * best_score_matrix[1][2]
        perfectScore += sum([bigram.frequency for bigram in bigrams_L2_L2]) * best_score_matrix[2][2]
        
        if NR_OF_LAYERS > 2:
            bigrams_L3 = getBigramList(''.join(sorted(layer1letters+layer2letters+layer3letters)))
            bigrams_L1_L3 = filterBigrams(bigrams_L3, [layer1letters, layer3letters])
            bigrams_L2_L3 = filterBigrams(bigrams_L3, [layer2letters, layer3letters])
            bigrams_L3_L3 = getBigramList(''.join(sorted(layer3letters)))
            # print("bigramLetters_L1_L3", bigramLetters_L1_L3)
            # print("bigramLetters_L2_L3", bigramLetters_L2_L3)
            # print("bigramLetters_L3_L3", bigramLetters_L3_L3)
            perfectScore += sum([bigram.frequency for bigram in bigrams_L1_L3]) * best_score_matrix[1][3]
            perfectScore += sum([bigram.frequency for bigram in bigrams_L2_L3]) * best_score_matrix[2][3]
            perfectScore += sum([bigram.frequency for bigram in bigrams_L3_L3]) * best_score_matrix[3][3]

            if NR_OF_LAYERS > 3:
                bigrams_L4 = getBigramList(''.join(sorted(layer1letters+layer2letters+layer3letters+layer4letters)))
                bigrams_L1_L4 = filterBigrams(bigrams_L4, [layer1letters, layer4letters])
                bigrams_L2_L4 = filterBigrams(bigrams_L4, [layer2letters, layer4letters])
                bigrams_L3_L4 = filterBigrams(bigrams_L4, [layer3letters, layer4letters])
                bigrams_L4_L4 = getBigramList(''.join(sorted(layer4letters)))
                # print("bigramLetters_L1_L4", bigramLetters_L1_L4)
                # print("bigramLetters_L2_L4", bigramLetters_L2_L4)
                # print("bigramLetters_L3_L4", bigramLetters_L3_L4)
                # print("bigramLetters_L4_L4", bigramLetters_L4_L4)
                perfectScore += sum([bigram.frequency for bigram in bigrams_L1_L4]) * best_score_matrix[1][4]
                perfectScore += sum([bigram.frequency for bigram in bigrams_L2_L4]) * best_score_matrix[2][4]
                perfectScore += sum([bigram.frequency for bigram in bigrams_L3_L4]) * best_score_matrix[3][4]
                perfectScore += sum([bigram.frequency for bigram in bigrams_L4_L4]) * best_score_matrix[4][4]

    return perfectScore

def getTopScores(layouts: list, scores: list, nrOfBest=None):
    """Returns the best [whatever you set "nrOfBestPermutations" to] layouts with their scores.
    The LAST items of those lists should be the best ones."""

    orderedScoreIdxTuples = sorted(zip(scores, range(len(scores))))
    
    if not nrOfBest:
        nrOfBest = nrOfBestPermutations

    topScores, topIndeces = [list(l) for l in zip(*orderedScoreIdxTuples[-nrOfBest:])]
    topLayouts = [layouts[idx] for idx in topIndeces]

    return topLayouts, topScores

def combinePermutations(list1: list, list2: list) -> list:
    """Creates all possible permutations of two lists while still keeping them in the right order. (first, second) (a, then b)"""
    listOfStrings = []

    for a in list1:
        for b in list2:
            listOfStrings.append(a + b)

    return listOfStrings

def greedyOptimization(layouts: list, scores: list, asciiArray: list):
    """Randomly switches letters in each of the layouts to see whether the layouts can be improved this way."""

    allLayouts = dict(zip(layouts, scores))
    orderedLetters = ''.join(sorted(layouts[0]))
    print("Starting greedy optimization.")
    print("Number of layouts to optimize:", len(layouts))
    for layout, score in zip(deepcopy(layouts), deepcopy(scores)):
        optimizing = True
        while optimizing is True:
            layoutPermutations = performLetterSwaps(layout)
            for permutatedLayout in layoutPermutations:
                permutatedScore = testSingleLayout(permutatedLayout, orderedLetters, asciiArray)
                if permutatedScore > score:
                    layout = permutatedLayout
                    score = permutatedScore
                    break
                else: optimizing = False
        if layout not in allLayouts:            
            allLayouts[layout] = score
    print("Number of layouts, afterwards:", len(allLayouts))
    print("Finished greedy optimization.")

    goodLayouts, goodScores = getTopScores(list(allLayouts.keys()), list(allLayouts.values()), 500)
    return goodLayouts, goodScores

def performLetterSwaps(layout: str) -> list:
    """Get all layouts that are possible through 2-letter-swaps."""
    layouts = set([layout])
    originalLayout = list(layout)
    for i1 in range(1, len(layout)):
        for i2 in range(i1+1, len(layout)):
            copy = deepcopy(originalLayout)
            copy[i1], copy[i2] = copy[i2], copy[i1]
            layoutStr = ''.join(copy)
            if layoutStr not in layouts:
                layouts.add(layoutStr)
    return list(layouts)

def showDataInTerminal(
        layouts: list,
        scores: list,
        customLayoutNames: list,
        customLayouts: list,
        customScores: list,
        perfectLayoutScore: int,
        showData: bool,
        showGeneralStats: bool,
        nrOfTopLayouts: int,
    ) -> None:
    """Displays the results; The best layouts, maybe (if i decide to keep this in here) the worst, and some general data."""

    if showData is True:
        # Get the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers.
        sumOfALLbigrams = getAbsoluteBigramCount()

        nrOfLayouts = len(layouts)
        # Order the layouts. [0] is the worst layout, [nrOfLayouts] is the best.
        orderedScores, orderedLayouts = [list(l) for l in zip(*sorted(zip(scores, layouts)))]

        # Make the values more visually appealing.
        for j in range(len(orderedScores)):
            orderedScores[j] = round(orderedScores[j], 2)
        perfectLayoutScore = round(perfectLayoutScore, 2)
        for j in range(len(customScores)):
            customScores[j] = round(customScores[j], 2)

        if nrOfTopLayouts != 0:
            print('\n')
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            if nrOfTopLayouts == 1:
                print('                                                       The King:')
            else:
                print('                                                The top', nrOfTopLayouts, 'BEST layouts:')
            
            j=nrOfLayouts-1
            while j > nrOfLayouts-nrOfTopLayouts-1:
                layout = orderedLayouts[j]
                layoutScore = orderedScores[j]
                firstLayerLetters =  layout[0:LETTERS_PER_LAYER]
                secondLayerLetters = layout[LETTERS_PER_LAYER:LETTERS_PER_LAYER*2]
                thirdLayerLetters =  layout[LETTERS_PER_LAYER*2:LETTERS_PER_LAYER*3]
                fourthLayerLetters = layout[LETTERS_PER_LAYER*3:LETTERS_PER_LAYER*4]
                
                print('\n')
                print(layoutVisualisation(layout))
                print(optStrToXmlStr(layout))
                print('─'*(LETTERS_PER_LAYER*NR_OF_LAYERS+NR_OF_LAYERS+9) + '> Layout-placing:', nrOfLayouts-j)
                print('─'*(LETTERS_PER_LAYER*NR_OF_LAYERS+NR_OF_LAYERS+9) + '> Score:', layoutScore, '   ~%.2f' % float(100*layoutScore/perfectLayoutScore), '%')
                j-=1

        if testingCustomLayouts is True:
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            print('                                                    Custom layouts:')

            for j in range(len(customLayouts)):
                print('\n{}:'.format(customLayoutNames[j]))
                print(optStrToXmlStr(customLayouts[j]))
                print('─'*(LETTERS_PER_LAYER*NR_OF_LAYERS+3) + '> Score:', customScores[j], '   ~%.2f' % float(100*customScores[j]/perfectLayoutScore), '%')

        if showGeneralStats is True:
            allWriteableBigrams = getBigramList(''.join(sorted(layouts[0]))) # Get all bigrams that actually can be written using this layout.
            unweightedWriteableFrequency = sum([bigram.frequency for bigram in allWriteableBigrams]) # Get the sum of those ^ frequencies.

            if nrOfTopLayouts == 0:
                print('\n')
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            print('                                                    General Stats:')
            # print('Number of Layouts tested:', nrOfLayouts)
            print('Time needed for the whole runthrough: %s seconds.' % round((time.time() - start_time), 2))
            print('Amount of bigrams that can be written with the letters used in this layout (without factoring in flow or layer-penalty):')
            print(unweightedWriteableFrequency, 'out of', sumOfALLbigrams, ' (', '~%.2f' % float(100*unweightedWriteableFrequency/sumOfALLbigrams), '%)')
        print('#######################################################################################################################')
        print('########################################### 8vim Keyboard Layout Calculator ###########################################')
        print('#######################################################################################################################')

def optStrToXmlStr(layout: str) -> str:
    """Turns the string-representation which is used internally into one that aligns with 8vim's XML-formatting."""

    b1 = "{6}{7}{14}{15}{22}{23}{30}{31} {0}{1}{8}{9}{16}{17}{24}{25} {2}{3}{10}{11}{18}{19}{26}{27} {4}{5}{12}{13}{20}{21}{28}{29}"
    b2 = "{6}{7}{14}{15}{22}{23}{30}{31} {0}{1}{8}{9}{16}{17}{24}{25} {2}{3}{10}{11}{18}{19}{26}{27} {4}{5}{12}{13}{20}{21}{28}{29}"
    layout = deAsciify(layout)
    return b1.format(*layout) + "\n" + b2.format(*layout.upper())

def layoutVisualisation(layout: str) -> str:
    """Takes the layout-letters and gives a visual representation of them.
    Currently only supports layouts with 4-sections."""
    blueprint = """      ⟍  {27}                {28} ⟋
      {26} ⟍  {19}            {20} ⟋  {29}
        {18} ⟍  {11}        {12} ⟋  {21}
          {10} ⟍  {3}    {4} ⟋  {13}
            {2} ⟍     ⟋  {5}
                ⟍ ⟋
                ⟋ ⟍
            {1} ⟋     ⟍  {6}
          {9} ⟋  {0}    {7} ⟍  {14}
        {17} ⟋  {8}        {15} ⟍  {22}
      {25} ⟋  {16}            {23} ⟍  {30}
      ⟋  {24}                {31} ⟍"""
    layout = deAsciify(layout)
    layout = layout.replace(FILL_SYMBOL, '▓')
    if platform.system() is 'Windows': # Windows-console needs special treatment.
        blueprint = blueprint.replace('⟍', '\\')
        blueprint = blueprint.replace('⟋', '/')
    return blueprint.format(*layout)

class Bigram:
    def __init__(self, bigramCharacters: str, frequency: int):
        # Make sure the bigrams we're actually using only consist of ascii-characters.
        bigramCharacters = asciify(bigramCharacters)
        self.letter1AsciiCode = ord(bigramCharacters[0])
        self.letter2AsciiCode = ord(bigramCharacters[1])
        self.frequency = frequency

    def getAsciifiedLetters(self) -> str:
        return chr(self.letter1AsciiCode) + chr(self.letter2AsciiCode)

    def getRealLetters(self) -> str:
        return deAsciify(self.getAsciifiedLetters())

if __name__ == '__main__':
    main()
