from array import array
import os.path
import itertools
from collections import OrderedDict
from copy import deepcopy
import math
import random
import statistics
import time
import multiprocessing
from functools import partial
import platform

from config import N_GRAM_LENGTH, BIGRAMS_CONFIGS, LAYER_1_LETTERS, LAYER_2_LETTERS, LAYER_3_LETTERS, LAYER_4_LETTERS, VAR_LETTERS_L1_L2, STATIC_LETTERS, NR_OF_LAYERS, NR_OF_BEST_LAYOUTS, PERFORM_GREEDY_OPTIMIZATION, SHOW_DATA, SHOW_GENERAL_STATS, SHOW_TOP_LAYOUTS, TEST_CUSTOM_LAYOUTS, CUSTOM_LAYOUTS, LETTERS_PER_LAYER, DEBUG_MODE, USE_MULTIPROCESSING, FILL_SYMBOL, ASCII_REPLACEMENT_CHARS, SCORE_LIST, SCREEN_WIDTH
from helper_classes import BigramsConfig, ConfigSpecificResults

start_time = time.time()

def main():
    ###########################################################################################################################
    ###########################################################################################################################
    ################################################### Start of the script ###################################################
    ###########################################################################################################################
    ############################# (Edit `config.py` and `score_list.py` to influence the results) #############################
    ###########################################################################################################################
    ###########################################################################################################################

    # Make sure staticLetters and customLayouts are lowercase and properly formatted
    staticLetters = lowerStaticLetters(STATIC_LETTERS)
    customLayouts = OrderedDict()
    for name, layout in CUSTOM_LAYOUTS:
        customLayouts[name] = xmlStrToOptStr(layout)

    # Validate the main error-hotspots in settings
    if validateSettings(LAYER_1_LETTERS, LAYER_2_LETTERS, LAYER_3_LETTERS, LAYER_4_LETTERS, VAR_LETTERS_L1_L2, staticLetters) is True:
        print("Starting opitimzation with:")
        for config in BIGRAMS_CONFIGS:
            if config.weight > 0:
                print("{}% {},".format(config.weight, config.name), " Path: {}".format(config.path))
        print()
    else:
        # If something is wrong, stop execution
        return

    # Asciify all necessary strings
    layer1letters = asciify(LAYER_1_LETTERS)
    layer2letters = asciify(LAYER_2_LETTERS)
    layer3letters = asciify(LAYER_3_LETTERS)
    layer4letters = asciify(LAYER_4_LETTERS)
    varLetters_L1_L2 = asciify(VAR_LETTERS_L1_L2)
    staticLetters = tuple(asciify(l) for l  in staticLetters)

    # Create the asciiArray
    asciiArray = array("B", [0]*256)

    # Get the letters for the layers possible with the letters you specified.
    firstLayers, secondLayers = getLayerCombinations(layer1letters, layer2letters, varLetters_L1_L2)
    #secondLayers, thirdLayers = getLayers(layer2letters, layer3letters, varLetters_L2_L3)
    nrOfCycles = len(firstLayers)

    # Prepare variables for later.
    tempLayoutList = []
    tempScoresList = []

    finalLayoutList = []
    finalScoresList = []

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
        del layouts_L1


        print("------------------------ %s seconds --- Got best layouts for layer 1" % round((time.time() - start_time), 2))


        # If the user says so, calculate the second layer.
        if NR_OF_LAYERS >= 2:
            ####################################################################################################################
            ################################  Calculate the second Layer

            print("\n------------------------ %s seconds --- Started with layouts for layer 2" % round((time.time() - start_time), 2))

            # Sort the best layer-1 layouts and only return the best ones
            bestLayouts_L1, bestScores_L1 = getTopScores(goodLayouts_L1, goodScores_L1)
            del goodLayouts_L1, goodScores_L1

            # Combine the layouts of layer 1 and layer 2 to all possible variants
            layouts_L1_L2 = combinePermutations(bestLayouts_L1, layouts_L2)
            del bestLayouts_L1, layouts_L2

            # Test the the combined layouts of layer 1 and layer2
            goodLayouts_L1_L2, goodScores_L1_L2 = testLayouts(layouts_L1_L2, asciiArray, bestScores_L1)
            del layouts_L1_L2, bestScores_L1

            print("------------------------ %s seconds --- Got best layouts for layer 2" % round((time.time() - start_time), 2))

            # Add the found layouts to the list (which will later be displayed)
            tempLayoutList.extend(goodLayouts_L1_L2)
            tempScoresList.extend(goodScores_L1_L2)
            del goodLayouts_L1_L2, goodScores_L1_L2
        else:
            # Add the found layouts to the list (which will later be displayed)
            tempLayoutList.extend(goodLayouts_L1)
            tempScoresList.extend(goodScores_L1)
            del goodLayouts_L1, goodScores_L1

    if NR_OF_LAYERS >= 3:
        ####################################################################################################################
        ################################  Calculate the third Layer

        print("\n------------------------ %s seconds --- Started with layouts for layer 3" % round((time.time() - start_time), 2))

        nrOfBestPermutations = NR_OF_BEST_LAYOUTS * 2

        # Sort the best layer-1 layouts and only return the best ones
        bestLayouts_L1_L2, bestScores_L1_L2 = getTopScores(tempLayoutList, tempScoresList)
        del tempLayoutList, tempScoresList

        # Combine the layouts of layer 1 and layer 2 to all possible variants
        layouts_L1_L2_L3 = combinePermutations(bestLayouts_L1_L2, layouts_L3)
        bestLayouts_L1_L2, layouts_L3

        # Test the the combined layouts of layers 1&2 and layer 3
        initialGoodLayouts_L1_L2_L3, initialGoodScores_L1_L2_L3 = testLayouts(layouts_L1_L2_L3, asciiArray, bestScores_L1_L2)
        del layouts_L1_L2_L3, bestScores_L1_L2

        if PERFORM_GREEDY_OPTIMIZATION:
            # Do an additional hillclimbing-optimization
            goodLayouts_L1_L2_L3, goodScores_L1_L2_L3 = greedyOptimization(initialGoodLayouts_L1_L2_L3, initialGoodScores_L1_L2_L3, asciiArray)
        else:
            goodLayouts_L1_L2_L3, goodScores_L1_L2_L3 = initialGoodLayouts_L1_L2_L3, initialGoodScores_L1_L2_L3
        del initialGoodLayouts_L1_L2_L3, initialGoodScores_L1_L2_L3

        print("------------------------ %s seconds --- Got best layouts for layer 3" % round((time.time() - start_time), 2))

        if NR_OF_LAYERS >= 4:
            ####################################################################################################################
            ################################  Calculate the fourth Layer

            print("\n------------------------ %s seconds --- Started with layouts for layer 4" % round((time.time() - start_time), 2))

            nrOfBestPermutations = nrOfBestPermutations * 5

            # Sort the best layer-1 layouts and only return the best ones
            bestLayouts_L1_L2_L3, bestScores_L1_L2_L3 = getTopScores(goodLayouts_L1_L2_L3, goodScores_L1_L2_L3)
            del goodLayouts_L1_L2_L3, goodScores_L1_L2_L3

            # Combine the layouts of layer 1 and layer 2 to all possible variants
            layouts_L1_L2_L3_L4 = combinePermutations(bestLayouts_L1_L2_L3, layouts_L4)
            del bestLayouts_L1_L2_L3, layouts_L4

            # Test the the combined layouts of layers 1&2 and layer 3
            goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4 = testLayouts(layouts_L1_L2_L3_L4, asciiArray, bestScores_L1_L2_L3)
            layouts_L1_L2_L3_L4, bestScores_L1_L2_L3

            if PERFORM_GREEDY_OPTIMIZATION:
                # Do an additional hillclimbing-optimization, then
                # add the found layouts to the list (which will later be displayed)
                finalLayoutList, finalScoresList = greedyOptimization(goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4, asciiArray)
            else:
                finalLayoutList, finalScoresList = goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4
            del goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4

            print("------------------------ %s seconds --- Got best layouts for layer 4" % round((time.time() - start_time), 2))

        else:
            # Do an additional hillclimbing-optimization, then
            # add the found layouts to the list (which will later be displayed)
            finalLayoutList, finalScoresList = goodLayouts_L1_L2_L3, goodScores_L1_L2_L3
            del goodLayouts_L1_L2_L3, goodScores_L1_L2_L3
    else:
        # Add the found layouts to the list (which will later be displayed). This happens if there is no layer 3 or 4.
        finalLayoutList = tempLayoutList
        finalScoresList = tempScoresList
        del tempLayoutList, tempScoresList

    print("\n------------------------ %s seconds --- Done computing" % round((time.time() - start_time), 2))

    if SHOW_DATA is True:
        if TEST_CUSTOM_LAYOUTS is True:
            customScores = array("d", [])
            for name, layout in customLayouts.items():
                # Get the scores for the custom layouts.
                partialLayout = layout[:NR_OF_LAYERS*LETTERS_PER_LAYER]
                bigrams = getBigrams(''.join(sorted(partialLayout)))
                customScore = testSingleLayout(partialLayout, asciiArray, bigrams)
                customScores.append(customScore)

                # If yout're only testing a certain nuber of layers, only use that amount of layers in the name of the custom layouts.
                if len(layout) > (NR_OF_LAYERS*LETTERS_PER_LAYER):
                    layoutStr = layout[:NR_OF_LAYERS*LETTERS_PER_LAYER] + "... (+ more letters that weren't tested. Change nrOfLayers to the correct number to test all of them.)"
                    customLayouts[name] = layoutStr

        
        # Calculate what the perfect score would be
        configSpecificData = [ ConfigSpecificResults(
            "All",
            100,
            getBigrams(layer1letters + layer2letters + layer3letters + layer4letters),
            getPerfectLayoutScore(layer1letters, layer2letters, layer3letters, layer4letters),
        ) ]
        if len(BIGRAMS_CONFIGS) > 1:
            for config in BIGRAMS_CONFIGS:
                originalWeight = config.weight
                fullWeightConfig = config.fullWeightClone()
                
                configSpecificData.append(ConfigSpecificResults(
                    config.name,
                    originalWeight,
                    getBigrams(layer1letters + layer2letters + layer3letters + layer4letters, (fullWeightConfig, )),
                    getPerfectLayoutScore(layer1letters, layer2letters, layer3letters, layer4letters, (fullWeightConfig, )),
                ))

        # Display the data in the terminal.
        showDataInTerminal(finalLayoutList, finalScoresList, configSpecificData, asciiArray, customLayouts, customScores)


def validateSettings(layer1letters, layer2letters, layer3letters, layer4letters, varLetters_L1_L2, staticLetters) -> bool:
    """Checks the user's input for common errors. If everything is correct, returns `True`"""

    layout = layer1letters + layer2letters + layer3letters + layer4letters
    # Check for duplicate letters
    for char in layout:
        if (char != FILL_SYMBOL) and (layout.count(char) > 1):
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
    if len(BIGRAMS_CONFIGS) == 0:
        print("No bigrams-config found.")
        return False
    else:
        for config in BIGRAMS_CONFIGS:
            if os.path.exists(config.path) is False:
                print("The bigram-path you provided does not point to an existing file.")
                print("Language:", config.name, "\nPath:", config.path)
                return False
    return True

replacedWithAscii = dict()
asciiReplacementChars = ASCII_REPLACEMENT_CHARS
def asciify(string: str) -> str:
    """Take a string and replace all non-ascii-chars with ascii-versions of them"""
    result = list(string)
    for idx, char in enumerate(string):
        try: char.encode('ascii')
        except UnicodeEncodeError:
            if char in replacedWithAscii:
                result[idx] = replacedWithAscii[char]
            else:
                replacedWithAscii[char] = asciiReplacementChars[-1]
                asciiReplacementChars.pop()
                result[idx] = replacedWithAscii[char]
    return ''.join(result)

def deAsciify(string: str) -> str:
    """Take turn all replacement-ascii-chars and turn them back into their original forms."""
    result = list(string)
    for idx, char in enumerate(string):
        for replacedChar, asciiChar in replacedWithAscii.items():
            if char == asciiChar:
                result[idx] = replacedChar
    return ''.join(result)

def getLayerCombinations(layer1letters: str, layer2letters: str, varLetters_L1_L2: str):
    """Creates all possible layer-combinations with the letters you specified.
    This includes "varLetters_L1_L2" and "varLetters_L2_L3"
    It always returns two List (of strings)."""

    if varLetters_L1_L2: # Only do all this stuff if there actually exist variable letters.

        L1_Layers = []
        L2_Layers = []

        nrFlexLetters_L1 = round(len(varLetters_L1_L2)/2)
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
def getBigrams(sortedLetters: str, configs: tuple = BIGRAMS_CONFIGS) -> tuple:
    """This opens the bigram-list (the txt-file) and returns the letters and the frequencies of the required bigrams."""
    if configs == BIGRAMS_CONFIGS and sortedLetters in bigramCache:
        return bigramCache[sortedLetters]
    else:
        fullBigramList = []
        
        # Prepare the bigram-letters
        for bigram in itertools.permutations(sortedLetters, N_GRAM_LENGTH):
            fullBigramList.append(''.join(bigram))
        for letter in sortedLetters:
            fullBigramList.append(letter+letter)
        
        # Filter out the bigrams that contain the predefined filler-symbol.
        bigramList = [ b for b in fullBigramList if FILL_SYMBOL not in b ]
        
        # Make sure we also will get the replaced letters from the dictionary.
        for i, bigram in enumerate(bigramList):
            bigramList[i] = deAsciify(bigram)

        normalizedCorpora = []
        for config in configs:
            if config.weight <= 0:
                continue

            # Sum up the corpus's frequencies. Used for later normalization.
            frequencySum = 0
            with open(config.path, 'r') as corpus:                
                for line in corpus:
                    frequencySum += float(line[line.find(' ')+1:])
            
            # Read the file and normalize its contents.
            normalizedCorpus = []
            for currentBigram in bigramList:
                with open(config.path, 'r') as corpus:
                    for line in corpus:
                        line = line.lower()
                        if currentBigram == line[0:N_GRAM_LENGTH]:
                            absFreq = float(line[line.find(' ')+1:])
                            normalizedCorpus.append((
                                currentBigram,
                                absFreq * config.weight / frequencySum
                            ))
                            break
            normalizedCorpora.append(normalizedCorpus)

        bigramsDict = dict()
        for corpus in normalizedCorpora:
            for bigram, freq in corpus:
                if bigram not in bigramsDict:
                    bigramsDict[bigram] = freq
                else:
                    bigramsDict[bigram] += freq

        bigrams = tuple(Bigram(characters, freq) for characters, freq in bigramsDict.items())
        if configs == BIGRAMS_CONFIGS:
            bigramCache[sortedLetters] = bigrams
        return bigrams

def getSumBigramCount(configs: tuple = BIGRAMS_CONFIGS) -> float:
    """This returns the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers."""

    frequencySum = 0.0
    for config in configs:
        if config.weight <= 0:
            continue

        # Sum up the corpus's frequencies. Used for later normalization.
        absoluteSum = 0
        with open(config.path, 'r') as corpus:                
            for line in corpus:
                absoluteSum += float(line[line.find(' ')+1:])
        
        # Read the file and normalize its contents.
        with open(config.path, 'r') as corpus:
            for line in corpus:
                absFreq = float(line[line.find(' ')+1:])
                frequencySum += absFreq * config.weight / absoluteSum

    return frequencySum

def filterBigrams(bigrams: tuple, requiredLetters=[]) -> tuple:
    """Trims the bigram-list to make getPermutations() MUCH faster.
    It basically removes all the bigrams that were already tested.""" # I'm amazing.
    
    indicesToKeep = []
    for j, bigram in enumerate(bigrams):
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

        if keepBigram is True: # Remove the redundant bigrams
            indicesToKeep.append(j)

    trimmedBigrams = tuple(bigrams[index] for index in indicesToKeep)
    return trimmedBigrams

def lowerStaticLetters(staticLetters: tuple) -> tuple:
    """Takes any Iterable and turns its uppercase letters into lowercase ones."""
    lst = list(staticLetters)
    for j, element in enumerate(staticLetters):
        lst[j] = element.lower()
    return tuple(lst)

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
                if staticLetters[letterPlacement] != '':
                    layouts[layoutIteration] += staticLetters[letterPlacement]
                else:
                    layouts[layoutIteration] += letterCombination[j]
                    j+=1

    else: # This is used for all layers except for layer 1
        for layoutIteration, letterCombination in enumerate(itertools.permutations(varLetters)): # try every layout
            layouts[layoutIteration] = ''.join(letterCombination)

    return tuple(layouts)

def fillAndPermuteLayout(letters: str) -> tuple:
    """Creates full layouts out of only a few letters, while avoiding redundancy.
    It is primarily important for layer 4, which many alphabets do not completely fill with letters."""
    missingSlotCount = LETTERS_PER_LAYER - len(letters)
    newLetters = letters + (FILL_SYMBOL * missingSlotCount)

    permutations = itertools.permutations(newLetters) # Get permutations
    layouts = set(''.join(letterList) for letterList in permutations) # Remove all duplicates

    return tuple(layouts)

def testLayouts(layouts: tuple, asciiArray: array, prevScores=None):
    """Calculates the best layouts and returns them (and their scores)."""

    # Combine the Letters for the layer 1 and layer 2
    layoutLetters = layouts[0]
    # Get the letters of the last layer calculated. (if you're only calculating one layer, this is what you get.)
    lastLayerLetters = layoutLetters[-LETTERS_PER_LAYER:]

    if DEBUG_MODE is True:
        print(lastLayerLetters)

    # Get the bigrams for the input letters 
    bigrams = getBigrams(''.join(sorted(layoutLetters)))

    if len(layoutLetters) > LETTERS_PER_LAYER: # Filter out the previous bigrams if there are any that need filtering.
        bigrams = filterBigrams(bigrams, [lastLayerLetters])
    

    if USE_MULTIPROCESSING is True:
        if prevScores:
            if len(prevScores) > 1:
                goodLayouts = []
                goodScores = array("d", [])
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
                goodLayouts = tuple(goodLayouts)

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

def testSingleLayout(layout: str, asciiArray: array, bigrams: tuple) -> float:
    """A toned-down version of testLayouts() and is only tests one layout per call."""

    # Get the bigrams that contain [orderedLetters]
    for j, letter in enumerate(layout): asciiArray[ord(letter)] = j # Fill up asciiArray
    score = sum([bigram.frequency * SCORE_LIST[asciiArray[bigram.letter1AsciiCode]][asciiArray[bigram.letter2AsciiCode]] for bigram in bigrams])
    ### The monstrous line above ^ has the same function as the following block of code:
    # for bigram in bigrams: # Go through every bigram and see how well it flows.
    #         firstLetterPlacement = asciiArray[bigram.letter1AsciiCode]
    #         secondLetterPlacement = asciiArray[bigram.letter2AsciiCode]
    #         scores[k] += bigram.frequency * SCORE_LIST[firstLetterPlacement][secondLetterPlacement]
    return score

def getLayoutScores(layouts: tuple, asciiArray: array, bigrams: tuple, prevScores=None):
    """Tests the layouts and return their scores. It's only used when single-threading."""

    nrLayouts = len(layouts)
    # Create the empty scoring-list
    scores = array("d", [0.0]*nrLayouts)

    # Test the flow of all the layouts.
    for k, layout in enumerate(layouts):
        for j, letter in enumerate(layout): asciiArray[ord(letter)] = j # Fill up asciiArray
        scores[k] = sum([bigram.frequency * SCORE_LIST[asciiArray[bigram.letter1AsciiCode]][asciiArray[bigram.letter2AsciiCode]] for bigram in bigrams])

    ### The monstrous line above ^ has the same function as the following block of code:
    # for bigram in bigrams: # Go through every bigram and see how well it flows.
    #         firstLetterPlacement = asciiArray[bigram.letter1AsciiCode]
    #         secondLetterPlacement = asciiArray[bigram.letter2AsciiCode]
    #         scores[k] += bigram.frequency * SCORE_LIST[firstLetterPlacement][secondLetterPlacement]

    if prevScores:
        # Add the previous layouts' scores. (which weren't tested here. It would be redundant.)
        for j in range(len(prevScores)):
            groupSize = int((nrLayouts / len(prevScores)))
            groupBeginning = groupSize * j
            groupEnding = groupSize * (j+1)
            
            for k in range(groupBeginning, groupEnding):
                scores[k] += prevScores[j]

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
    layouts = allLayouts[groupBeginning : groupEnding]
    bigrams = staticArgs[2]

    prevScore = staticArgs[3][int(groupBeginning/groupSize)]
    scores = array("d", [0.0]*groupSize)

    # Test the flow of all the layouts.
    for k, layout in enumerate(layouts):
        for j, letter in enumerate(layout): asciiArray[ord(letter)] = j # Fill up asciiArray
        scores[k] = prevScore + sum([bigram.frequency * SCORE_LIST[asciiArray[bigram.letter1AsciiCode]][asciiArray[bigram.letter2AsciiCode]] for bigram in bigrams])

    ### The monstrous line above ^ has the same function as the following block of code:
    # scores[k] += prevScore
    # for bigram in bigrams: # Go through every bigram and see how well it flows.
    #         firstLetterPlacement = asciiArray[bigram.letter1AsciiCode]
    #         secondLetterPlacement = asciiArray[bigram.letter2AsciiCode]
    #         scores[k] += bigram.frequency * SCORE_LIST[firstLetterPlacement][secondLetterPlacement]

    # Only use the best scores (and layouts) for performance-reasons
    goodLayouts, goodScores = getTopScores(layouts, scores, 500)
    return goodLayouts, goodScores

def getPerfectLayoutScore(layer1letters: str, layer2letters: str, layer3letters: str, layer4letters: str, configs: tuple = BIGRAMS_CONFIGS) -> float:
    """Creates the score a perfect (impossible) layout would have, just for comparison's sake."""

    best_score_matrix = [] # A matrix that contains the best values for any combination of two layers
    for _ in range(NR_OF_LAYERS):
        best_score_matrix.append([0.0]*NR_OF_LAYERS)

    for letter1_idx, scores in enumerate(SCORE_LIST):
        layer1_idx = math.trunc(letter1_idx/LETTERS_PER_LAYER)
        for layer2_idx in range(layer1_idx, NR_OF_LAYERS):
            scores_for_Lj_Lk = scores[LETTERS_PER_LAYER*layer2_idx : LETTERS_PER_LAYER*layer2_idx+LETTERS_PER_LAYER]
            if max(scores_for_Lj_Lk) > best_score_matrix[layer1_idx][layer2_idx]:
                best_score_matrix[layer1_idx][layer2_idx] = max(scores_for_Lj_Lk)

    best_score_matrix.insert(0, [0.0]*NR_OF_LAYERS) # Add empty rows so that we can access the values with the layer-numbers instead of the layer-indices
    for i in range(len(best_score_matrix)):
        best_score_matrix[i].insert(0, 0)

    bigrams_L1_L1 = getBigrams(''.join(sorted(layer1letters)), configs)
    # print("bigramLetters_L1_L1", bigramLetters_L1_L1)
    perfectScore = sum(bigram.frequency for bigram in bigrams_L1_L1) * best_score_matrix[1][1]
    
    if NR_OF_LAYERS > 1:
        bigrams_L2 = getBigrams(''.join(sorted(layer1letters+layer2letters)), configs)
        bigrams_L1_L2 = filterBigrams(bigrams_L2, [layer1letters, layer2letters])
        bigrams_L2_L2 = getBigrams(''.join(sorted(layer2letters)), configs)
        # print("bigramLetters_L1_L2", bigramLetters_L1_L2)
        # print("bigramLetters_L2_L2", bigramLetters_L2_L2)
        perfectScore += sum(bigram.frequency for bigram in bigrams_L1_L2) * best_score_matrix[1][2]
        perfectScore += sum(bigram.frequency for bigram in bigrams_L2_L2) * best_score_matrix[2][2]
        
        if NR_OF_LAYERS > 2:
            bigrams_L3 = getBigrams(''.join(sorted(layer1letters+layer2letters+layer3letters)), configs)
            bigrams_L1_L3 = filterBigrams(bigrams_L3, [layer1letters, layer3letters])
            bigrams_L2_L3 = filterBigrams(bigrams_L3, [layer2letters, layer3letters])
            bigrams_L3_L3 = getBigrams(''.join(sorted(layer3letters)), configs)
            # print("bigramLetters_L1_L3", bigramLetters_L1_L3)
            # print("bigramLetters_L2_L3", bigramLetters_L2_L3)
            # print("bigramLetters_L3_L3", bigramLetters_L3_L3)
            perfectScore += sum(bigram.frequency for bigram in bigrams_L1_L3) * best_score_matrix[1][3]
            perfectScore += sum(bigram.frequency for bigram in bigrams_L2_L3) * best_score_matrix[2][3]
            perfectScore += sum(bigram.frequency for bigram in bigrams_L3_L3) * best_score_matrix[3][3]

            if NR_OF_LAYERS > 3:
                bigrams_L4 = getBigrams(''.join(sorted(layer1letters+layer2letters+layer3letters+layer4letters)), configs)
                bigrams_L1_L4 = filterBigrams(bigrams_L4, [layer1letters, layer4letters])
                bigrams_L2_L4 = filterBigrams(bigrams_L4, [layer2letters, layer4letters])
                bigrams_L3_L4 = filterBigrams(bigrams_L4, [layer3letters, layer4letters])
                bigrams_L4_L4 = getBigrams(''.join(sorted(layer4letters)), configs)
                # print("bigramLetters_L1_L4", bigramLetters_L1_L4)
                # print("bigramLetters_L2_L4", bigramLetters_L2_L4)
                # print("bigramLetters_L3_L4", bigramLetters_L3_L4)
                # print("bigramLetters_L4_L4", bigramLetters_L4_L4)
                perfectScore += sum(bigram.frequency for bigram in bigrams_L1_L4) * best_score_matrix[1][4]
                perfectScore += sum(bigram.frequency for bigram in bigrams_L2_L4) * best_score_matrix[2][4]
                perfectScore += sum(bigram.frequency for bigram in bigrams_L3_L4) * best_score_matrix[3][4]
                perfectScore += sum(bigram.frequency for bigram in bigrams_L4_L4) * best_score_matrix[4][4]

    return perfectScore

def getTopScores(layouts: tuple, scores: array, nrOfBest=NR_OF_BEST_LAYOUTS):
    """Returns the best [whatever you set "nrOfBestPermutations" to] layouts with their scores.
    The LAST items of those lists should be the best ones."""

    # Make sure we don't try to get more scores than actually exist
    if nrOfBest > len(scores):
        nrOfBest = len(scores)

    oldScores = scores
    indices = range(len(scores))

    # BEFORE sorting the lists, make sure they're not unnecessarily large
    nrRemainingScores = len(oldScores)
    while nrRemainingScores > nrOfBest*3 and nrRemainingScores > LETTERS_PER_LAYER*2:
        mean = statistics.mean(scores)
        # Get all indices & scores that are above the mean of the remaining scores.
        # This roughly halfes or tripples the remaining scores.
        indices = [i for i, score in enumerate(oldScores) if score >= mean]
        scores = [oldScores[idx] for idx in indices]
        
        newNrRemainingScores = len(scores)
        if newNrRemainingScores == nrRemainingScores:
            break
        else:
            nrRemainingScores = newNrRemainingScores

    # Sort scores & indices. This is way faster thanks to the above while-loop
    sortedScoreIdxTuples = sorted(zip(scores, indices))

    topScores, topIndices = (l for l in zip(*sortedScoreIdxTuples[-nrOfBest:]))
    topLayouts = tuple(layouts[idx] for idx in topIndices)
    topScores = array("d", topScores)

    return topLayouts, topScores

def combinePermutations(list1: tuple, list2: tuple) -> tuple:
    """Creates all possible permutations of two tuples while still keeping them in the right order. (first, second) (a, then b)"""
    listOfStrings = []

    for a in list1:
        listOfStrings.extend(a + b for b in list2)

    return tuple(listOfStrings)

def greedyOptimization(layouts: tuple, scores: array, asciiArray: array):
    """Randomly switches letters in each of the layouts to see whether the layouts can be improved this way."""

    optimizedLayouts = dict(zip(layouts, scores))
    bigrams = getBigrams(''.join(sorted(layouts[0])))
    print("Starting greedy optimization.")
    print("Number of layouts to optimize:", len(layouts))
    for layout, score in zip(layouts, deepcopy(scores)):
        optimizing = True
        while optimizing is True:
            layoutPermutations = performLetterSwaps(layout)
            for i, permutatedLayout in enumerate(layoutPermutations):
                permutatedScore = testSingleLayout(permutatedLayout, asciiArray, bigrams)
                if permutatedScore > score:
                    layout = permutatedLayout
                    score = permutatedScore
                    break
                elif i+1 == len(layoutPermutations):
                    optimizing = False
        if layout not in optimizedLayouts:
            optimizedLayouts[layout] = score
    print("Number of layouts, afterwards:", len(optimizedLayouts))
    print("Finished greedy optimization.")

    return tuple(optimizedLayouts.keys()), array("d", optimizedLayouts.values())

def performLetterSwaps(layout: str) -> set:
    """Get all layouts that are possible through 2-letter-swaps."""
    layouts = set([layout])
    originalLayout = tuple(layout)
    for idx1 in range(len(layout)):
        for idx2 in range(idx1+1, len(layout)):
            copy = list(originalLayout)
            copy[idx1], copy[idx2] = copy[idx2], copy[idx1]
            layoutStr = ''.join(copy)
            if layoutStr not in layouts:
                layouts.add(layoutStr)
    return layouts

def showDataInTerminal(
        layouts: tuple,
        scores: array,
        configSpecificData: list,
        asciiArray: array,
        customLayouts = OrderedDict(),
        customScores = array("d"),
    ) -> None:
    """Displays the results; The best layouts, maybe (if i decide to keep this in here) the worst, and some general data."""

    if SHOW_DATA is True:
        # Get the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers.
        sumOfALLbigrams = getSumBigramCount()

        nrOfLayouts = len(layouts)
        # Order the layouts. [0] is the worst layout, [nrOfLayouts] is the best.
        orderedScores, orderedLayouts = [list(l) for l in zip(*sorted(zip(scores, layouts)))]

        # Make the values more visually appealing.
        for j in range(len(orderedScores)):
            orderedScores[j] = round(orderedScores[j], 2)
        for j in range(len(customScores)):
            customScores[j] = round(customScores[j], 2)

        if SHOW_TOP_LAYOUTS != 0:
            print('\n')
            print('#'*SCREEN_WIDTH)
            print('#'*SCREEN_WIDTH)
            if SHOW_TOP_LAYOUTS == 1:
                print(' '*(int(SCREEN_WIDTH/2) - 5), 'The King:')
            else:
                print(' '*(int(SCREEN_WIDTH/2) - 12), 'The top', SHOW_TOP_LAYOUTS, 'BEST layouts:')
            
            j=nrOfLayouts-1
            while j > nrOfLayouts-SHOW_TOP_LAYOUTS-1:
                layout = orderedLayouts[j]
                placing = nrOfLayouts-j
                
                printLayoutData(layout, asciiArray, configSpecificData, placing=placing)
                j-=1

        if TEST_CUSTOM_LAYOUTS is True:
            print('#'*SCREEN_WIDTH)
            print('#'*SCREEN_WIDTH)
            print(' '*(int(SCREEN_WIDTH/2) - 8), "Custom layouts:")

            for name, layout in customLayouts.items():
                printLayoutData(layout, asciiArray, configSpecificData, name=name)
                
        if SHOW_GENERAL_STATS is True:
            writeableBigrams = getBigrams(''.join(sorted(layouts[0]))) # Get all bigrams that actually can be written using this layout.
            writeableFrequencySum = sum(bigram.frequency for bigram in writeableBigrams) # Get the sum of those ^ frequencies.

            if SHOW_TOP_LAYOUTS == 0:
                print('\n')
            print('#'*SCREEN_WIDTH)
            print('#'*SCREEN_WIDTH)
            print(' '*(int(SCREEN_WIDTH/2) - 7), 'General Stats:')
            # print('Number of Layouts tested:', nrOfLayouts)
            print('Time needed for the whole runthrough: %s seconds.' % round((time.time() - start_time), 2))
            print('Amount of bigrams that can be written with the letters used in this layout:',
                    '~%.2f' % float(100*writeableFrequencySum/sumOfALLbigrams), '%')

def optStrToXmlStr(layout: str) -> str:
    """Turns the string-representation which is used internally into one that aligns with 8vim's XML-formatting."""

    b = "{6}{7}{14}{15}{22}{23}{30}{31} {0}{1}{8}{9}{16}{17}{24}{25} {2}{3}{10}{11}{18}{19}{26}{27} {4}{5}{12}{13}{20}{21}{28}{29}"
    layout = deAsciify(layout)
    return b.format(*layout) + "\n" + b.format(*layout.upper())

def xmlStrToOptStr(layout: str) -> str:
    """Turns a layout which uses 8vim's XML-formatting into the string-representation which is used internally while optimizing."""

    b = "{8}{9}{16}{17}{24}{25}{0}{1} {10}{11}{18}{19}{26}{27}{2}{3} {12}{13}{20}{21}{28}{29}{4}{5} {14}{15}{22}{23}{30}{31}{6}{7}"
    layout = layout.replace(' ', '') # Remove whitespaces
    layout = asciify(layout)
    layout = b.format(*layout)
    layout = layout.replace(' ', '') # Remove whitespaces
    return layout

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
    while len(layout) < 32: layout += " "
    layout = layout.replace(FILL_SYMBOL, '▓')
    if platform.system() == 'Windows': # Windows-console needs special treatment.
        blueprint = blueprint.replace('⟍', '\\')
        blueprint = blueprint.replace('⟋', '/')
    return blueprint.format(*layout)

def printLayoutData(layout: str, asciiArray: array, configSpecificData: list, placing: int = None, name: str = None):
    """A function that positions and prints information
    next to the layout-display-string for more compact visuals."""

    print('-'*SCREEN_WIDTH)
    visLayout = layoutVisualisation(layout)
    visLayoutLines = visLayout.split('\n')

    lineToPrint = 0
    if placing is not None:
        print(getExpandedLine(start=visLayoutLines[lineToPrint], end='Layout-placing: ' + str(placing)))
        lineToPrint += 1
    if name is not None:
        print(getExpandedLine(start=visLayoutLines[lineToPrint], end=name))
        lineToPrint += 1

    xmlStr = optStrToXmlStr(layout)
    xmlStrParts = xmlStr.split('\n')
    for xmlStrPart in xmlStrParts:
        print(getExpandedLine(start=visLayoutLines[lineToPrint], end=xmlStrPart))
        lineToPrint += 1

    print(visLayoutLines[lineToPrint])
    lineToPrint += 1

    for data in configSpecificData:
        try:
            visLine = visLayoutLines[lineToPrint]
        except IndexError:
            visLine = ""
        
        lineToPrint += 1
        cfgName = data.name
        weight = data.weight
        score = round(testSingleLayout(layout, asciiArray, data.bigrams), 2)
        perfectScore = data.perfectScore
        if cfgName == "All":
            visName = "All Languages "
            offset = 0
        else:
            visName = cfgName + " {}% ".format(weight)
            offset = 14
        infoStr = " "*offset + visName
        infoStr += '─'*(LETTERS_PER_LAYER*NR_OF_LAYERS+NR_OF_LAYERS-len(visName)-offset) + '> Score: ' + str(score)
        infoStr += '   ~%.2f' % float(100*score/perfectScore) + '%'
        print(
            getExpandedLine(
                start=visLine,
                end=infoStr,
            )
        )

    if lineToPrint < len(visLayoutLines):
        for visLine in visLayoutLines[lineToPrint:]:
            print(visLine)

def getExpandedLine(start="", end=""):
    """Spaces two strings as far apart as possible."""
    remainingSpace = SCREEN_WIDTH - len(start+end)
    return start + " "*remainingSpace + end

class Bigram:
    def __init__(self, bigramCharacters: str, frequency: float):
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
