import os.path
import itertools
from copy import deepcopy
import math
import random
import time
import multiprocessing #import Process
#from threading import Thread
from functools import partial

start_time = time.time()


def main():
    global n_gramLength
    global bigramTxt
    global testingCustomLayouts
    global debugMode
    global useMultiProcessing
    global fillSymbol

    #global useDiacriticsGesture
    global nrOfLettersInEachLayer
    global nrOfLayers
    global nrOfBestPermutations

    global ratings_evenPos_L1
    global ratings_oddPos_L1
    global ratings_evenPos_L2
    global ratings_oddPos_L2
    global ratings_evenPos_L3
    global ratings_oddPos_L3
    global ratings_evenPos_L4
    global ratings_oddPos_L4

    # Define the letters you want to use
    layer1letters = 'eaiolnrt'.lower() # All letters for the first cycleNr of calculation, including 'e' (or whatever you put in >staticLetters<)
    layer2letters = 'scdpumvg'.lower() # All letters for the second cycleNr of calculation
    layer3letters = 'bzfhqkwy'.lower() # All letters for the third cycleNr of calculation
    layer4letters = 'jx'.lower() # All letters for the fourth cycleNr of calculation

    # Define how which of the above letters are interchangeable (variable) between adjacent layers.
    # They have to be in the same order as they apear between layer1letters and layer2letters.
    # This has a drastic effect on performance. Time for computation skyrockets. This is where the "======>  2 out of X cycleNrs" come from.
    #varLetters_L1_L2 = 'nrtscd'.lower()
    varLetters_L1_L2 = 'ts'.lower()
    #varLetters_L2_L3 = ''.lower()
    #varLetters_L3_L4 = ''.lower()

    # Decide whether you want to include diacritics (typed with the diacritics-gesture) in your testing. If you have all the diacritics you need on your main layout, leave this on False.
    #useGestureDiacritics = False
    #gestureDiacritics = ''
    #gestureDiacritics_correspondingLetters = 'aous'


    # For layer 1, define that a certain Letter ('e') doesn't change.
    # Just pick the most common one in your language.
    # You can set it to other letters as well, it doesn't change anything about the quality of the layouts though.
    # IF 'e' IS NOT IN YOUR INNERMOST LAYER, PUT ANOTHER LETTER WHERE 'e' IS!!
    staticLetters = ['e', '', '', '', '', '', '', ''] # the positions go clockwise. 'e' is on the bottom left. 

    # Define how many layers the layouts you recieve should contain.
    nrOfLayers = 4
    # Define how many of the best layer-versions should be. This has a HUGE impact on how long this program will take, so be careful.
    nrOfBestPermutations = 1

    # Define what information you want to recieve.
    showData = True
    showGeneralStats = True
    nrOfTopLayouts = 3
    nrOfBottomLayouts = 0

    # You can use this section to test your custom-made layouts. Leave "'abcdefghijklmnop'," intact, but append any number of your own layouts afterwards.
    testCustomLayouts = True
    customLayoutNames = [
        'Old / original 8VIM layout',
        'English layout by sslater11',
        'English layout 4 by kjoetom',
        'Best English layout found by this script',
        ' ......should be ~91.01 %',]
    customLayouts = [
        'eitsyanolhcdbrmukjzgpxfv----q--w',
        'hitanerolfydmcsujwkgpxbv----q--z',
        'ieaorntsubdhmcflvqypwgkj-x---z--',
        'eotrnsaidfcugmlhxvjykpwbq-z-----',
        'eotrnsaidgcpumlhxvjfbywzq---k---']




    # Define bigram-stuff
    n_gramLength = 2
    bigramTxt = './bigram_dictionaries/italian_bigrams.txt' # <- This is the main thing you want to change. Name it whatever your bigram is called.



    # Define how important layer-placement is as opposed to flow. 0 = only flow is important. 1 =  only what layer the letter is in is important.
    layerVsFlow = 0.5  # /0.6

    # Define the comfort of different Layers. Use numbers between 1 (most comfortable) and 0 (least comfortable).
    L1_comfort = 1
    L2_comfort = 0.7
    L3_comfort = 0.3
    L4_comfort = 0

    # Define what placement-combinations have a "good flow"
    # Put in numbers between 1 (best flow) and 0 (worst flow).
    # 0 (the middle of this array) is assumed to be the position of the first letter. IT'S ASSUMED TO BE EVEN!!!
    # ( = where the 'e' is in the current Layout)
    # +1 is one step clockwise. +2 is two steps clockwise. -1 is one step counterclockwise. -2 is two steps counterclockwise.
    # Place the score-numbers in a way that reflects how well the second letter follows after the first one.
    # For explanations, see https://github.com/flide/8VIM/discussions/99#discussioncomment-585774 and the following messages.
    #                     -7  -6   -5   -4  -3  -2   -1  ~0~ 1   2    3    4   5    6    7
    flow_evenPos_L1 = [0, 0.3, 0.8, 0.5, 1, 0.9, 0.8, 1, 0, 0.3, 0.8, 0.5, 1, 0.9, 0.8]

    #                      -7   -6  -5  -4   -3   -2    -1  ~0~  1    2   3   4    5    6     7
    flow_evenPos_L2 = [0.5, 0.9, 0, 0.5, 0.8, 0.5, 0.95, 1, 0.5, 0.9, 0, 0.5, 0.8, 0.5, 0.95]

    #                     -7 -6  -5   -4  -3  -2   -1   ~0~  1  2   3    4   5   6    7
    flow_evenPos_L3 = [1, 1, 0.4, 0.9, 0, 0.3, 0.5, 0.5, 1, 1, 0.4, 0.9, 0, 0.3, 0.5]

    #                      -7   -6    -5  -4  -3   -2  -1  ~0~   1    2    3    4   5    6   7
    flow_evenPos_L4 = [0.9, 0.5, 0.95, 1, 0.5, 0.9, 0, 0.3, 0.9, 0.5, 0.95, 1, 0.5, 0.9, 0]


    # Unless you're trying out a super funky layout with more (or less) than 4 sectors, this should be 8.
    nrOfLettersInEachLayer = 8

    # Ignore this variable:
    debugMode = False

    # Use Multiprocessing (disable this when using `pypy3 8vim_keyboard_layout_calculator.py`)
    useMultiProcessing = False

    # Symbol used for filling up layer 4. If your alphabet or your bigram-list for some reason contains "-", change - to something else.
    fillSymbol = '-'


    ###########################################################################################################################
    ###########################################################################################################################
    ################################################### Start of the script ###################################################
    ###########################################################################################################################
    ############################## (There's no need to read or change anything after this line) ###############################
    ###########################################################################################################################
    ###########################################################################################################################

    staticLetters = lowercaseList(staticLetters)
    ratings_evenPos_L1, ratings_oddPos_L1 = getScoreList(flow_evenPos_L1, L1_comfort, layerVsFlow)
    ratings_evenPos_L2, ratings_oddPos_L2 = getScoreList(flow_evenPos_L2, L2_comfort, layerVsFlow)
    ratings_evenPos_L3, ratings_oddPos_L3 = getScoreList(flow_evenPos_L3, L3_comfort, layerVsFlow)
    ratings_evenPos_L4, ratings_oddPos_L4 = getScoreList(flow_evenPos_L4, L4_comfort, layerVsFlow)

    # create the asciiArray
    asciiArray, emptySlots = prepareAsciiArray(staticLetters)

    # Get the letters for the layers possible with the letters you specified.
    firstLayers, secondLayers = getLayerLetters(layer1letters, layer2letters, varLetters_L1_L2)
    #secondLayers, thirdLayers = getLayers(layer2letters, layer3letters, varLetters_L2_L3)
    nrOfCycles = len(firstLayers)

    # Prepare variables for later.
    finalLayoutList = []
    finalScoresList = []

    tempLayoutList = []
    tempScoresList = []

    testingCustomLayouts = False

    # Start the actual testing process
    cycleNr=0
    for letters_L1 in firstLayers:
        letters_L2 = secondLayers[cycleNr]
        ####################################################################################################################
        ################################# Calculate the first Layer
        cycleNr+=1

        if nrOfCycles > 1:
            print ('\n======> ', cycleNr, 'out of', nrOfCycles, 'cycles')
        if cycleNr == 2:
            print('\nEstimated time needed for all cycles:', round(nrOfCycles*(time.time() - start_time), 2), 'seconds')
            print("Those only are the cycles for layer 1 and 2 though. Don't worry however; Layer 3 (and 4) should be calculated quicker.")
        print("\n------------------------ %s seconds --- Started with layouts for layer 1" % round((time.time() - start_time), 2))
        

        # get the letters in layer 1 that can actually move.
        varLetters = getVariableLetters(letters_L1, staticLetters)


        # Get all layouts for each Layer with the current layer-letters.
        layouts_L1, layouts_L2, layouts_L3, layouts_L4 = getLayouts(varLetters, staticLetters, letters_L2, layer3letters, layer4letters)

        # Test the layer 1 - layouts
        goodLayouts_L1, goodScores_L1 = testLayouts(layouts_L1, asciiArray, [], staticLetters, emptySlots)


        print("------------------------ %s seconds --- Got best layouts for layer 1" % round((time.time() - start_time), 2))
        
        
        # If the user says so, calculate the second layer.
        if nrOfLayers > 1:
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

        for j in  range(len(layoutList)):
            # Add the found layouts to the list (which will later be displayed)
            tempLayoutList.append(layoutList[j])
            tempScoresList.append(scoresList[j])
    




    if nrOfLayers > 2:
        ####################################################################################################################
        ################################  Calculate the third Layer

        print("\n------------------------ %s seconds --- Started with layouts for layer 3" % round((time.time() - start_time), 2))

        nrOfBestPermutations = nrOfBestPermutations * 2

        # Sort the best layer-1 layouts and only return the best ones
        bestLayouts_L1_L2, bestScores_L1_L2 = getTopScores(tempLayoutList, tempScoresList)


        # Combine the layouts of layer 1 and layer 2 to all possible variants
        layouts_L1_L2_L3 = combinePermutations(bestLayouts_L1_L2, layouts_L3)


        # Test the the combined layouts of layers 1&2 and layer 3
        goodLayouts_L1_L2_L3, goodScores_L1_L2_L3 = testLayouts(layouts_L1_L2_L3, asciiArray, bestScores_L1_L2)


        print("------------------------ %s seconds --- Got best layouts for layer 3" % round((time.time() - start_time), 2))

        if nrOfLayers > 3:
            ####################################################################################################################
            ################################  Calculate the fourth Layer

            print("\n------------------------ %s seconds --- Started with layouts for layer 4" % round((time.time() - start_time), 2))

            nrOfBestPermutations = nrOfBestPermutations * 5

            # Sort the best layer-1 layouts and only return the best ones
            bestLayouts_L1_L2_L3, bestScores_L1_L2_L3 = getTopScores(goodLayouts_L1_L2_L3, goodScores_L1_L2_L3)


            # If layer 4 isn't completely filled with letters, fill the remaining slots of layer 4 with blanks.
            if len(layer4letters) < nrOfLettersInEachLayer:
                pass
                

            # Combine the layouts of layer 1 and layer 2 to all possible variants
            layouts_L1_L2_L3_L4 = combinePermutations(bestLayouts_L1_L2_L3, layouts_L4)


            # Test the the combined layouts of layers 1&2 and layer 3
            goodLayouts_L1_L2_L3_L4, goodScores_L1_L2_L3_L4 = testLayouts(layouts_L1_L2_L3_L4, asciiArray, bestScores_L1_L2_L3)


            print("------------------------ %s seconds --- Got best layouts for layer 4" % round((time.time() - start_time), 2))

            # Add the found layouts to the list (which will later be displayed)
            finalLayoutList = goodLayouts_L1_L2_L3_L4[:]
            finalScoresList = goodScores_L1_L2_L3_L4[:]

        else:
            # Add the found layouts to the list (which will later be displayed)
            finalLayoutList = goodLayouts_L1_L2_L3[:]
            finalScoresList = goodScores_L1_L2_L3[:]
    else:
        # Add the found layouts to the list (which will later be displayed). This happens if there is no layer 3 or 4.
        finalLayoutList = tempLayoutList[:]
        finalScoresList = tempScoresList[:]

    (finalLayoutList, finalScoresList) = greedyOptimization(finalLayoutList, finalScoresList, asciiArray)


    # Calculate what the perfect score would be (when including )
    perfectLayoutScore = getPerfectLayoutScore(layer1letters, layer2letters, layer3letters, layer4letters, L1_comfort, L2_comfort, L3_comfort, L4_comfort, layerVsFlow)

    print("------------------------ %s seconds --- Done computing" % round((time.time() - start_time), 2))

    testingCustomLayouts = testCustomLayouts
    if testingCustomLayouts:
        customScores = []
        customSizeLayouts = []
        for layout in customLayouts:

            # If yout're only testing a certain nuber of layers, only use that amount of layers of the custom layouts.
            if len(layout) > (nrOfLayers*nrOfLettersInEachLayer):
                layoutName = layout[:nrOfLayers*nrOfLettersInEachLayer] + "... (+ more letters that weren't tested. Change nrOfLayers to the correct number to test all of them.)"
                customSizeLayouts.append(layoutName)
            else:
                customSizeLayouts.append(layout)

            # Get the scores for the custom layouts.
            customScore = testSingleLayout(layout[:nrOfLayers*nrOfLettersInEachLayer], asciiArray)
            customScores.append(customScore)

        # Display the data in the terminal.
        showDataInTerminal(finalLayoutList, finalScoresList, customLayoutNames, customSizeLayouts, customScores, perfectLayoutScore, showData, showGeneralStats, nrOfTopLayouts, nrOfBottomLayouts)
    
    else:
        # Display the data in the terminal.
        showDataInTerminal(finalLayoutList, finalScoresList, [], [], [], perfectLayoutScore, showData, showGeneralStats, nrOfTopLayouts, nrOfBottomLayouts)



def getLayerLetters(layer1letters, layer2letters, varLetters_L1_L2):
    # This creates all possible layer-combinations with the letters you specified.
    # This includes "varLetters_L1_L2" and "varLetters_L2_L3"
    # It always returns a List (of strings).

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

            if addCombination: # Only add letter-combinations that are new.
                L1_LayerLetters = fixLetters_L1 + varLetters_L1 
                L2_LayerLetters = combination[nrFlexLetters_L1:] + fixLetters_L2

                L1_Layers.append(L1_LayerLetters)
                L2_Layers.append(L2_LayerLetters)
                
                if debugMode:
                    print(L1_Layers[j], L2_Layers[j])

                j+=1
        return L1_Layers, L2_Layers

    else: # if there are no variable letters between layer 1 and 2, do nothing.
        return [layer1letters], [layer2letters]

def getVariableLetters(fullLayer, staticLetters):
    # This extracts the non-fix letters for the first layer.
    if staticLetters:
        varLetters='' 

        j=0
        while j < len(fullLayer):
            if not fullLayer[j] in staticLetters:
                varLetters += fullLayer[j]
            j+=1

    else:
        varLetters = fullLayer

    return varLetters

def getScoreList(flowList, layerComfort, layerVsFlow):
    # This prepares the fow-list and its reverse for the rest of the program.

    layerImportance = layerVsFlow
    flowImportance = 1-layerVsFlow

    layerScore = layerComfort * layerImportance
    ratingList = []
    
    for flow in flowList:
        flowScore = flow * flowImportance
        
        ratingList.append(flowScore + layerScore)

    ratings = enlargeList(ratingList)

    reverseRatings = ratings[:] # The flow-list for the letters at the odd positions (see beginning of program) is just the
    reverseRatings.reverse()     # same thing, but reversed.

    return ratings, reverseRatings

def enlargeList(flowList):
    # This makes the flowList larger, in accordance to the number of layers
    
    flowList_end = len(flowList)

    firstSlots_flowList = flowList[:nrOfLettersInEachLayer]
    lastslots_flowList = flowList[flowList_end-nrOfLettersInEachLayer:]
    
    j=0
    while j < nrOfLayers:
        flowList =  firstSlots_flowList + flowList + lastslots_flowList
        j+=1
    return flowList

def getBigramList(letters):
    # This opens the bigram-list (the txt-file) and returns the letters and the frequencies of the required bigrams.

    fullBigramArray = []
    bigramFrequency = []
    bigrams = []
    
    # Prepare the bigram-letters
    for bigram in itertools.permutations(letters, n_gramLength):
        fullBigramArray.append(''.join(bigram))
    for letter in letters:
        fullBigramArray.append(letter+letter)
        
    # Filter out the bigrams that contain the predefined filler-symbol.
    bigramArray = [ x for x in fullBigramArray if fillSymbol not in x ]

    # Read the file for the frequencies of the bigrams.
    for currentBigram in bigramArray:
        with open(bigramTxt, 'r') as bbl:
            for line in bbl:
                line = line.lower()
                if currentBigram == line[0:n_gramLength]:
                    bigramFrequency.append(int(line[line.find(' ')+1:]))
                    bigrams.append(currentBigram)
                    break
    return bigrams, bigramFrequency

def getAbsoluteBigramCount():
    # This returns the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers.
    bigramFrequencies = []

    with open(bigramTxt, 'r') as file:
        for line in file:
            bigramFrequencies.append(int(line[line.find(' ')+1:])) # Collect the frequencies of ALL bigrams
    absoluteBigramCount = sum(bigramFrequencies)

    return absoluteBigramCount

def filterBigrams(neededLetters ,bigrams, bigramFrequency):
    # This function trims the bigram-list to make getPermutations() MUCH faster.
    # It basically removes all the bigrams that were already tested. I'm amazing.
    
    trimmedBigrams = bigrams[:]

    j=0
    for bigram in bigrams: # Scan for redundant bigrams
        knockBigramOut = True
        for letter in neededLetters:
            if letter in bigram:
                knockBigramOut = False

        if knockBigramOut: # Remove the redundant bigrams
            trimmedBigrams.pop(j)
            bigramFrequency.pop(j)
            j-=1
        j+=1

    return trimmedBigrams, bigramFrequency

def lowercaseList(list):
    # This just takes any list and turns its uppercase letters into lowercase ones.
    if len(list) != 0:
        j=0
        while j < len(list):
            list[j] = list[j].lower()
            j+=1
        return list

def prepareAsciiArray(staticLetters):
    # This initializes the ascii-array.
    # It also creates the variable "emptySlots", which tells us what slots aren't filled by static letters. (in layer 1)
    asciiArray = [255]*256
    emptySlots = [0]*8
    letterPlacement = 0
    j=0
    while letterPlacement < nrOfLettersInEachLayer:

        if staticLetters[letterPlacement]:
            currentLetter = staticLetters[letterPlacement]
            asciiArray[ord(currentLetter)] = letterPlacement
        else:
            emptySlots[j] = letterPlacement
            j+=1

        letterPlacement += 1

    return asciiArray, emptySlots

def getLayouts(varLetters, staticLetters, layer2letters, layer3letters, layer4letters):
    # This calculates and returns all layouts.

    layer1layouts = getPermutations(varLetters, staticLetters)
    layer2layouts = ['']
    layer3layouts = ['']
    layer4layouts = ['']
    
    if layer2letters:
        layer2layouts = getPermutations(layer2letters)
    if layer3letters:
        layer3layouts = getPermutations(layer3letters)
    if layer4letters:
        if len(layer4letters) == nrOfLettersInEachLayer:
            layer4layouts = getPermutations(layer4letters)
        else:
            layer4layouts = fillUpLayout(layer4letters)
    
    return layer1layouts, layer2layouts, layer3layouts, layer4layouts

def getPermutations(varLetters, staticLetters=[]):
    # This returns all possible letter-positions (permutations) with the input letters.

    layouts = ['']*math.factorial(len(varLetters))

    if staticLetters: # this only activates for layer 1 (that has static letters)
        layoutIteration=0
        for letterCombination in itertools.permutations(varLetters): # try every layout
            letterPlacement = 0
            j=0
            while letterPlacement < nrOfLettersInEachLayer:
                if staticLetters[letterPlacement]:
                    layouts[layoutIteration] += staticLetters[letterPlacement]
                else:
                    layouts[layoutIteration] += letterCombination[j]
                    j+=1
                letterPlacement += 1
            layoutIteration+=1

    else: # This is used for all layers except for layer 1
        layoutIteration=0
        for letterCombination in itertools.permutations(varLetters): # try every layout
            layouts[layoutIteration] = ''.join(letterCombination)
            layoutIteration+=1

    return layouts

def fillUpLayout(letters):
    # This small function creates full layouts out of only a few letters, while avoiding redundancy.
    # It is primarily used for layer 4, which many alphabets do not completely fill with letters.
    newLetters = letters + (fillSymbol * (nrOfLettersInEachLayer-len(letters)))
    layouts = []

    for letterCombination in itertools.permutations(newLetters):
        layout = ''.join(letterCombination)
        if layout not in layouts:
            layouts.append(layout)
    
    return(layouts)

def testLayouts(layouts, asciiArray, prevScores=None, fixedLetters=None, emptySlots=None):
    # This calculates the best layouts and returns them (and their scores).

    # Combine the Letters for the layer 1 and layer 2
    layoutLetters = layouts[0]
    # Get the letters of the last layer calculated. (if you're only calculating one layer, this is what you get.)
    lastLayerLetters = layoutLetters[-nrOfLettersInEachLayer:]

    if debugMode:
        print(lastLayerLetters)

    # Get the bigrams for the input letters 
    bigrams, bigramFrequency = getBigramList(layoutLetters)

    if (len(layoutLetters) > nrOfLettersInEachLayer) & (testingCustomLayouts == False): # Filter out the previous bigrams if there are any that need filtering.
        bigrams, bigramFrequency = filterBigrams(lastLayerLetters, bigrams, bigramFrequency)
    

    if useMultiProcessing:
        if prevScores:
            if len(prevScores) > 1:
                goodLayouts = []
                goodScores = []
                # Prepare the group-sizes of the layout-groups for multiprozessing
                groupBeginnings = []
                for j in range(len(prevScores)):
                    groupBeginnings.append(int((len(layouts) / len(prevScores)) * j)) # Prepare the iterables for the later "pool.map"
                groupSize = groupBeginnings[1]

                # Prepare the flow-lists so they can be used in the next line
                flowList = [ratings_evenPos_L1, ratings_oddPos_L1,
                    ratings_evenPos_L2, ratings_oddPos_L2,
                    ratings_evenPos_L3, ratings_oddPos_L3,
                    ratings_evenPos_L4, ratings_oddPos_L4]

                # Prepare the layout-testing-function and its "static parameters"
                testingFunction = partial(getLayoutScores_multiprocessing, [layouts, asciiArray[:], bigrams, bigramFrequency, prevScores, flowList, groupSize])
                
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
                goodLayouts, goodScores = getLayoutScores(layouts, asciiArray, bigrams, bigramFrequency, prevScores, fixedLetters, emptySlots)
        else:
            # Test the layouts for their flow
            goodLayouts, goodScores = getLayoutScores(layouts, asciiArray, bigrams, bigramFrequency, prevScores, fixedLetters, emptySlots)
    else:
        # Test the layouts for their flow
        goodLayouts, goodScores = getLayoutScores(layouts, asciiArray, bigrams, bigramFrequency, prevScores, fixedLetters, emptySlots)
    
    return goodLayouts, goodScores

def testSingleLayout(layout, asciiArray):
    # This is a toned-down version of testLayouts() and is only used for testing custom layouts. (only one at a time)

    # Get the bigrams for the input letters 
    bigrams, bigramFrequency = getBigramList(layout)
    return getLayoutScores([layout], asciiArray, bigrams, bigramFrequency)[0]  # <- the [0] corrects some weird list-mechanisms.

def getLayoutScores(layouts, asciiArray, bigrams, bigramFrequency, prevScores=None, fixedLetters=None, emptySlots=None):
    # This function tests the layouts and return their scores. It's only used when single-threading.

    # Create the empty scoring-list
    scores = [0]*len(layouts)

    # Test the flow of all the layouts.
    k=0
    for layout in layouts:

        if fixedLetters: # Fill up the asciiArray
            j=0
            while j < len(fixedLetters)-1:
                if fixedLetters[j]:
                    varLayout = layout.replace(fixedLetters[j],'')
                j+=1
            l=0
            for letter in varLayout:
                asciiArray[ord(letter)] = emptySlots[l]
                l+=1
        else:
            j=0
            for letter in layout:
                asciiArray[ord(letter)] = j
                j+=1 # Done with filling up the asciiArray
    
        j=0
        for bigram in bigrams: # go through every bigram and see how well it flows.
            firstLetterPlacement = asciiArray[ord(bigram[0])]
            secondLetterPlacement = asciiArray[ord(bigram[1])]

            if firstLetterPlacement < 8:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L1[secondLetterPlacement - firstLetterPlacement + 7]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L1[secondLetterPlacement - firstLetterPlacement + 7]

            elif firstLetterPlacement < 16:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L2[secondLetterPlacement - firstLetterPlacement + 15]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L2[secondLetterPlacement - firstLetterPlacement + 15]

            elif firstLetterPlacement < 24:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L3[secondLetterPlacement - firstLetterPlacement + 23]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L3[secondLetterPlacement - firstLetterPlacement + 23]

            else:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L4[secondLetterPlacement - firstLetterPlacement + 31]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L4[secondLetterPlacement - firstLetterPlacement + 31]
            j+=1
        k+=1

    if prevScores:
        # Add the previous layouts' scores. (which weren't tested here. It would be redundant.)
        j=0
        while j < len(prevScores):
            groupBeginning = int((len(layouts) / len(prevScores)) * j)
            groupEnding = int((len(layouts) / len(prevScores)) * (j+1))
            
            k = groupBeginning
            while k < groupEnding:
                scores[k] = scores[k] + prevScores[j]
                k+=1
            j+=1

    # if prevScores:
    #     for j in range(len(layouts)):
    #         scores[j] += prevScores

    if len(scores) > 1:
        goodLayouts, goodScores = getTopScores(layouts, scores, 200)
        return goodLayouts, goodScores
    else:
        return scores

def getLayoutScores_multiprocessing(*args):
    # This function tests the layouts and return their scores.
    # Only use this function when using multiprocessing. Otherwise, use "getLayoutScores"

    # Rename the input arguments
    mapArgs = args[1]
    staticArgs = args[0]

    groupSize = staticArgs[6]

    groupBeginning = mapArgs
    groupEnding = groupBeginning + groupSize

    allLayouts = staticArgs[0]
    asciiArray = staticArgs[1]
    bigrams = staticArgs[2]
    bigramFrequency = staticArgs[3]
    prevScore = staticArgs[4][ int(groupBeginning/groupSize)]

    [ratings_evenPos_L1, ratings_oddPos_L1,
        ratings_evenPos_L2, ratings_oddPos_L2,
        ratings_evenPos_L3, ratings_oddPos_L3,
        ratings_evenPos_L4, ratings_oddPos_L4] = staticArgs[5]

    scores = [0]*groupSize
    layouts = allLayouts[groupBeginning : groupEnding]

    # Test the flow of all the layouts.
    k=0
    for layout in layouts:
        #scoresList[k] = 0
        j=0
        for letter in layout:
            asciiArray[ord(letter)] = j
            j+=1 # Done with filling up the asciiArray
    
        j=0
        for bigram in bigrams: # go through every bigram and see how well it flows.
            firstLetterPlacement = asciiArray[ord(bigram[0])]
            secondLetterPlacement = asciiArray[ord(bigram[1])]

            if firstLetterPlacement < 8:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L1[secondLetterPlacement - firstLetterPlacement + 7]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L1[secondLetterPlacement - firstLetterPlacement + 7]

            elif firstLetterPlacement < 16:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L2[secondLetterPlacement - firstLetterPlacement + 15]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L2[secondLetterPlacement - firstLetterPlacement + 15]

            elif firstLetterPlacement < 24:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L3[secondLetterPlacement - firstLetterPlacement + 23]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L3[secondLetterPlacement - firstLetterPlacement + 23]

            else:
                if (firstLetterPlacement % 2) == 0: # if first letter of the bigram is EVEN, check the ratings_evenPos array
                    scores[k] += bigramFrequency[j] * ratings_evenPos_L4[secondLetterPlacement - firstLetterPlacement + 31]
                else: # if it's ODD, check the reversed ratings_oddPos array
                    scores[k] += bigramFrequency[j] * ratings_oddPos_L4[secondLetterPlacement - firstLetterPlacement + 31]
            j+=1
        
        scores[k] += prevScore
        k+=1
    
    # Only use the best scores (and layouts) for performance-reasons
    goodLayouts, goodScores = getTopScores(layouts, scores, 200)

    return goodLayouts, goodScores

def getPerfectLayoutScore(layer1letters, layer2letters, layer3letters, layer4letters, L1_comfort, L2_comfort, L3_comfort, L4_comfort, layerVsFlow):
    # This creates the score a perfect (impossible) layout would have, just for comparison's sake.
    bigramLetters_L1, bigramFrequencies_L1 = getBigramList(layer1letters)
    perfectScore = sum(bigramFrequencies_L1) * ((L1_comfort * layerVsFlow) + (1-layerVsFlow))
    
    if nrOfLayers > 1:
        bigramLetters_L2, bigramFrequencies_L2 = getBigramList(layer1letters+layer2letters)
        bigramLetters_L2, bigramFrequencies_L2 = filterBigrams(layer2letters, bigramLetters_L2, bigramFrequencies_L2)
        perfectScore += sum(bigramFrequencies_L2) * ((L2_comfort * layerVsFlow) + (1-layerVsFlow))
        
        if nrOfLayers > 2:
            bigramLetters_L3, bigramFrequencies_L3 = getBigramList(layer1letters+layer2letters+layer3letters)
            bigramLetters_L3, bigramFrequencies_L3 = filterBigrams(layer3letters, bigramLetters_L3, bigramFrequencies_L3)
            perfectScore += sum(bigramFrequencies_L3) * ((L3_comfort * layerVsFlow) + (1-layerVsFlow))

            if nrOfLayers > 3:
                bigramLetters_L4, bigramFrequencies_L4 = getBigramList(layer1letters+layer2letters+layer3letters+layer4letters)
                bigramLetters_L4, bigramFrequencies_L4 = filterBigrams(layer4letters, bigramLetters_L4, bigramFrequencies_L4)
                perfectScore += sum(bigramFrequencies_L4) * ((L4_comfort * layerVsFlow) + (1-layerVsFlow))

    return(perfectScore)

def getTopScores(layouts, scores, nrOfBest=None):
    # This returns the best [whatever you set "nrOfBestPermutations" to] layouts with their scores.
    # The LAST items of those lists should be the best ones.

    copiedLayouts = layouts[:]
    orderedLayouts = [copiedLayout for _,copiedLayout in sorted(zip(scores,copiedLayouts))]
    
    orderedScores = scores[:]
    orderedScores.sort()
    
    if nrOfBest: # If a custom number of how many best layouts should be returned, return that number of layouts instead of the globally defined nrOfBestPermutations
        index_firstGoodLayout = (len(layouts)-nrOfBest)
    else:
        index_firstGoodLayout = (len(layouts)-nrOfBestPermutations)

    bestLayouts = orderedLayouts[index_firstGoodLayout:]
    biggestScores = orderedScores[index_firstGoodLayout:]

    return bestLayouts, biggestScores

def combinePermutations(list1, list2):
    # This creates all possible permutations of two lists while still keeping them in the right order. (first, second) (a, then b)
    listOfStrings = []

    for a in list1:
        for b in list2:
            listOfStrings.append(a + b)

    return listOfStrings

def greedyOptimization(layouts, scores, asciiArray):
    returnLayouts = layouts
    returnScores = scores
    print("Number of layouts to optimize:", len(layouts))
    for layout, score in zip(deepcopy(layouts), deepcopy(scores)):
        optimizing = True
        while optimizing:
            optimizing = False
            layoutPermutations = performSingleSwaps(layout)
            print("Number of permutations:", len(layoutPermutations))
            for permutatedLayout in layoutPermutations:
                permutatedScore = testSingleLayout(permutatedLayout, asciiArray)
                if permutatedScore > score:
                    print('\nnew better:')
                    print(layout, score)
                    print(permutatedLayout, permutatedScore)

                    optimizing = True
                    layout = permutatedLayout
                    score = permutatedScore
                    break
        print("\nDone optimizing one layout.\n")
        if layout not in returnLayouts:            
            returnLayouts.append(layout)
            returnScores.append(score)
    return returnLayouts, returnScores


def performSingleSwaps(layout):
    """Get all layouts that are possible through 2-letter-swaps."""
    layouts = [layout]
    originalLayout = list(layout)
    for i1 in range(len(layout)):
        for i2 in range(i1+1, len(layout)):
            copy = deepcopy(originalLayout)
            copy[i1], copy[i2] = copy[i2], copy[i1]
            layoutStr = ''.join(copy)
            if layoutStr not in layouts:
                layouts.append(layoutStr)
    random.shuffle(layouts)
    return layouts

def showDataInTerminal(layoutList, scoreList, customLayoutNames, customLayouts, customScores, perfectLayoutScore, showData, showGeneralStats, showTopLayouts, showBottomLayouts):
    # Display the results; The best layouts, maybe (if i decide to keep this in here) the worst, and some general data.
    if showData:

        # Get the total number of all bigram-frequencies, even of those with letters that don't exist in the calculated layers.
        sumOfALLbigrams = getAbsoluteBigramCount()

        # Order the layouts. [0] is the worst layout, [nrOfLayouts] is the best.
        nrOfLayouts = len(layoutList)
        orderedLayouts = [layoutList for _,layoutList in sorted(zip(scoreList,layoutList))]

        #Do the same thing to the scores.
        orderedScoreList = scoreList[:]
        orderedScoreList.sort()

        # Make the values more visually appealing.
        j=0
        while j < len(orderedScoreList):
            orderedScoreList[j] = round(orderedScoreList[j], 2)
            j+=1
        perfectLayoutScore = round(perfectLayoutScore, 2)
        j=0
        while j < len(customScores):
            customScores[j] = round(customScores[j], 2)
            j+=1


        if showTopLayouts != 0:
            print('\n')
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            if showTopLayouts == 1:
                print('                                                       The King:')
            else:
                print('                                                The top', showTopLayouts, 'BEST layouts:')
            
            j=nrOfLayouts-1
            while j > nrOfLayouts-showTopLayouts-1:
                layoutStr = orderedLayouts[j]
                layoutScore = orderedScoreList[j]
                firstLayerLetters =  layoutStr[0:nrOfLettersInEachLayer]
                secondLayerLetters = layoutStr[nrOfLettersInEachLayer:nrOfLettersInEachLayer*2]
                thirdLayerLetters =  layoutStr[nrOfLettersInEachLayer*2:nrOfLettersInEachLayer*3]
                fourthLayerLetters = layoutStr[nrOfLettersInEachLayer*3:nrOfLettersInEachLayer*4]
                
                print('\nLayout:')
                print(firstLayerLetters, secondLayerLetters, thirdLayerLetters, fourthLayerLetters)
                print('─'*(nrOfLettersInEachLayer*nrOfLayers+nrOfLayers+9) + '> Layout-placing:', nrOfLayouts-j)
                print('─'*(nrOfLettersInEachLayer*nrOfLayers+nrOfLayers+9) + '> Score:', layoutScore, '   ~%.2f' % float(100*layoutScore/perfectLayoutScore), '%')
                print(layoutVisualisation(layoutStr), '\n')
                j-=1

        if showBottomLayouts != 0:
            j=0
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            if showBottomLayouts == 1:
                print('                                                   The WORST layout:')
            else:
                print('                                                The top', showBottomLayouts, 'WORST layouts:')
            while j < showBottomLayouts:
                i = showBottomLayouts-j
                layoutStr = orderedLayouts[i]
                layoutScore = orderedScoreList[i]

                firstLayerLetters =  layoutStr[0:nrOfLettersInEachLayer]
                secondLayerLetters = layoutStr[nrOfLettersInEachLayer:nrOfLettersInEachLayer*2]
                thirdLayerLetters =  layoutStr[nrOfLettersInEachLayer*2:nrOfLettersInEachLayer*3]
                fourthLayerLetters = layoutStr[nrOfLettersInEachLayer*3:nrOfLettersInEachLayer*4]

                print('\nLayout:')
                print(firstLayerLetters, secondLayerLetters, thirdLayerLetters, fourthLayerLetters)
                print('Layout-placing:', nrOfLayouts+1-i)
                print('Good bigrams:', layoutScore, '   ~%.2f' % float(100*layoutScore/perfectLayoutScore), '%')
                print(layoutVisualisation(layoutStr), '\n')
                j+=1
            print('Worst Layout: ^^^^')

        if testingCustomLayouts:
            j=0
            print('#######################################################################################################################')
            print('#######################################################################################################################')
            print('                                                    Custom layouts:')

            while j < len(customLayouts):
                print('\n{}:'.format(customLayoutNames[j]))
                print(customLayouts[j])
                print('─'*(nrOfLettersInEachLayer*nrOfLayers+3) + '> Score:', customScores[j], '   ~%.2f' % float(100*customScores[j]/perfectLayoutScore), '%')
                j+=1


        if showGeneralStats:
            allWriteableBigramFrequencies = getBigramList(layoutList[0])[1] # Get the bigram-frequencies for the bigrams that actually can be input using this layout.
            unweightedWriteableFrequency = sum(allWriteableBigramFrequencies) # Get the sum of those ^ frequencies.

            if (showTopLayouts == 0) & (showBottomLayouts == 0):
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

def layoutVisualisation(layout):
    """Takes the layout-letters and gives a visual representation of them.
    Currently only supports layouts with 4-sections."""
    blueprint = """   ⟍  {27}                {28} ⟋
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
    layout = layout.replace(fillSymbol, '▓')
    return blueprint.format(*layout)

if __name__ == '__main__':
    main()